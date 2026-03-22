# feature_engineering/multilingual_utils.py
"""
Shared multilingual utilities for ALL fraud detection modules
Provides common functions for feature extraction across languages
"""

import re
import numpy as np
from collections import Counter
from .language_detector import IndianLanguageDetector

class MultilingualFeatureExtractor:
    """
    Base class for multilingual feature extraction
    Used by ALL fraud type modules (SMS, Call, Crypto, Jobs, Social, Web)
    """
    
    def __init__(self):
        self.language_detector = IndianLanguageDetector()
        
        # Language-specific scam patterns for ALL Indian languages
        self.language_scam_patterns = {
            'marathi': {
                'banking': ['बँक', 'खाते', 'एटीएम', 'पिन', 'ओटीपी', 'केवाईसी'],
                'prize': ['बक्षीस', 'लॉटरी', 'जिंकलात', 'पैसे', 'रक्कम'],
                'govt': ['सरकार', 'पोलीस', 'कोर्ट', 'आधार', 'पॅन'],
                'urgent': ['तातडीचे', 'लगेच', 'आज', 'उद्या', 'बंद']
            },
            'hindi': {
                'banking': ['बैंक', 'खाता', 'एटीएम', 'पिन', 'ओटीपी', 'केवाईसी'],
                'prize': ['इनाम', 'लॉटरी', 'जीत', 'पैसे', 'रकम'],
                'govt': ['सरकार', 'पुलिस', 'कोर्ट', 'आधार', 'पैन'],
                'urgent': ['तुरंत', 'अभी', 'आज', 'कल', 'बंद']
            },
            'tamil': {
                'banking': ['வங்கி', 'கணக்கு', 'ஏடிஎம்', 'பின்', 'ஓடிபி'],
                'prize': ['பரிசு', 'லாட்டரி', 'வெற்றி', 'பணம்'],
                'govt': ['அரசு', 'போலீஸ்', 'நீதிமன்றம்', 'ஆதார்'],
                'urgent': ['அவசரம்', 'இப்போது', 'இன்று', 'நாளை']
            },
            'telugu': {
                'banking': ['బ్యాంక్', 'ఖాతా', 'ఏటీఎం', 'పిన్', 'ఓటిపి'],
                'prize': ['బహుమతి', 'లాటరీ', 'గెలుపు', 'డబ్బు'],
                'govt': ['ప్రభుత్వం', 'పోలీస్', 'కోర్ట్', 'ఆధార్'],
                'urgent': ['అత్యవసరం', 'ఇప్పుడే', 'ఈరోజు', 'రేపు']
            },
            'kannada': {
                'banking': ['ಬ್ಯಾಂಕ್', 'ಖಾತೆ', 'ಎಟಿಎಂ', 'ಪಿನ್', 'ಒಟಿಪಿ'],
                'prize': ['ಬಹುಮಾನ', 'ಲಾಟರಿ', 'ಗೆಲುವು', 'ಹಣ'],
                'govt': ['ಸರ್ಕಾರ', 'ಪೋಲೀಸ್', 'ಕೋರ್ಟ್', 'ಆಧಾರ್'],
                'urgent': ['ತುರ್ತು', 'ಈಗ', 'ಇಂದು', 'ನಾಳೆ']
            },
            'malayalam': {
                'banking': ['ബാങ്ക്', 'അക്കൗണ്ട്', 'എടിഎം', 'പിൻ', 'ഒടിപി'],
                'prize': ['സമ്മാനം', 'ലോട്ടറി', 'വിജയം', 'പണം'],
                'govt': ['സർക്കാർ', 'പോലീസ്', 'കോടതി', 'ആധാർ'],
                'urgent': ['അടിയന്തര', 'ഇപ്പോൾ', 'ഇന്ന്', 'നാളെ']
            },
            'gujarati': {
                'banking': ['બેંક', 'ખાતું', 'એટીએમ', 'પિન', 'ઓટીપી'],
                'prize': ['ઇનામ', 'લોટરી', 'જીત', 'પૈસા'],
                'govt': ['સરકાર', 'પોલીસ', 'કોર્ટ', 'આધાર'],
                'urgent': ['તાત્કાલિક', 'હમણાં', 'આજે', 'કાલે']
            },
            'bengali': {
                'banking': ['ব্যাঙ্ক', 'অ্যাকাউন্ট', 'এটিএম', 'পিন', 'ওটিপি'],
                'prize': ['পুরস্কার', 'লটারি', 'জয়', 'টাকা'],
                'govt': ['সরকার', 'পুলিশ', 'কোর্ট', 'আধার'],
                'urgent': ['জরুরি', 'এখনই', 'আজ', 'কাল']
            },
            'punjabi': {
                'banking': ['ਬੈਂਕ', 'ਖਾਤਾ', 'ਏਟੀਐਮ', 'ਪਿੰਨ', 'ਓਟੀਪੀ'],
                'prize': ['ਇਨਾਮ', 'ਲਾਟਰੀ', 'ਜਿੱਤ', 'ਪੈਸੇ'],
                'govt': ['ਸਰਕਾਰ', 'ਪੁਲਿਸ', 'ਕੋਰਟ', 'ਆਧਾਰ'],
                'urgent': ['ਜ਼ਰੂਰੀ', 'ਹੁਣੇ', 'ਅੱਜ', 'ਕੱਲ੍ਹ']
            }
        }
        
        # Universal scam indicators (across ALL languages)
        self.universal_indicators = {
            'phone_numbers': r'(\+?\d{1,3}[-.]?)?\(?\d{2,4}\)?[-.]?\d{3,4}[-.]?\d{4,10}',
            'indian_phone': r'(\+91|0)?[6-9]\d{9}',
            'indian_pincode': r'\b[1-9][0-9]{5}\b',
            'indian_aadhaar': r'\b[2-9]{1}[0-9]{11}\b',
            'indian_pan': r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
            'indian_voter': r'[A-Z]{3}[0-9]{7}',
            'urls': r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(com|in|org|net|bharat)',
            'short_urls': r'(bit\.ly|tinyurl|goo\.gl|t\.co|rb\.gy)',
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'money': r'(?:Rs\.?|₹|INR|रु|টাকা)\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            'indian_money': r'(\d+\s*(lakh|lac|cr|k|हजार|लाख|करोड़|లక్ష|కోటి|லட்சம்|கோடி))',
            'percentages': r'\d+\s*%|\d+\s*प्रतिशत|\d+\s*శాతం|\d+\s*சதவீதம்',
            'dates': r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+(जनवरी|फरवरी|मार्च|अप्रैल|मई|जून|जुलाई|अगस्त|सितंबर|अक्टूबर|नवंबर|दिसंबर)'
        }
        
    def extract_script_features(self, text):
        """
        Extract script-based features (works for any language)
        Returns dictionary of script-related features
        """
        features = {}
        
        if not text:
            return features
        
        # Detect language and script
        lang, conf, details = self.language_detector.detect_language(text)
        script = details.get('script', 'unknown') if isinstance(details, dict) else 'unknown'
        
        features['detected_language'] = lang
        features['language_confidence'] = conf
        features['detected_script'] = script
        
        # Count characters in each script (for code-mixing detection)
        for script_name in ['devanagari', 'tamil', 'telugu', 'kannada', 'malayalam', 
                           'gujarati', 'bengali', 'gurmukhi', 'oriya', 'latin']:
            count = 0
            if script_name == 'latin':
                count = sum(1 for c in text if 0x0041 <= ord(c.upper()) <= 0x005A)
            else:
                start, end = self.language_detector.script_ranges.get(script_name, (0, 0))
                if start and end:
                    count = sum(1 for c in text if start <= ord(c) <= end)
            
            features[f'script_{script_name}_count'] = count
            features[f'script_{script_name}_present'] = int(count > 0)
        
        # Code-mixing features
        scripts_present = sum(1 for k in features if k.endswith('_present') and features[k])
        features['code_mixed'] = int(scripts_present > 1)
        features['num_scripts'] = scripts_present
        
        # Text statistics (language agnostic)
        features['char_length'] = len(text)
        features['word_count'] = len(text.split())
        features['avg_word_length'] = features['char_length'] / max(features['word_count'], 1)
        
        return features
    
    def extract_character_ngrams(self, text, ngram_range=(2, 5), top_k=20):
        """
        Extract character n-grams - completely language agnostic
        Works for any language including code-mixed text
        """
        features = {}
        
        if not text or len(text) < 2:
            return features
        
        text_clean = text.lower()
        all_ngrams = []
        
        for n in range(ngram_range[0], ngram_range[1] + 1):
            ngrams = []
            for i in range(len(text_clean) - n + 1):
                ngram = text_clean[i:i+n]
                ngrams.append(ngram)
                all_ngrams.append(ngram)
            
            if ngrams:
                # Get most common n-grams of this length
                common = Counter(ngrams).most_common(min(top_k, len(ngrams)))
                for i, (ngram, count) in enumerate(common):
                    features[f'char_ngram_{n}_{i}'] = ngram
                    features[f'char_ngram_{n}_{i}_freq'] = count / max(len(text_clean), 1)
        
        # Overall statistics
        if all_ngrams:
            features['total_ngrams'] = len(all_ngrams)
            features['unique_ngrams'] = len(set(all_ngrams))
            features['ngram_diversity'] = features['unique_ngrams'] / max(features['total_ngrams'], 1)
        
        return features
    
    def extract_universal_patterns(self, text):
        """
        Extract patterns that work across ALL languages
        Uses regex patterns that are language independent
        """
        features = {}
        
        if not text:
            return features
        
        text_lower = text.lower()
        
        # Check for each universal indicator
        for indicator_name, pattern in self.universal_indicators.items():
            matches = re.findall(pattern, text_lower)
            features[f'universal_{indicator_name}_count'] = len(matches)
            features[f'universal_{indicator_name}_present'] = int(len(matches) > 0)
            
            # For money, also extract amounts
            if indicator_name == 'money' and matches:
                features['has_monetary_value'] = 1
        
        # Special indicators for Indian context
        features['has_indian_contact'] = int(features.get('universal_indian_phone_present', 0) or 
                                             features.get('universal_email_present', 0))
        features['has_suspicious_link'] = int(features.get('universal_short_urls_present', 0) or 
                                              features.get('universal_urls_present', 0))
        
        return features
    
    def extract_language_specific_scam_patterns(self, text, detected_lang=None):
        """
        Extract language-specific scam patterns
        If language not provided, auto-detect
        """
        features = {}
        
        if not text:
            return features
        
        # Auto-detect language if not provided
        if not detected_lang:
            detected_lang, conf, _ = self.language_detector.detect_language(text)
        
        # Get patterns for detected language
        lang_patterns = self.language_scam_patterns.get(detected_lang, {})
        
        if lang_patterns:
            for category, keywords in lang_patterns.items():
                matches = 0
                for keyword in keywords:
                    if keyword in text:
                        matches += 1
                features[f'{detected_lang}_{category}_score'] = matches / max(len(keywords), 1)
                features[f'{detected_lang}_{category}_present'] = int(matches > 0)
        
        return features
    
    def extract_numeric_features(self, text):
        """
        Extract numeric patterns (language independent)
        """
        features = {}
        
        if not text:
            return features
        
        # Basic digit features
        digits = [c for c in text if c.isdigit()]
        features['digit_count'] = len(digits)
        features['digit_ratio'] = len(digits) / max(len(text), 1)
        
        if len(digits) >= 10:
            features['has_phone_like'] = 1
        
        # Special characters
        special_chars = [c for c in text if not c.isalnum() and not c.isspace()]
        features['special_char_count'] = len(special_chars)
        features['special_char_ratio'] = len(special_chars) / max(len(text), 1)
        
        # Uppercase (for Latin script, but useful for emphasis in any language)
        uppercase = [c for c in text if c.isupper()]
        features['uppercase_count'] = len(uppercase)
        features['uppercase_ratio'] = len(uppercase) / max(len(text), 1)
        
        return features
    
    def extract_all_features(self, text):
        """
        Extract ALL multilingual features at once
        This is the main method to call from feature modules
        """
        features = {}
        
        # Extract all feature types
        features.update(self.extract_script_features(text))
        features.update(self.extract_character_ngrams(text))
        features.update(self.extract_universal_patterns(text))
        features.update(self.extract_numeric_features(text))
        
        # Extract language-specific patterns based on detected language
        detected_lang = features.get('detected_language', 'unknown')
        features.update(self.extract_language_specific_scam_patterns(text, detected_lang))
        
        return features
    
    def get_feature_names(self):
        """
        Get list of all possible feature names (for model training)
        """
        return [
            'detected_language', 'language_confidence', 'detected_script',
            'code_mixed', 'num_scripts', 'char_length', 'word_count', 'avg_word_length',
            'digit_count', 'digit_ratio', 'special_char_count', 'special_char_ratio',
            'uppercase_count', 'uppercase_ratio',
            'universal_phone_numbers_count', 'universal_indian_phone_present',
            'universal_indian_pincode_present', 'universal_indian_aadhaar_present',
            'universal_indian_pan_present', 'universal_urls_present',
            'universal_short_urls_present', 'universal_email_present',
            'universal_money_present', 'universal_indian_money_present',
            'has_indian_contact', 'has_suspicious_link'
        ]


# Test the extractor
if __name__ == "__main__":
    extractor = MultilingualFeatureExtractor()
    
    test_texts = [
        "तुमचे बँक खाते बंद होणार आहे. लगेच KYC अपडेट करा: bit.ly/fakebank",
        "உங்கள் வங்கி கணக்கு மூடப்படும். உடனே OTP பகிரவும்",
        "Aapka bank account band ho jayega. Turant OTP share karein 9876543210",
        "Your account will be closed. Call 1800-123-4567 immediately"
    ]
    
    print("=" * 80)
    print("MULTILINGUAL FEATURE EXTRACTION TEST")
    print("=" * 80)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. Text: {text[:80]}...")
        features = extractor.extract_all_features(text)
        
        print("   Key Features:")
        key_features = ['detected_language', 'language_confidence', 'detected_script', 
                       'code_mixed', 'num_scripts', 'char_length', 'digit_count']
        
        for feat in key_features:
            if feat in features:
                print(f"   - {feat}: {features[feat]}")
        
        print("-" * 80)