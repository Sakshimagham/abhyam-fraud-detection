# models/train_social_media_model.py
"""
Train Social Media Fraud Detection Model with Multilingual Support
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
from feature_engineering.social_media_features import MultilingualSocialMediaFeatureExtractor
from risk_engine.rule_engine import MultilingualRuleEngine

class MultilingualSocialMediaModelTrainer:
    """
    Trains social media fraud detection model with multilingual support
    """
    
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_path, "data", "processed", "social_media_preprocessed.csv")
        self.models_path = os.path.join(self.base_path, "models")
        
        os.makedirs(self.models_path, exist_ok=True)
        
        self.router = get_feature_router()
        self.extractor = MultilingualSocialMediaFeatureExtractor()
        self.rule_engine = MultilingualRuleEngine()
        
        self.model = None
        self.scaler = None
        
        print("🚀 Multilingual Social Media Model Trainer Initialized")
    
    def load_and_prepare_data(self):
        """
        Load social media data
        """
        print("\n📊 Loading social media data...")
        
        if not os.path.exists(self.data_path):
            print("⚠️ Creating sample social media data...")
            sample_data = {
                'username': [
                    'priya_singh_23',
                    'crypto_king_india',
                    'real_ananya',
                    'love_forever_786',
                    'tech_guru',
                    'sbi_helpdesk',
                    'travel_with_me',
                    'double_money_123'
                ],
                'bio': [
                    'सिंगल और रेडी टू मैरिज 💕 DM me for friendship',
                    'बिटकॉइन गुरु। पैसे दोगुने करें। लिंक इन बायो',
                    'Travel | Fashion | Lifestyle 📍Mumbai',
                    'உங்கள் வங்கி கணக்கு மூடப்படும் - link in bio',
                    'Tech news and updates',
                    'आपका बैंक खाता बंद होगा - क्लिक करें',
                    'Wanderlust ✈️ Travel blogger',
                    'మీ బ్యాంక్ ఖాతా మూసివేయబడుతుంది'
                ],
                'followers': [15000, 500, 25000, 100, 5000, 50, 15000, 200],
                'following': [120, 1500, 850, 1000, 300, 100, 800, 1800],
                'posts': [45, 120, 320, 5, 500, 2, 800, 10],
                'account_age': [30, 5, 365, 2, 200, 1, 400, 3],
                'is_verified': [0, 0, 1, 0, 0, 0, 1, 0],
                'label': [1, 1, 0, 1, 0, 1, 0, 1]
            }
            df = pd.DataFrame(sample_data)
            print("✅ Created sample data with 8 profiles")
        else:
            df = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(df)} profiles")
        
        # Handle missing values
        df['bio'] = df['bio'].fillna('')
        df['username'] = df['username'].fillna('')
        
        return df
    
    def extract_features(self, df):
        """
        Extract multilingual features from social media data
        """
        print("\n🔍 Extracting social media features...")
        
        X_list = []
        y_list = []
        
        for idx, row in df.iterrows():
            profile_data = {
                'username': row['username'],
                'bio': row['bio'],
                'followers': row['followers'],
                'following': row['following'],
                'posts': row['posts'],
                'account_age': row['account_age'],
                'is_verified': row.get('is_verified', 0)
            }
            
            features = self.router.extract_features('social', profile_data)
            feature_vector = self.router.get_feature_vector('social', profile_data, model_type='ml')
            
            X_list.append(feature_vector)
            y_list.append(row['label'])
            
            if (idx + 1) % 10 == 0:
                print(f"  Processed {idx + 1}/{len(df)} profiles...")
        
        X = np.array(X_list)
        y = np.array(y_list)
        
        print(f"\n✅ Extracted features: {X.shape}")
        return X, y
    
    def train_model(self, X, y):
        """
        Train social media model
        """
        print("\n🎯 Training social media model...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Gradient Boosting for social media patterns
        self.model = GradientBoostingClassifier(
            n_estimators=150,
            max_depth=8,
            learning_rate=0.1,
            random_state=42
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
        Evaluate social media model
        """
        print("\n📊 Model Evaluation")
        
        y_pred = self.model.predict(X_test)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))
        
        cm = confusion_matrix(y_test, y_pred)
        print("\nConfusion Matrix:")
        print(cm)
    
    def save_model(self):
        """
        Save social media model
        """
        print("\n💾 Saving model...")
        
        model_path = os.path.join(self.models_path, 'social_media_model.pkl')
        joblib.dump(self.model, model_path)
        
        scaler_path = os.path.join(self.models_path, 'social_media_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        
        print(f"✅ Model saved to: {model_path}")
    
    def run_training_pipeline(self):
        """
        Complete training pipeline
        """
        print("=" * 80)
        print("🚀 MULTILINGUAL SOCIAL MEDIA MODEL TRAINING")
        print("=" * 80)
        
        df = self.load_and_prepare_data()
        X, y = self.extract_features(df)
        X_test, y_test = self.train_model(X, y)
        self.evaluate_model(X_test, y_test)
        self.save_model()
        
        print("\n" + "=" * 80)
        print("✅ SOCIAL MEDIA MODEL TRAINING COMPLETE")
        print("=" * 80)


if __name__ == "__main__":
    trainer = MultilingualSocialMediaModelTrainer()
    trainer.run_training_pipeline()