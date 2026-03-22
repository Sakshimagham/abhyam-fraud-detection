# models/train_sms_model.py
"""
Train SMS Fraud Detection Model with Multilingual Support
Trains on data from multiple Indian languages
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feature_engineering.feature_router import get_feature_router
from feature_engineering.sms_features import MultilingualSMSFeatureExtractor
from risk_engine.rule_engine import MultilingualRuleEngine

class MultilingualSMSModelTrainer:
    """
    Trains SMS fraud detection model with multilingual support
    """
    
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_path, "data", "processed", "sms_preprocessed.csv")
        self.models_path = os.path.join(self.base_path, "models")
        self.feature_path = os.path.join(self.base_path, "feature_engineering")
        
        # Create directories if they don't exist
        os.makedirs(self.models_path, exist_ok=True)
        
        # Initialize components
        self.router = get_feature_router()
        self.extractor = MultilingualSMSFeatureExtractor()
        self.rule_engine = MultilingualRuleEngine()
        
        # Model configurations
        self.models = {}
        self.scaler = None
        self.best_model = None
        self.feature_names = []  # will hold the list of numeric column names
        
        print("🚀 Multilingual SMS Model Trainer Initialized")
    
    def load_and_prepare_data(self):
        """
        Load SMS data and prepare features
        """
        print("\n📊 Loading SMS data...")
        
        if not os.path.exists(self.data_path):
            print(f"❌ Data file not found: {self.data_path}")
            return None, None
        
        # Load data
        df = pd.read_csv(self.data_path)
        print(f"✅ Loaded {len(df)} SMS messages")
        
        # Handle missing values
        df['clean_text'] = df['clean_text'].fillna('').astype(str)
        
        # Check language distribution (sample)
        languages = []
        for text in df['clean_text'].head(100):
            lang_info = self.router.detect_language(text)
            languages.append(lang_info['language'])
        
        print(f"\n🌐 Sample Language Distribution:")
        lang_counts = pd.Series(languages).value_counts()
        for lang, count in lang_counts.items():
            print(f"  {lang}: {count}")
        
        return df
    
    def extract_features(self, df):
        """
        Extract multilingual features from SMS data
        """
        print("\n🔍 Extracting multilingual features...")
        
        all_features = []  # list of dicts
        y_list = []
        language_stats = {}
        
        for idx, row in df.iterrows():
            text = row['clean_text']
            label = row.get('label', row.get('class', 0))
            
            # Extract features using router (returns dict)
            features = self.router.extract_features('sms', {'text': text})
            
            # Track language statistics
            lang = features.get('detected_language', 'unknown')
            language_stats[lang] = language_stats.get(lang, 0) + 1
            
            all_features.append(features)
            y_list.append(label)
            
            if (idx + 1) % 1000 == 0:
                print(f"  Processed {idx + 1}/{len(df)} messages...")
        
        # Convert list of dicts to DataFrame
        df_features = pd.DataFrame(all_features)
        
        # Fill NaN with 0 and keep only numeric columns
        df_features = df_features.fillna(0)
        numeric_cols = df_features.select_dtypes(include=[np.number]).columns
        self.feature_names = list(numeric_cols)  # store for later use
        X = df_features[numeric_cols].values
        y = np.array(y_list)
        
        print(f"\n✅ Extracted features: {X.shape}")
        print(f"\n🌐 Language Distribution in Dataset:")
        for lang, count in sorted(language_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {lang}: {count} ({count/len(df)*100:.1f}%)")
        
        return X, y
    
    def train_models(self, X, y):
        """
        Train multiple models and select best
        """
        print("\n🎯 Training multiple models...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Compute sample weights for balanced training
        classes = np.unique(y_train)
        weights = compute_class_weight('balanced', classes=classes, y=y_train)
        sample_weights = np.array([weights[0] if yi == classes[0] else weights[1] for yi in y_train])
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define models to try
        models_to_try = {
            'logistic_regression': LogisticRegression(
                max_iter=1000, 
                class_weight='balanced',
                random_state=42
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=20,
                min_samples_split=5,
                class_weight='balanced',
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=200,
                max_depth=10,
                learning_rate=0.1,
                random_state=42
            ),
            'xgboost': xgb.XGBClassifier(
                n_estimators=200,
                max_depth=10,
                learning_rate=0.1,
                scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
                random_state=42,
                n_jobs=-1
            ),
            'svm': SVC(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                class_weight='balanced',
                probability=True,
                random_state=42
            )
        }
        
        results = {}
        
        for name, model in models_to_try.items():
            print(f"\n  Training {name}...")
            
            # Train model with sample weights if supported
            if name in ['random_forest', 'gradient_boosting']:
                model.fit(X_train_scaled, y_train, sample_weight=sample_weights)
            elif name == 'xgboost':
                # scale_pos_weight already set in constructor
                model.fit(X_train_scaled, y_train)
            else:
                model.fit(X_train_scaled, y_train)
            
            # Predictions
            y_pred = model.predict(X_test_scaled)
            
            # Metrics
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            # Cross-validation (use sample weights for CV if possible)
            try:
                cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='f1_weighted')
                cv_mean = cv_scores.mean()
                cv_std = cv_scores.std()
            except:
                cv_mean, cv_std = 0, 0
            
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'f1_score': f1,
                'cv_mean': cv_mean,
                'cv_std': cv_std
            }
            
            print(f"    Accuracy: {accuracy:.4f}")
            print(f"    F1 Score: {f1:.4f}")
            print(f"    CV Score: {cv_mean:.4f} (+/- {cv_std:.4f})")
        
        # Select best model based on F1 score
        best_name = max(results, key=lambda x: results[x]['f1_score'])
        self.best_model = results[best_name]['model']
        
        print(f"\n✅ Best Model: {best_name}")
        print(f"  F1 Score: {results[best_name]['f1_score']:.4f}")
        print(f"  Accuracy: {results[best_name]['accuracy']:.4f}")
        
        # Create ensemble of top 3 models
        top_models = sorted(results.items(), key=lambda x: x[1]['f1_score'], reverse=True)[:3]
        ensemble_estimators = [(name, results[name]['model']) for name, _ in top_models]
        
        if len(ensemble_estimators) > 1:
            ensemble = VotingClassifier(
                estimators=ensemble_estimators,
                voting='soft',
                weights=[3, 2, 1]  # Weight by performance
            )
            ensemble.fit(X_train_scaled, y_train)
            y_pred_ensemble = ensemble.predict(X_test_scaled)
            ensemble_f1 = f1_score(y_test, y_pred_ensemble, average='weighted')
            
            print(f"\n🎯 Ensemble Model F1 Score: {ensemble_f1:.4f}")
            
            if ensemble_f1 > results[best_name]['f1_score']:
                self.best_model = ensemble
                print("✅ Using Ensemble Model as Best")
        
        # Store all models for potential use
        self.models = results
        
        return X_test_scaled, y_test
    
    def evaluate_model(self, X_test, y_test):
        """
        Detailed evaluation of best model
        """
        print("\n📊 Detailed Model Evaluation")
        print("-" * 50)
        
        # Predictions
        y_pred = self.best_model.predict(X_test)
        y_prob = self.best_model.predict_proba(X_test)
        
        # Classification Report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraud']))
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print("\nConfusion Matrix:")
        print(f"  True Negatives: {cm[0,0]:4d}  False Positives: {cm[0,1]:4d}")
        print(f"  False Negatives: {cm[1,0]:4d}  True Positives: {cm[1,1]:4d}")
        
        # Calculate metrics
        tn, fp, fn, tp = cm.ravel()
        
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"\n📈 Key Metrics:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1 Score:  {f1:.4f}")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm
        }
    
    def hyperparameter_tuning(self, X_train, y_train):
        """
        Hyperparameter tuning for best model
        """
        print("\n🔧 Hyperparameter Tuning...")
        
        # Define parameter grid based on best model type
        if isinstance(self.best_model, RandomForestClassifier):
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            model = RandomForestClassifier(random_state=42, n_jobs=-1, class_weight='balanced')
            
        elif isinstance(self.best_model, xgb.XGBClassifier):
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [6, 8, 10],
                'learning_rate': [0.05, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0]
            }
            scale_pos = (y_train == 0).sum() / (y_train == 1).sum()
            model = xgb.XGBClassifier(random_state=42, n_jobs=-1, scale_pos_weight=scale_pos)
            
        else:
            print("  Skipping tuning for non-tree model")
            return self.best_model
        
        # Grid search
        grid_search = GridSearchCV(
            model, param_grid, cv=3, scoring='f1_weighted',
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"\n✅ Best Parameters: {grid_search.best_params_}")
        print(f"   Best Score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def save_model(self):
        """
        Save trained model and associated files
        """
        print("\n💾 Saving model...")
        
        # Save model
        model_path = os.path.join(self.models_path, 'sms_model.pkl')
        joblib.dump(self.best_model, model_path)
        print(f"✅ Model saved to: {model_path}")
        
        # Save scaler
        scaler_path = os.path.join(self.models_path, 'sms_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        print(f"✅ Scaler saved to: {scaler_path}")
        
        # Save feature names (used for aligning vectors in inference)
        feature_names_path = os.path.join(self.models_path, 'sms_feature_names.pkl')
        joblib.dump(self.feature_names, feature_names_path)
        print(f"✅ Feature names saved to: {feature_names_path}")
        
        # Save model metadata
        metadata = {
            'model_type': type(self.best_model).__name__,
            'features': 'multilingual_sms_features',
            'languages_supported': self.router.get_supported_languages(),
            'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'feature_dimension': self.best_model.n_features_in_ if hasattr(self.best_model, 'n_features_in_') else None
        }
        
        metadata_path = os.path.join(self.models_path, 'sms_model_metadata.json')
        pd.Series(metadata).to_json(metadata_path)
        print(f"✅ Metadata saved to: {metadata_path}")
    
    def test_with_examples(self):
        """
        Test model with real examples in different languages
        Uses saved feature names to align feature vectors.
        """
        print("\n🧪 Testing with multilingual examples")
        print("-" * 50)
        
        # Load feature names (must exist; if not, fallback to using get_feature_vector directly)
        feature_names_path = os.path.join(self.models_path, 'sms_feature_names.pkl')
        if os.path.exists(feature_names_path):
            feature_names = joblib.load(feature_names_path)
            use_alignment = True
        else:
            print("⚠️ Feature names file not found, using raw feature vector (may cause dimension mismatch)")
            use_alignment = False
        
        test_examples = [
            {
                'text': 'तुमचे बँक खाते बंद होणार आहे. लगेच KYC अपडेट करा: bit.ly/bankupdate',
                'expected': 1,
                'language': 'marathi'
            },
            {
                'text': 'Aapka bank account band ho raha hai. Turant OTP share karein',
                'expected': 1,
                'language': 'hinglish'
            },
            {
                'text': 'உங்கள் வங்கி கணக்கு மூடப்படும். உடனே OTP பகிரவும்',
                'expected': 1,
                'language': 'tamil'
            },
            {
                'text': 'Your Amazon order has been delivered. Track at amazon.com/track',
                'expected': 0,
                'language': 'english'
            },
            {
                'text': 'మీ బ్యాంక్ ఖాతా మూసివేయబడుతుంది. వెంటనే OTP షేర్ చేయండి',
                'expected': 1,
                'language': 'telugu'
            },
            {
                'text': 'नमस्कार, कालच्या मीटिंगचे मिनिट्स पाठवले आहेत. कृपया तपासून सांगा',
                'expected': 0,
                'language': 'marathi'
            }
        ]
        
        for i, example in enumerate(test_examples, 1):
            # Extract features dict
            features_dict = self.router.extract_features('sms', {'text': example['text']})
            
            if use_alignment:
                # Create a DataFrame row with the same columns as training
                row_df = pd.DataFrame([features_dict])
                # Fill missing columns with 0 and ensure column order matches training
                row_df = row_df.reindex(columns=feature_names, fill_value=0)
                feature_vector = row_df.values.astype(float)
            else:
                # Fallback to old method (may fail if dimension mismatch)
                feature_vector = self.router.get_feature_vector('sms', {'text': example['text']}, model_type='ml')
                feature_vector = feature_vector.reshape(1, -1)
            
            # Scale
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            # Predict
            pred = self.best_model.predict(feature_vector_scaled)[0]
            prob = self.best_model.predict_proba(feature_vector_scaled)[0]
            
            # Get rule engine score
            rule_score, reasons, helplines, _, _= self.rule_engine.sms_rules(
                example['text'], detected_lang=example['language']
            )
            
            status = "✅ PASS" if pred == example['expected'] else "❌ FAIL"
            
            print(f"\n{i}. [{example['language']}] {status}")
            print(f"   Text: {example['text'][:80]}...")
            print(f"   Expected: {'Fraud' if example['expected'] else 'Legitimate'}")
            print(f"   Predicted: {'FRAUD' if pred else 'LEGITIMATE'} (prob: {prob[pred]:.3f})")
            print(f"   Rule Score: {rule_score}")
            if reasons:
                print(f"   Reasons: {len(reasons)} flags")
    
    def run_training_pipeline(self):
        """
        Complete training pipeline
        """
        print("=" * 80)
        print("🚀 MULTILINGUAL SMS MODEL TRAINING PIPELINE")
        print("=" * 80)
        
        # Step 1: Load data
        df = self.load_and_prepare_data()
        if df is None:
            return
        
        # Step 2: Extract features
        X, y = self.extract_features(df)
        
        if len(X) == 0:
            print("❌ No features extracted")
            return
        
        # Step 3: Train models
        X_test, y_test = self.train_models(X, y)
        
        # Step 4: Evaluate
        metrics = self.evaluate_model(X_test, y_test)
        
        # Step 5: Hyperparameter tuning (optional)
        # X_train, y_train = train_test_split(X, y, test_size=0.2, random_state=42)[:2]
        # self.best_model = self.hyperparameter_tuning(X_train, y_train)
        
        # Step 6: Save model
        self.save_model()
        
        # Step 7: Test with examples
        self.test_with_examples()
        
        print("\n" + "=" * 80)
        print("✅ SMS MODEL TRAINING COMPLETE")
        print("=" * 80)
        
        return self.best_model


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    trainer = MultilingualSMSModelTrainer()
    model = trainer.run_training_pipeline()