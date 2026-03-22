# models/train_fake_jobs_model.py
"""
Train Fake Job Detection Model with Multilingual Support
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feature_engineering.feature_router import get_feature_router
from feature_engineering.fake_jobs_features import MultilingualFakeJobsFeatureExtractor
from risk_engine.rule_engine import MultilingualRuleEngine

class MultilingualFakeJobsModelTrainer:
    """
    Trains fake job detection model with multilingual support
    """
    
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_path, "data", "processed", "fake_jobs_preprocessed.csv")
        self.models_path = os.path.join(self.base_path, "models")
        
        os.makedirs(self.models_path, exist_ok=True)
        
        self.router = get_feature_router()
        self.extractor = MultilingualFakeJobsFeatureExtractor()
        self.rule_engine = MultilingualRuleEngine()
        
        self.model = None
        self.scaler = None
        
        print("🚀 Multilingual Fake Jobs Model Trainer Initialized")
    
    def load_and_prepare_data(self):
        """
        Load fake jobs data
        """
        print("\n📊 Loading jobs data...")
        
        if not os.path.exists(self.data_path):
            print("⚠️ Creating sample jobs data...")
            sample_data = {
                'title': [
                    "घर बैठे काम करें, लाखों कमाएं",
                    "வங்கி வேலை - நேரடி நியமனம்",
                    "Software Developer at Google",
                    "మీ ఇంటి నుంచి పని చేయండి",
                    "Data Entry Operator Wanted",
                    "బ్యాంక్ జాబ్స్ - ఫీజు చెల్లించండి",
                    "Amazon Work From Home",
                    "प्रतिष्ठित कंपनी में नौकरी"
                ],
                'description': [
                    "कोई एक्सपीरियंस नहीं चाहिए। रजिस्ट्रेशन फीस ₹500 जमा करें",
                    "பதிவுக் கட்டணம் ₹1000 செலுத்தவும். நேர்காணல் இல்லை",
                    "Submit registration fee of ₹2000 for processing",
                    "రిజిస్ట్రేషన్ ఫీజు ₹1000 చెల్లించండి",
                    "No fees, direct interview at our office",
                    "ఫీజు చెల్లించండి, ఉద్యోగం పొందండి",
                    "No registration fee, genuine opportunity",
                    "कृपया अपना बायोडाटा भेजें, कोई फीस नहीं"
                ],
                'company': [
                    "Unknown Services",
                    "Banking Corp",
                    "Google India",
                    "Tech Solutions",
                    "Data Ltd",
                    "Job Agency",
                    "Amazon",
                    "HR Company"
                ],
                'email': [
                    "hr.jobs@gmail.com",
                    "careers@banking.in",
                    "hr.googl@gmail.com",
                    "jobs@tech.in",
                    "hr@dataltd.com",
                    "apply@jobagency.xyz",
                    "hiring@amazon.com",
                    "careers@company.com"
                ],
                'label': [1, 1, 1, 1, 0, 1, 0, 0]
            }
            df = pd.DataFrame(sample_data)
            print("✅ Created sample data with 8 job postings")
        else:
            df = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(df)} job postings")
        
        # Handle missing values
        text_fields = ['title', 'description', 'company', 'email']
        for field in text_fields:
            if field in df.columns:
                df[field] = df[field].fillna('')
        
        return df
    
    def extract_features(self, df):
        """
        Extract multilingual features from job data
        """
        print("\n🔍 Extracting job features...")
        
        X_list = []
        y_list = []
        
        for idx, row in df.iterrows():
            job_data = {
                'title': row.get('title', ''),
                'description': row.get('description', ''),
                'company': row.get('company', ''),
                'email': row.get('email', '')
            }
            
            features = self.router.extract_features('job', job_data)
            feature_vector = self.router.get_feature_vector('job', job_data, model_type='ml')
            
            X_list.append(feature_vector)
            y_list.append(row['label'])
            
            if (idx + 1) % 10 == 0:
                print(f"  Processed {idx + 1}/{len(df)} jobs...")
        
        X = np.array(X_list)
        y = np.array(y_list)
        
        print(f"\n✅ Extracted features: {X.shape}")
        return X, y
    
    def train_model(self, X, y):
        """
        Train fake jobs model
        """
        print("\n🎯 Training jobs model...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Random Forest works well for job data
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"\n✅ Model trained:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  F1 Score: {f1:.4f}")
        
        return X_test_scaled, y_test
    
    def evaluate_model(self, X_test, y_test):
        """
        Evaluate jobs model
        """
        print("\n📊 Model Evaluation")
        
        y_pred = self.model.predict(X_test)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fake']))
        
        cm = confusion_matrix(y_test, y_pred)
        print("\nConfusion Matrix:")
        print(cm)
    
    def save_model(self):
        """
        Save jobs model
        """
        print("\n💾 Saving model...")
        
        model_path = os.path.join(self.models_path, 'fake_jobs_model.pkl')
        joblib.dump(self.model, model_path)
        
        scaler_path = os.path.join(self.models_path, 'fake_jobs_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        
        print(f"✅ Model saved to: {model_path}")
    
    def run_training_pipeline(self):
        """
        Complete training pipeline
        """
        print("=" * 80)
        print("🚀 MULTILINGUAL FAKE JOBS MODEL TRAINING")
        print("=" * 80)
        
        df = self.load_and_prepare_data()
        X, y = self.extract_features(df)
        X_test, y_test = self.train_model(X, y)
        self.evaluate_model(X_test, y_test)
        self.save_model()
        
        print("\n" + "=" * 80)
        print("✅ FAKE JOBS MODEL TRAINING COMPLETE")
        print("=" * 80)


if __name__ == "__main__":
    trainer = MultilingualFakeJobsModelTrainer()
    trainer.run_training_pipeline()