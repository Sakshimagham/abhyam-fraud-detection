# models/train_websites_model.py
"""
Train Website Fraud Detection Model with Multilingual Support
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
from feature_engineering.web_features import MultilingualWebsiteFeatureExtractor
from risk_engine.rule_engine import MultilingualRuleEngine

class MultilingualWebsiteModelTrainer:
    """
    Trains website fraud detection model with multilingual support
    """
    
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_path, "data", "processed", "websites_preprocessed.csv")
        self.models_path = os.path.join(self.base_path, "models")
        
        os.makedirs(self.models_path, exist_ok=True)
        
        self.router = get_feature_router()
        self.extractor = MultilingualWebsiteFeatureExtractor()
        self.rule_engine = MultilingualRuleEngine()
        
        self.model = None
        self.scaler = None
        
        print("🚀 Multilingual Website Model Trainer Initialized")
    
    def load_and_prepare_data(self):
        """
        Load website data
        """
        print("\n📊 Loading website data...")
        
        if not os.path.exists(self.data_path):
            print("⚠️ Creating sample website data...")
            sample_data = {
                'url': [
                    'https://sbi-secure-login.xyz',
                    'https://pmkisan.gov.in',
                    'https://flipkartt-offer.xyz',
                    'https://bankofindia.co.in',
                    'https://google-secure.com',
                    'https://amazon-offer.top',
                    'https://instagram.com',
                    'https://paytm-kyc-update.xyz'
                ],
                'title': [
                    'SBI - Secure Login',
                    'PM Kisan Samman Nidhi',
                    'Flipkart Big Billion Days',
                    'Bank of India',
                    'Google Security Alert',
                    'Amazon Great Offer',
                    'Instagram',
                    'Paytm KYC Update'
                ],
                'domain_age': [5, 800, 2, 900, 10, 3, 5000, 4],
                'has_ssl': [1, 1, 0, 1, 1, 0, 1, 1],
                'has_contact': [0, 1, 0, 1, 0, 0, 1, 0],
                'label': [1, 0, 1, 0, 1, 1, 0, 1]
            }
            df = pd.DataFrame(sample_data)
            print("✅ Created sample data with 8 websites")
        else:
            df = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(df)} websites")
        
        # Handle missing values
        df['url'] = df['url'].fillna('')
        df['title'] = df['title'].fillna('')
        
        return df
    
    def extract_features(self, df):
        """
        Extract multilingual features from website data
        """
        print("\n🔍 Extracting website features...")
        
        X_list = []
        y_list = []
        
        for idx, row in df.iterrows():
            trust_data = {
                'domain_age': row.get('domain_age', 0),
                'has_ssl': row.get('has_ssl', 0),
                'has_contact': row.get('has_contact', 0)
            }
            
            website_data = {
                'url': row['url'],
                'title': row.get('title', ''),
                'trust_data': trust_data
            }
            
            features = self.router.extract_features('website', website_data)
            feature_vector = self.router.get_feature_vector('website', website_data, model_type='ml')
            
            X_list.append(feature_vector)
            y_list.append(row['label'])
            
            if (idx + 1) % 10 == 0:
                print(f"  Processed {idx + 1}/{len(df)} websites...")
        
        X = np.array(X_list)
        y = np.array(y_list)
        
        print(f"\n✅ Extracted features: {X.shape}")
        return X, y
    
    def train_model(self, X, y):
        """
        Train website fraud model
        """
        print("\n🎯 Training website model...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Random Forest for website features
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
        Evaluate website model
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
        Save website model
        """
        print("\n💾 Saving model...")
        
        model_path = os.path.join(self.models_path, 'web_model.pkl')
        joblib.dump(self.model, model_path)
        
        scaler_path = os.path.join(self.models_path, 'web_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        
        print(f"✅ Model saved to: {model_path}")
    
    def run_training_pipeline(self):
        """
        Complete training pipeline
        """
        print("=" * 80)
        print("🚀 MULTILINGUAL WEBSITE MODEL TRAINING")
        print("=" * 80)
        
        df = self.load_and_prepare_data()
        X, y = self.extract_features(df)
        X_test, y_test = self.train_model(X, y)
        self.evaluate_model(X_test, y_test)
        self.save_model()
        
        print("\n" + "=" * 80)
        print("✅ WEBSITE MODEL TRAINING COMPLETE")
        print("=" * 80)


if __name__ == "__main__":
    trainer = MultilingualWebsiteModelTrainer()
    trainer.run_training_pipeline()