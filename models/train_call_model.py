# models/train_call_model.py
"""
Train Call Fraud Detection Model with Multilingual Support
Trains on call transcript data in multiple Indian languages
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
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feature_engineering.feature_router import get_feature_router
from feature_engineering.call_features import MultilingualCallFeatureExtractor
from risk_engine.rule_engine import MultilingualRuleEngine

class MultilingualCallModelTrainer:
    """
    Trains call fraud detection model with multilingual support
    """
    
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_path, "data", "processed", "call_data_cleaned.csv")
        self.models_path = os.path.join(self.base_path, "models")
        
        os.makedirs(self.models_path, exist_ok=True)
        
        self.router = get_feature_router()
        self.extractor = MultilingualCallFeatureExtractor()
        self.rule_engine = MultilingualRuleEngine()
        
        self.model = None
        self.scaler = None
        
        print("🚀 Multilingual Call Model Trainer Initialized")
    
    def load_and_prepare_data(self):
        """
        Load call transcript data
        """
        print("\n📊 Loading call data...")
        
        if not os.path.exists(self.data_path):
            print(f"⚠️ Creating sample call data...")
            # Create sample data if not exists
            sample_data = {
                'transcript': [
                    "Caller: मी पोलीस अधिकारी बोलतोय. तुमच्यावर केस आहे. पैसे भरा नाहीतर अटक",
                    "Caller: Hello sir, your KYC is expiring. Share OTP to update",
                    "Caller: Congratulations! You won 25 lakhs lottery",
                    "Caller: I'm calling from SBI bank. Your account will be blocked",
                    "Caller: आपला बँक खाते बंद होणार आहे. ओटीपी द्या",
                    "Caller: உங்கள் வங்கி கணக்கு மூடப்படும். OTP பகிரவும்",
                    "Caller: Hi, this is HR from Google. You're selected for interview",
                    "Caller: मैं आयकर विभाग से बोल रहा हूँ। आपके खिलाफ केस है"
                ],
                'duration': [120, 60, 90, 180, 150, 110, 300, 200],
                'caller_id': ['+1234567890', 'UNKNOWN', '+9187654321', 'SBI', 'PRIVATE', '+9198765432', 'GOOGLE', 'UNKNOWN'],
                'label': [1, 1, 1, 1, 1, 1, 0, 1]
            }
            df = pd.DataFrame(sample_data)
            print("✅ Created sample data with 8 calls")
        else:
            df = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(df)} calls")
        
        # Handle missing values
        df['transcript'] = df['transcript'].fillna('').astype(str)
        df['duration'] = df['duration'].fillna(0)
        df['caller_id'] = df['caller_id'].fillna('UNKNOWN')
        
        return df
    
    def extract_features(self, df):
        """
        Extract multilingual features from call data
        """
        print("\n🔍 Extracting call features...")
        
        X_list = []
        y_list = []
        
        for idx, row in df.iterrows():
            call_data = {
                'transcript': row['transcript'],
                'duration': row['duration'],
                'caller_id': row['caller_id']
            }
            
            # Extract features
            features = self.router.extract_features('call', call_data)
            feature_vector = self.router.get_feature_vector('call', call_data, model_type='ml')
            
            X_list.append(feature_vector)
            y_list.append(row['label'])
            
            if (idx + 1) % 10 == 0:
                print(f"  Processed {idx + 1}/{len(df)} calls...")
        
        X = np.array(X_list)
        y = np.array(y_list)
        
        print(f"\n✅ Extracted features: {X.shape}")
        return X, y
    
    def train_model(self, X, y):
        """
        Train call fraud detection model
        """
        print("\n🎯 Training call model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"\n✅ Model trained:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  F1 Score: {f1:.4f}")
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5, scoring='f1_weighted')
        print(f"  CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        return X_test_scaled, y_test
    
    def evaluate_model(self, X_test, y_test):
        """
        Detailed evaluation
        """
        print("\n📊 Detailed Evaluation")
        
        y_pred = self.model.predict(X_test)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraud']))
        
        cm = confusion_matrix(y_test, y_pred)
        print("\nConfusion Matrix:")
        print(cm)
    
    def save_model(self):
        """
        Save trained model
        """
        print("\n💾 Saving model...")
        
        model_path = os.path.join(self.models_path, 'call_model.pkl')
        joblib.dump(self.model, model_path)
        
        scaler_path = os.path.join(self.models_path, 'call_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        
        print(f"✅ Model saved to: {model_path}")
    
    def run_training_pipeline(self):
        """
        Complete training pipeline
        """
        print("=" * 80)
        print("🚀 MULTILINGUAL CALL MODEL TRAINING")
        print("=" * 80)
        
        df = self.load_and_prepare_data()
        X, y = self.extract_features(df)
        X_test, y_test = self.train_model(X, y)
        self.evaluate_model(X_test, y_test)
        self.save_model()
        
        print("\n" + "=" * 80)
        print("✅ CALL MODEL TRAINING COMPLETE")
        print("=" * 80)


if __name__ == "__main__":
    trainer = MultilingualCallModelTrainer()
    trainer.run_training_pipeline()