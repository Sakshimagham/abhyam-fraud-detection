"""
Enhanced Call Transcript Feature Engineering with Multilingual Support
Supports call analysis in all Indian languages
"""

import os
import pandas as pd
import joblib
import numpy as np
import re
from collections import Counter
from .multilingual_utils import MultilingualFeatureExtractor
from .language_detector import IndianLanguageDetector

# ============================================================================
# DYNAMIC PATH SETUP – replace absolute Windows paths
# ============================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
DATA_PATH = os.path.join(repo_root, "data", "processed", "call_data_cleaned.csv")
FEATURE_PATH = current_dir   # where scalers will be saved

class MultilingualCallFeatureExtractor:
    """
    Enhanced call transcript feature extractor with support for all Indian languages
    """
    
    def __init__(self):
        # Load call data
        if os.path.exists(DATA_PATH):
            self.df = pd.read_csv(DATA_PATH)
            # Handle missing values
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].fillna("")
        else:
            print(f"⚠️ Call data not found at {DATA_PATH}")
            self.df = pd.DataFrame()
        
        # Initialize multilingual utilities
        self.multilingual_utils = MultilingualFeatureExtractor()
        self.language_detector = IndianLanguageDetector()
        
        # Call-specific scam patterns for Indian languages (unchanged)
        self.call_scam_patterns = {
            'marathi': {
                'banking': ['बँक', 'खाते', 'केवाईसी', 'ओटीपी', 'क्रेडिट कार्ड', 'डेबिट कार्ड'],
                'govt': ['सरकार', 'पोलीस', 'आयकर', 'जीएसटी', 'आधार', 'पॅन कार्ड'],
                'prize': ['बक्षीस', 'लॉटरी', 'जिंकलात', 'पैसे', 'योजना'],
                'threats': ['अटक', 'केस', 'दंड', 'तुरुंग', 'नोटीस'],
                'urgency': ['ताबडतोब', 'लगेच', 'आजच', 'उद्या', 'शेवटची संधी']
            },
            'hindi': {
                'banking': ['बैंक', 'खाता', 'केवाईसी', 'ओटीपी', 'क्रेडिट कार्ड', 'डेबिट कार्ड'],
                'govt': ['सरकार', 'पुलिस', 'आयकर', 'जीएसटी', 'आधार', 'पैन कार्ड'],
                'prize': ['इनाम', 'लॉटरी', 'जीत', 'पैसे', 'योजना'],
                'threats': ['गिरफ्तारी', 'केस', 'जुर्माना', 'जेल', 'नोटिस'],
                'urgency': ['तुरंत', 'अभी', 'आज', 'कल', 'आखिरी मौका']
            },
            'tamil': {
                'banking': ['வங்கி', 'கணக்கு', 'கேஒய்சி', 'ஓடிபி', 'கிரெடிட் கார்டு'],
                'govt': ['அரசு', 'போலீஸ்', 'வருமான வரி', 'ஜிஎஸ்டி', 'ஆதார்'],
                'prize': ['பரிசு', 'லாட்டரி', 'வெற்றி', 'பணம்', 'திட்டம்'],
                'threats': ['கைது', 'வழக்கு', 'அபராதம்', 'சிறை', 'நோட்டீஸ்'],
                'urgency': ['அவசரம்', 'இப்போது', 'இன்று', 'நாளை', 'கடைசி வாய்ப்பு']
            },
            'telugu': {
                'banking': ['బ్యాంక్', 'ఖాతా', 'కేవైసీ', 'ఓటిపి', 'క్రెడిట్ కార్డ్'],
                'govt': ['ప్రభుత్వం', 'పోలీస్', 'ఆదాయపు పన్ను', 'జిఎస్టి', 'ఆధార్'],
                'prize': ['బహుమతి', 'లాటరీ', 'గెలుపు', 'డబ్బు', 'పథకం'],
                'threats': ['అరెస్టు', 'కేసు', 'జరిమానా', 'జైలు', 'నోటీసు'],
                'urgency': ['అత్యవసరం', 'ఇప్పుడే', 'ఈరోజు', 'రేపు', 'చివరి అవకాశం']
            }
        }
        
        # Common Indian call scam scenarios (unchanged)
        self.indian_scam_scenarios = [
            'digital_arrest',  # Digital arrest scam
            'kyc_expiry',      # KYC expiry scam
            'electricity_cut', # Electricity bill scam
            'fd_maturity',     # FD maturity scam
            'loan_approval',   # Loan approval scam
            'insurance_refund', # Insurance refund scam
            'relative_in_trouble', # Relative in trouble
            'prize_money',     # Prize money scam
            'govt_scheme',     # Government scheme scam
            'job_offer'        # Fake job offer
        ]
        
        # Scenario keywords in multiple languages (unchanged)
        self.scenario_keywords = {
            'digital_arrest': {
                'marathi': ['अटक', 'पोलीस', 'केस', 'कोर्ट', 'वॉरंट'],
                'hindi': ['गिरफ्तारी', 'पुलिस', 'केस', 'कोर्ट', 'वारंट'],
                'tamil': ['கைது', 'போலீஸ்', 'வழக்கு', 'நீதிமன்றம்', 'வாரண்ட்'],
                'english': ['arrest', 'police', 'case', 'court', 'warrant']
            },
            'kyc_expiry': {
                'marathi': ['केवाईसी', 'बँक', 'खाते', 'बंद', 'अपडेट'],
                'hindi': ['केवाईसी', 'बैंक', 'खाता', 'बंद', 'अपडेट'],
                'tamil': ['கேஒய்சி', 'வங்கி', 'கணக்கு', 'மூடல்', 'புதுப்பிப்பு'],
                'english': ['kyc', 'bank', 'account', 'close', 'update']
            },
            'electricity_cut': {
                'marathi': ['वीज', 'बिल', 'कनेक्शन', 'कापणार', 'बकाया'],
                'hindi': ['बिजली', 'बिल', 'कनेक्शन', 'काटेंगे', 'बकाया'],
                'tamil': ['மின்சாரம்', 'பில்', 'இணைப்பு', 'துண்டிப்பு', 'நிலுவை'],
                'english': ['electricity', 'bill', 'connection', 'cut', 'due']
            }
        }
    
    def extract_call_specific_features(self, transcript, duration=None, caller_id=None):
        """
        Extract call-specific features from transcript
        """
        features = {}
        
        if not transcript:
            return features
        
        # Basic call metrics
        features['call_word_count'] = len(transcript.split())
        features['call_character_count'] = len(transcript)
        
        # Turn-taking features (if transcript has speaker labels)
        turns = transcript.split('\n')
        speaker_turns = [t for t in turns if ':' in t]
        features['call_num_turns'] = len(speaker_turns)
        
        # Caller speech ratio (if we can identify caller/callee)
        caller_words = 0
        callee_words = 0
        for turn in speaker_turns:
            if 'caller' in turn.lower() or 'agent' in turn.lower():
                caller_words += len(turn.split())
            else:
                callee_words += len(turn.split())
        
        total_words = caller_words + callee_words
        if total_words > 0:
            features['call_caller_speech_ratio'] = caller_words / total_words
            features['call_callee_speech_ratio'] = callee_words / total_words
        
        # Question count (scammers ask many questions)
        features['call_question_count'] = transcript.count('?')
        features['call_question_density'] = transcript.count('?') / max(len(transcript.split()), 1)
        
        # Exclamation count (scammers use urgency)
        features['call_exclamation_count'] = transcript.count('!')
        
        # Pause indicators (scammers wait for victim to speak)
        features['call_pause_indicators'] = int('...' in transcript or 'pause' in transcript.lower())
        
        # Call duration if available
        if duration:
            features['call_duration_seconds'] = duration
            features['call_is_long'] = int(duration > 300)  # >5 minutes suspicious
        
        # Caller ID features
        if caller_id:
            features['call_has_caller_id'] = 1
            # Check for international numbers
            features['call_is_international'] = int('+' in caller_id and '+91' not in caller_id)
        else:
            features['call_has_caller_id'] = 0
            features['call_is_international'] = 0
        
        return features
    
    def detect_scam_scenario(self, text, detected_lang='english'):
        """
        Detect which scam scenario matches the call
        """
        features = {}
        text_lower = text.lower()
        
        for scenario in self.indian_scam_scenarios:
            scenario_matches = 0
            total_keywords = 0
            
            # Check keywords in multiple languages
            for lang, keywords in self.scenario_keywords.get(scenario, {}).items():
                total_keywords += len(keywords)
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        scenario_matches += 1
                    
                    # Also check in original script if language matches
                    if lang == detected_lang and keyword in text:
                        scenario_matches += 2  # Extra weight for native script
            
            if total_keywords > 0:
                features[f'scenario_{scenario}_score'] = scenario_matches / total_keywords
                features[f'scenario_{scenario}_present'] = int(scenario_matches > 2)
        
        return features
    
    def extract_all_features(self, transcript, duration=None, caller_id=None):
        """
        Extract ALL features for call fraud detection
        """
        features = {}
        
        # Get base multilingual features
        features.update(self.multilingual_utils.extract_all_features(transcript))
        
        # Add call-specific features
        features.update(self.extract_call_specific_features(transcript, duration, caller_id))
        
        # Detect scam scenario
        detected_lang = features.get('detected_language', 'english')
        features.update(self.detect_scam_scenario(transcript, detected_lang))
        
        return features
    
    def prepare_training_data(self):
        """
        Prepare feature matrix for model training
        """
        if self.df.empty:
            print("⚠️ No call data available for training")
            return np.array([]), np.array([])
        
        print("📊 Preparing multilingual call training data...")
        
        all_features = []
        labels = []
        
        for idx, row in self.df.iterrows():
            transcript = row.get('transcript', '')
            label = row.get('label', 0)
            duration = row.get('duration', None)
            caller_id = row.get('caller_id', None)
            
            if not transcript:
                continue
            
            # Extract features
            features = self.extract_all_features(transcript, duration, caller_id)
            
            # Flatten features into vector
            feature_vector = []
            for key, value in features.items():
                if isinstance(value, (int, float)):
                    feature_vector.append(value)
            
            all_features.append(feature_vector)
            labels.append(label)
            
            if idx % 100 == 0:
                print(f"  Processed {idx} calls...")
        
        if all_features:
            X = np.array(all_features)
            y = np.array(labels)
            print(f"✅ Call training data prepared: {X.shape}")
            return X, y
        else:
            print("⚠️ No features extracted from call data")
            return np.array([]), np.array([])
    
    def save_scaler(self):
        """
        Save feature scaler for call features
        """
        from sklearn.preprocessing import StandardScaler
        
        # Prepare features for scaling
        X, _ = self.prepare_training_data()
        
        if X.size > 0:
            scaler = StandardScaler()
            scaler.fit(X)
            
            os.makedirs(FEATURE_PATH, exist_ok=True)
            joblib.dump(scaler, os.path.join(FEATURE_PATH, "call_scaler.pkl"))
            
            # Also save language detector
            joblib.dump(self.language_detector, os.path.join(FEATURE_PATH, "call_language_detector.pkl"))
            
            print("✅ Call scaler saved successfully")
        else:
            print("⚠️ No data to fit scaler")


# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("MULTILINGUAL CALL FEATURE ENGINEERING")
    print("=" * 80)
    
    # Initialize extractor
    extractor = MultilingualCallFeatureExtractor()
    
    # Test on sample transcripts
    test_transcripts = [
        {
            'transcript': "Caller: नमस्कार, मी SBI बँकेतून बोलतोय. तुमचे खाते बंद होणार आहे. ताबडतोब OTP द्या.\nPerson: पण मी तर OTP दिला नाही.\nCaller: नाही दिलात तर खाते बंद होईल. लगेच द्या.",
            'duration': 120,
            'caller_id': '+91234567890'
        },
        {
            'transcript': "Caller: Hello, I'm calling from Income Tax department. There's a case against you. Pay immediately to avoid arrest.",
            'duration': 180,
            'caller_id': 'unknown'
        },
        {
            'transcript': "Caller: உங்கள் வங்கி கணக்கு மூடப்படும். உடனே OTP பகிரவும்.\nPerson: நான் வங்கிக்கு போகிறேன்.\nCaller: இல்லை, இப்போதே OTP வேண்டும்.",
            'duration': 90,
            'caller_id': '+918765432109'
        }
    ]
    
    print("\n🔍 TESTING CALL FEATURE EXTRACTION:\n")
    
    for i, test in enumerate(test_transcripts, 1):
        print(f"Test Call {i}:")
        features = extractor.extract_all_features(
            test['transcript'], 
            test['duration'], 
            test['caller_id']
        )
        
        # Show key features
        print(f"  Language: {features.get('detected_language', 'unknown')} "
              f"(conf: {features.get('language_confidence', 0):.2f})")
        print(f"  Call duration: {test['duration']}s")
        print(f"  Turns: {features.get('call_num_turns', 0)}")
        print(f"  Questions: {features.get('call_question_count', 0)}")
        print(f"  Scenarios detected: ", end="")
        for scenario in ['digital_arrest', 'kyc_expiry', 'electricity_cut']:
            if features.get(f'scenario_{scenario}_present', 0):
                print(f"{scenario} ", end="")
        print("\n" + "-" * 60)
    
    # Save scaler if data exists
    print("\n💾 Saving scaler...")
    extractor.save_scaler()
    
    print("\n✅ Call feature engineering module ready!")
