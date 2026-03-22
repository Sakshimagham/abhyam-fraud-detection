# models/train_crypto_model.py
"""
Train Cryptocurrency Fraud Detection Model with Multilingual Support
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
from feature_engineering.crypto_features import MultilingualCryptoFeatureExtractor
from risk_engine.rule_engine import MultilingualRuleEngine

class MultilingualCryptoModelTrainer:
    """
    Trains crypto fraud detection model with multilingual support
    """
    
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_path, "data", "processed", "crypto_fraud_preprocessed.csv")
        self.models_path = os.path.join(self.base_path, "models")
        
        os.makedirs(self.models_path, exist_ok=True)
        
        self.router = get_feature_router()
        self.extractor = MultilingualCryptoFeatureExtractor()
        self.rule_engine = MultilingualRuleEngine()
        
        self.model = None
        self.scaler = None
        
        print("🚀 Multilingual Crypto Model Trainer Initialized")
    
    def load_and_prepare_data(self):
        """
        Load crypto fraud data
        """
        print("\n📊 Loading crypto data...")
        
        if not os.path.exists(self.data_path):
            print("⚠️ Creating sample crypto data...")
            sample_data = {
                'text': [
                    "बिटकॉइन में निवेश करें और 1 महीने में पैसे दोगुने करें",
                    "உங்கள் பணத்தை இரட்டிப்பாக்குங்கள்! பிட்காயின் முதலீடு",
                    "Double your Bitcoin in 24 hours! Guaranteed returns",
                    "మీ బిట్కాయిన్ డబ్బును రెట్టింపు చేసుకోండి",
                    "Crypto mining investment - earn 10% daily",
                    "Join our WhatsApp group for crypto signals",
                    "Official Bitcoin exchange - low fees",
                    "ತುರ್ತು ಕ್ರಿಪ್ಟೋ ಹೂಡಿಕೆ ಅವಕಾಶ"
                ],
                'url': [
                    'bit.ly/btc-double',
                    'crypto-guru.xyz',
                    'bitcoin-invest.com',
                    'క్రిప్టో-ట్రేడ్.in',
                    'mining-pro.com',
                    'whatsapp.com/invite/crypto',
                    'binance.com',
                    'bitcoin-guru.top'
                ],
                'label': [1, 1, 1, 1, 1, 1, 0, 1]
            }
            df = pd.DataFrame(sample_data)
            print("✅ Created sample data with 8 entries")
        else:
            df = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(df)} entries")
        
        df['text'] = df['text'].fillna('')
        df['url'] = df['url'].fillna('')
        
        return df
    
    def extract_features(self, df):
        """
        Extract multilingual features from crypto data
        """
        print("\n🔍 Extracting crypto features...")
        
        X_list = []
        y_list = []
        
        for idx, row in df.iterrows():
            crypto_data = {
                'text': row['text'],
                'url': row['url']
            }
            
            features = self.router.extract_features('crypto', crypto_data)
            feature_vector = self.router.get_feature_vector('crypto', crypto_data, model_type='ml')
            
            X_list.append(feature_vector)
            y_list.append(row['label'])
            
            if (idx + 1) % 10 == 0:
                print(f"  Processed {idx + 1}/{len(df)} entries...")
        
        X = np.array(X_list)
        y = np.array(y_list)
        
        print(f"\n✅ Extracted features: {X.shape}")
        return X, y
    
    def train_model(self, X, y):
        """
        Train crypto fraud model
        """
        print("\n🎯 Training crypto model...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Use XGBoost for crypto (handles imbalanced data well)
        self.model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.1,
            scale_pos_weight=(len(y) - sum(y)) / sum(y),
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
        Evaluate crypto model
        """
        print("\n📊 Model Evaluation")
        
        y_pred = self.model.predict(X_test)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraud']))
        
        cm = confusion_matrix(y_test, y_pred)
        print("\nConfusion Matrix:")
        print(cm)
    
    def save_model(self):
        """
        Save crypto model
        """
        print("\n💾 Saving model...")
        
        model_path = os.path.join(self.models_path, 'crypto_model.pkl')
        joblib.dump(self.model, model_path)
        
        scaler_path = os.path.join(self.models_path, 'crypto_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        
        print(f"✅ Model saved to: {model_path}")
    
    def run_training_pipeline(self):
        """
        Complete training pipeline
        """
        print("=" * 80)
        print("🚀 MULTILINGUAL CRYPTO MODEL TRAINING")
        print("=" * 80)
        
        df = self.load_and_prepare_data()
        X, y = self.extract_features(df)
        X_test, y_test = self.train_model(X, y)
        self.evaluate_model(X_test, y_test)
        self.save_model()
        
        print("\n" + "=" * 80)
        print("✅ CRYPTO MODEL TRAINING COMPLETE")
        print("=" * 80)


if __name__ == "__main__":
    trainer = MultilingualCryptoModelTrainer()
    trainer.run_training_pipeline()