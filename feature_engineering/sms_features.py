"""
Enhanced SMS Feature Engineering with Multilingual Support
Supports all Indian languages + Hinglish + Code-mixed text
"""

import os
import pandas as pd
import joblib
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from .multilingual_utils import MultilingualFeatureExtractor
from .language_detector import IndianLanguageDetector

# ============================================================================
# DYNAMIC PATH SETUP – replace absolute Windows paths
# ============================================================================
# Get the directory of the current file (feature_engineering/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the repository root
repo_root = os.path.dirname(current_dir)

# Construct paths relative to the repository root
DATA_PATH = os.path.join(repo_root, "data", "processed", "sms_preprocessed.csv")
FEATURE_PATH = current_dir   # where the vectorizers will be saved (same folder as this file)

class MultilingualSMSFeatureExtractor:
    """
    Enhanced SMS feature extractor with support for all Indian languages
    """
    
    def __init__(self):
        # Load preprocessed data
        self.df = pd.read_csv(DATA_PATH)
        self.df["clean_text"] = self.df["clean_text"].fillna("").astype(str)
        
        # Initialize multilingual utilities
        self.multilingual_utils = MultilingualFeatureExtractor()
        self.language_detector = IndianLanguageDetector()
        
        # SMS-specific patterns for Indian languages (unchanged)
        self.sms_scam_patterns = {
            'marathi': {
                'banking': ['बँक', 'खाते', 'एटीएम', 'पिन', 'ओटीपी', 'केवाईसी', 'बंद', 'अपडेट'],
                'prize': ['बक्षीस', 'लॉटरी', 'जिंकलात', 'पैसे', 'रक्कम', 'कूपन', 'ऑफर'],
                'govt': ['सरकार', 'पोलीस', 'कोर्ट', 'नोटीस', 'दंड', 'आधार', 'पॅन'],
                'urgent': ['तातडीचे', 'लगेच', 'आज', 'उद्या', 'शेवटची', 'बंद होणार']
            },
            'hindi': {
                'banking': ['बैंक', 'खाता', 'एटीएम', 'पिन', 'ओटीपी', 'केवाईसी', 'बंद', 'अपडेट'],
                'prize': ['इनाम', 'लॉटरी', 'जीत', 'पैसे', 'रकम', 'कूपन', 'ऑफर'],
                'govt': ['सरकार', 'पुलिस', 'कोर्ट', 'नोटिस', 'जुर्माना', 'आधार', 'पैन'],
                'urgent': ['तुरंत', 'अभी', 'आज', 'कल', 'आखिरी', 'बंद हो रहा']
            },
            'tamil': {
                'banking': ['வங்கி', 'கணக்கு', 'ஏடிஎம்', 'பின்', 'ஓடிபி', 'கேஒய்சி', 'மூடல்'],
                'prize': ['பரிசு', 'லாட்டரி', 'வெற்றி', 'பணம்', 'தொகை', 'கூப்பன்'],
                'govt': ['அரசு', 'போலீஸ்', 'நீதிமன்றம்', 'அறிவிப்பு', 'ஆதார்'],
                'urgent': ['அவசரம்', 'இப்போது', 'இன்று', 'நாளை', 'கடைசி']
            },
            'telugu': {
                'banking': ['బ్యాంక్', 'ఖాతా', 'ఏటీఎం', 'పిన్', 'ఓటిపి', 'కేవైసీ', 'మూసివేత'],
                'prize': ['బహుమతి', 'లాటరీ', 'గెలుపు', 'డబ్బు', 'మొత్తం', 'కూపన్'],
                'govt': ['ప్రభుత్వం', 'పోలీస్', 'కోర్ట్', 'నోటీసు', 'ఆధార్'],
                'urgent': ['అత్యవసరం', 'ఇప్పుడే', 'ఈరోజు', 'రేపు', 'చివరి']
            },
            'kannada': {
                'banking': ['ಬ್ಯಾಂಕ್', 'ಖಾತೆ', 'ಎಟಿಎಂ', 'ಪಿನ್', 'ಒಟಿಪಿ', 'ಕೆವೈಸಿ', 'ಮುಚ್ಚುವಿಕೆ'],
                'prize': ['ಬಹುಮಾನ', 'ಲಾಟರಿ', 'ಗೆಲುವು', 'ಹಣ', 'ಮೊತ್ತ', 'ಕೂಪನ್'],
                'govt': ['ಸರ್ಕಾರ', 'ಪೋಲೀಸ್', 'ಕೋರ್ಟ್', 'ಸೂಚನೆ', 'ಆಧಾರ್'],
                'urgent': ['ತುರ್ತು', 'ಈಗ', 'ಇಂದು', 'ನಾಳೆ', 'ಕೊನೆಯ']
            },
            'malayalam': {
                'banking': ['ബാങ്ക്', 'അക്കൗണ്ട്', 'എടിഎം', 'പിൻ', 'ഒടിപി', 'കെവൈസി', 'അടയ്ക്കൽ'],
                'prize': ['സമ്മാനം', 'ലോട്ടറി', 'വിജയം', 'പണം', 'തുക', 'കൂപ്പൺ'],
                'govt': ['സർക്കാർ', 'പോലീസ്', 'കോടതി', 'അറിയിപ്പ്', 'ആധാർ'],
                'urgent': ['അടിയന്തര', 'ഇപ്പോൾ', 'ഇന്ന്', 'നാളെ', 'അവസാന']
            },
            'gujarati': {
                'banking': ['બેંક', 'ખાતું', 'એટીએમ', 'પિન', 'ઓટીપી', 'કેવાયસી', 'બંધ'],
                'prize': ['ઇનામ', 'લોટરી', 'જીત', 'પૈસા', 'રકમ', 'કૂપન'],
                'govt': ['સરકાર', 'પોલીસ', 'કોર્ટ', 'નોટિસ', 'દંડ', 'આધાર'],
                'urgent': ['તાત્કાલિક', 'હમણાં', 'આજે', 'કાલે', 'છેલ્લી']
            },
            'bengali': {
                'banking': ['ব্যাঙ্ক', 'অ্যাকাউন্ট', 'এটিএম', 'পিন', 'ওটিপি', 'কেওয়াইসি', 'বন্ধ'],
                'prize': ['পুরস্কার', 'লটারি', 'জয়', 'টাকা', 'পরিমাণ', 'কুপন'],
                'govt': ['সরকার', 'পুলিশ', 'কোর্ট', 'নোটিশ', 'জরিমানা', 'আধার'],
                'urgent': ['জরুরি', 'এখনই', 'আজ', 'কাল', 'শেষ']
            },
            'punjabi': {
                'banking': ['ਬੈਂਕ', 'ਖਾਤਾ', 'ਏਟੀਐਮ', 'ਪਿੰਨ', 'ਓਟੀਪੀ', 'ਕੇਵਾਈਸੀ', 'ਬੰਦ'],
                'prize': ['ਇਨਾਮ', 'ਲਾਟਰੀ', 'ਜਿੱਤ', 'ਪੈਸੇ', 'ਰਕਮ', 'ਕੂਪਨ'],
                'govt': ['ਸਰਕਾਰ', 'ਪੁਲਿਸ', 'ਕੋਰਟ', 'ਨੋਟਿਸ', 'ਜੁਰਮਾਨਾ', 'ਆਧਾਰ'],
                'urgent': ['ਜ਼ਰੂਰੀ', 'ਹੁਣੇ', 'ਅੱਜ', 'ਕੱਲ੍ਹ', 'ਆਖਰੀ']
            }
        }
        
        # SMS-specific universal patterns (unchanged)
        self.sms_universal_patterns = {
            'short_urls': r'(bit\.ly|tinyurl|goo\.gl|t\.co|rb\.gy|ow\.ly|is\.gd|buff\.ly)',
            'free_keywords': r'\b(free|free|मुफ्त|मोफत|இலவச|ఉచిత|ಉಚಿತ|സൗജന്യ|મફત|ফ্রী|ਮੁਫ਼ਤ)\b',
            'winner_keywords': r'\b(win|won|winner|जीत|जिंकलात|வெற்றி|గెలుపు|ಗೆಲುವು|വിജയം|જીત|জয়|ਜਿੱਤ)\b',
            'claim_keywords': r'\b(claim|redeem|get now|पाएं|मिळवा|பெற|పొందండి|ಪಡೆಯಿರಿ|നേടുക|મેળવો|নিন|ਪ੍ਰਾਪਤ)\b',
            'otp_keywords': r'\b(otp|एकबारगी|ओटीपी|ஓடிபி|ఓటిపి|ಒಟಿಪಿ|ഒടിപി|ઓટીપી|ওটিপি|ਓਟੀਪੀ)\b',
            'kyc_keywords': r'\b(kyc|केवाईसी|கேஒய்சி|కేవైసీ|ಕೆವೈಸಿ|കെവൈസി|કેવાયસી|কেওয়াইসি|ਕੇਵਾਈਸੀ)\b'
        }
        
    def extract_sms_specific_features(self, text, detected_lang=None):
        """
        Extract SMS-specific features
        """
        features = {}
        
        if not text:
            return features
        
        text_lower = text.lower()
        
        # Check universal SMS patterns
        for pattern_name, pattern in self.sms_universal_patterns.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            features[f'sms_{pattern_name}_count'] = len(matches)
            features[f'sms_{pattern_name}_present'] = int(len(matches) > 0)
        
        # SMS structure features
        features['sms_has_question_mark'] = int('?' in text)
        features['sms_has_exclamation'] = int('!' in text)
        features['sms_has_multiple_punctuation'] = int(re.search(r'[!?]{2,}', text) is not None)
        
        # SMS length categories (common in spam)
        words = text.split()
        features['sms_word_count'] = len(words)
        features['sms_is_short'] = int(len(words) < 5)
        features['sms_is_long'] = int(len(words) > 50)
        
        # All caps words (shouting)
        all_caps_words = sum(1 for word in words if word.isupper() and len(word) > 2)
        features['sms_all_caps_count'] = all_caps_words
        features['sms_all_caps_ratio'] = all_caps_words / max(len(words), 1)
        
        return features
    
    def extract_all_features(self, text):
        """
        Extract ALL features for SMS fraud detection
        """
        features = {}
        
        # Get base multilingual features
        features.update(self.multilingual_utils.extract_all_features(text))
        
        # Add SMS-specific features
        detected_lang = features.get('detected_language', 'unknown')
        features.update(self.extract_sms_specific_features(text, detected_lang))
        
        return features
    
    def prepare_training_data(self):
        """
        Prepare feature matrix for model training
        """
        print("📊 Preparing multilingual SMS training data...")
        
        all_features = []
        labels = []
        
        for idx, row in self.df.iterrows():
            text = row['clean_text']
            label = row.get('label', 0)  # Assuming 'label' column exists
            
            # Extract features
            features = self.extract_all_features(text)
            
            # Flatten features into vector
            feature_vector = []
            for key, value in features.items():
                if isinstance(value, (int, float)):
                    feature_vector.append(value)
                elif isinstance(value, str):
                    # One-hot encode detected language
                    if key == 'detected_language':
                        for lang in ['hindi', 'marathi', 'tamil', 'telugu', 'kannada', 
                                   'malayalam', 'gujarati', 'bengali', 'punjabi', 'hinglish', 'english']:
                            feature_vector.append(1 if value == lang else 0)
            
            all_features.append(feature_vector)
            labels.append(label)
            
            if idx % 1000 == 0:
                print(f"  Processed {idx} messages...")
        
        # Convert to numpy arrays
        X = np.array(all_features)
        y = np.array(labels)
        
        print(f"✅ Training data prepared: {X.shape} features")
        return X, y
    
    def save_vectorizers(self):
        """
        Save multilingual vectorizers for inference
        """
        # Character-level vectorizer (language agnostic)
        char_vectorizer = TfidfVectorizer(
            analyzer='char',
            ngram_range=(2, 5),
            max_features=3000,
            lowercase=True
        )
        
        # Word-level vectorizer (for Latin script)
        word_vectorizer = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 3),
            max_features=2000,
            lowercase=True
        )
        
        # Fit on all texts
        print("🔄 Fitting multilingual vectorizers...")
        char_vectorizer.fit(self.df['clean_text'])
        word_vectorizer.fit(self.df['clean_text'])
        
        # Save both
        os.makedirs(FEATURE_PATH, exist_ok=True)
        joblib.dump(char_vectorizer, os.path.join(FEATURE_PATH, "sms_char_vectorizer.pkl"))
        joblib.dump(word_vectorizer, os.path.join(FEATURE_PATH, "sms_word_vectorizer.pkl"))
        
        # Also save language detector
        joblib.dump(self.language_detector, os.path.join(FEATURE_PATH, "sms_language_detector.pkl"))
        
        print("✅ SMS vectorizers saved successfully")
        print(f"   Character n-grams: {len(char_vectorizer.get_feature_names_out())}")
        print(f"   Word n-grams: {len(word_vectorizer.get_feature_names_out())}")
    
    def load_vectorizers(self):
        """
        Load saved vectorizers for inference
        """
        char_vectorizer = joblib.load(os.path.join(FEATURE_PATH, "sms_char_vectorizer.pkl"))
        word_vectorizer = joblib.load(os.path.join(FEATURE_PATH, "sms_word_vectorizer.pkl"))
        language_detector = joblib.load(os.path.join(FEATURE_PATH, "sms_language_detector.pkl"))
        
        return char_vectorizer, word_vectorizer, language_detector


# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("MULTILINGUAL SMS FEATURE ENGINEERING")
    print("=" * 80)
    
    # Initialize extractor
    extractor = MultilingualSMSFeatureExtractor()
    
    # Test on sample texts
    test_samples = [
        "तुमचे बँक खाते बंद होणार आहे. लगेच KYC अपडेट करा: bit.ly/bankupdate",
        "உங்கள் வங்கி கணக்கு மூடப்படும். உடனே OTP பகிரவும்",
        "Aapka bank account band ho raha hai. Turant OTP share karein",
        "Congratulations! You won ₹25 lakhs. Call now to claim",
        "আপনার ব্যাঙ্ক অ্যাকাউন্ট বন্ধ হয়ে যাবে। এখনই OTP শেয়ার করুন"
    ]
    
    print("\n🔍 TESTING FEATURE EXTRACTION:\n")
    
    for i, text in enumerate(test_samples, 1):
        print(f"Test {i}: {text[:80]}...")
        features = extractor.extract_all_features(text)
        
        # Show key features
        print(f"  Language: {features.get('detected_language', 'unknown')} "
              f"(conf: {features.get('language_confidence', 0):.2f})")
        print(f"  Code-mixed: {features.get('code_mixed', 0)}")
        print(f"  SMS patterns: "
              f"URL: {features.get('sms_short_urls_present', 0)}, "
              f"OTP: {features.get('sms_otp_keywords_present', 0)}, "
              f"KYC: {features.get('sms_kyc_keywords_present', 0)}")
        print(f"  Word count: {features.get('sms_word_count', 0)}")
        print("-" * 60)
    
    # Save vectorizers
    print("\n💾 Saving vectorizers...")
    extractor.save_vectorizers()
    
    print("\n✅ SMS feature engineering module ready!")
