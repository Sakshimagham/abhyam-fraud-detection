# feature_engineering/language_detector.py
"""
Universal Language Detector for Indian Languages
Detects 22 official Indian languages without ML - using script ranges and patterns
"""

import re
from collections import Counter

class IndianLanguageDetector:
    """
    Detect Indian languages from text without using ML models
    Supports all 22 official Indian languages + English + Hinglish
    """
    
    def __init__(self):
        # Unicode ranges for Indian scripts
        self.script_ranges = {
            'devanagari': (0x0900, 0x097F),   # Hindi, Marathi, Sanskrit, Konkani
            'bengali': (0x0980, 0x09FF),      # Bengali, Assamese
            'gurmukhi': (0x0A00, 0x0A7F),     # Punjabi
            'gujarati': (0x0A80, 0x0AFF),     # Gujarati
            'oriya': (0x0B00, 0x0B7F),        # Odia
            'tamil': (0x0B80, 0x0BFF),        # Tamil
            'telugu': (0x0C00, 0x0C7F),       # Telugu
            'kannada': (0x0C80, 0x0CFF),      # Kannada
            'malayalam': (0x0D00, 0x0D7F),    # Malayalam
            'sinhala': (0x0D80, 0x0DFF),      # Sinhala
            'thai': (0x0E00, 0x0E7F),         # Thai (for border areas)
            'lao': (0x0E80, 0x0EFF),          # Lao
            'tibetan': (0x0F00, 0x0FFF),      # Tibetan (Ladakh, Sikkim)
            'myanmar': (0x1000, 0x109F),      # Myanmar (border areas)
            'georgian': (0x10A0, 0x10FF),     # Georgian
            'hangul': (0xAC00, 0xD7AF),       # Korean (for Manipur)
            'ethiopic': (0x1200, 0x137F),     # Ethiopic
            'cherokee': (0x13A0, 0x13FF),     # Cherokee
            'canadian_aboriginal': (0x1400, 0x167F),  # Canadian Aboriginal
            'ogham': (0x1680, 0x169F),        # Ogham
            'runic': (0x16A0, 0x16FF),        # Runic
            'khmer': (0x1780, 0x17FF),        # Khmer
        }
        
        # Language-specific indicators (common words in each language)
        self.language_indicators = {
            'hindi': {
                'script': 'devanagari',
                'words': ['है', 'का', 'की', 'के', 'में', 'पर', 'से', 'को', 'यह', 'वह'],
                'scam_words': ['बैंक', 'खाता', 'ओटीपी', 'केवाईसी', 'लॉटरी', 'इनाम']
            },
            'marathi': {
                'script': 'devanagari',
                'words': ['आहे', 'होते', 'करा', 'मिळाले', 'तुमचे', 'आमचे', 'साठी'],
                'scam_words': ['बँक', 'खाते', 'पैसे', 'कर्ज', 'बक्षीस', 'लॉटरी']
            },
            'tamil': {
                'script': 'tamil',
                'words': ['உங்கள்', 'எனது', 'இது', 'அது', 'இங்கே', 'அங்கே'],
                'scam_words': ['வங்கி', 'கணக்கு', 'ஓடிபி', 'பரிசு', 'பணம்']
            },
            'telugu': {
                'script': 'telugu',
                'words': ['మీ', 'నా', 'ఈ', 'ఆ', 'ఇక్కడ', 'అక్కడ'],
                'scam_words': ['బ్యాంక్', 'ఖాతా', 'ఓటిపి', 'బహుమతి', 'డబ్బు']
            },
            'kannada': {
                'script': 'kannada',
                'words': ['ನಿಮ್ಮ', 'ನನ್ನ', 'ಈ', 'ಆ', 'ಇಲ್ಲಿ', 'ಅಲ್ಲಿ'],
                'scam_words': ['ಬ್ಯಾಂಕ್', 'ಖಾತೆ', 'ಒಟಿಪಿ', 'ಬಹುಮಾನ', 'ಹಣ']
            },
            'malayalam': {
                'script': 'malayalam',
                'words': ['നിങ്ങളുടെ', 'എന്റെ', 'ഈ', 'ആ', 'ഇവിടെ', 'അവിടെ'],
                'scam_words': ['ബാങ്ക്', 'അക്കൗണ്ട്', 'ഒടിപി', 'സമ്മാനം', 'പണം']
            },
            'gujarati': {
                'script': 'gujarati',
                'words': ['તમારું', 'મારું', 'આ', 'તે', 'અહીં', 'ત્યાં'],
                'scam_words': ['બેંક', 'ખાતું', 'ઓટીપી', 'ઇનામ', 'પૈસા']
            },
            'bengali': {
                'script': 'bengali',
                'words': ['আপনার', 'আমার', 'এই', 'সেই', 'এখানে', 'সেখানে'],
                'scam_words': ['ব্যাঙ্ক', 'অ্যাকাউন্ট', 'ওটিপি', 'পুরস্কার', 'টাকা']
            },
            'punjabi': {
                'script': 'gurmukhi',
                'words': ['ਤੁਹਾਡਾ', 'ਮੇਰਾ', 'ਇਹ', 'ਉਹ', 'ਇੱਥੇ', 'ਉੱਥੇ'],
                'scam_words': ['ਬੈਂਕ', 'ਖਾਤਾ', 'ਓਟੀਪੀ', 'ਇਨਾਮ', 'ਪੈਸੇ']
            },
            'odia': {
                'script': 'oriya',
                'words': ['ତୁମର', 'ମୋର', 'ଏହା', 'ସେହି', 'ଏଠାରେ', 'ସେଠାରେ'],
                'scam_words': ['ବ୍ୟାଙ୍କ', 'ଖାତା', 'ଓଟିପି', 'ପୁରସ୍କାର', 'ଟଙ୍କା']
            },
            'hinglish': {
                'script': 'latin',
                'patterns': [
                    r'\b(aap|tum|main|hum|ka|ki|ke|ko|se|mein|hai|hain|tha|the)\b',
                    r'\b(apna|mera|tera|iska|uska|kya|kyu|kaise|kahan|kab)\b',
                    r'\b(yeh|woh|jo|so|to|bhi|hi|nahi|haan|na)\b'
                ]
            },
            'english': {
                'script': 'latin',
                'patterns': [
                    r'\b(the|is|are|was|were|will|shall|have|has|had)\b',
                    r'\b(your|my|our|their|this|that|here|there)\b'
                ]
            }
        }
        
        # Universal scam patterns (works across languages)
        self.universal_scam_indicators = {
            'banking': ['bank', 'account', 'otp', 'pin', 'password', 'verify', 'kyc'],
            'money': ['money', 'cash', 'prize', 'lottery', 'won', 'reward', 'free'],
            'urgency': ['urgent', 'immediate', 'today', 'now', 'limited', 'expire'],
            'authority': ['police', 'court', 'govt', 'income tax', 'aadhaar', 'pan'],
            'action': ['click', 'call', 'whatsapp', 'download', 'update', 'verify']
        }
        
    def detect_script(self, text):
        """
        Detect which Indian script is used in the text
        Returns: script_name, confidence, character_counts
        """
        if not text or len(text.strip()) == 0:
            return 'unknown', 0, {}
        
        # Count characters in each script
        script_counts = {}
        total_chars = len(text)
        
        for script_name, (start, end) in self.script_ranges.items():
            count = sum(1 for char in text if start <= ord(char) <= end)
            if count > 0:
                script_counts[script_name] = count
        
        # Count Latin characters (English, Hinglish)
        latin_count = sum(1 for char in text if 0x0041 <= ord(char.upper()) <= 0x005A)
        if latin_count > 0:
            script_counts['latin'] = latin_count
        
        # Count digits and special chars (language agnostic)
        digit_count = sum(1 for char in text if char.isdigit())
        special_count = sum(1 for char in text if not char.isalnum() and not char.isspace())
        
        if not script_counts:
            return 'unknown', 0, {'digits': digit_count, 'special': special_count}
        
        # Find dominant script
        dominant_script = max(script_counts, key=script_counts.get)
        confidence = script_counts[dominant_script] / total_chars if total_chars > 0 else 0
        
        return dominant_script, confidence, script_counts
    
    def detect_language(self, text):
        """
        Detect specific Indian language from text
        Returns: language_code, confidence, details
        """
        if not text or len(text.strip()) == 0:
            return 'unknown', 0, {'error': 'empty text'}
        
        # First detect script
        script, script_conf, script_counts = self.detect_script(text)
        text_lower = text.lower()
        
        # If Latin script, check for English or Hinglish
        if script == 'latin':
            # Check for Hinglish patterns
            hinglish_score = 0
            for pattern in self.language_indicators['hinglish']['patterns']:
                if re.search(pattern, text_lower):
                    hinglish_score += 0.2
            
            if hinglish_score > 0.4:
                return 'hinglish', min(hinglish_score, 0.95), {
                    'script': script,
                    'pattern_matches': hinglish_score
                }
            
            # Check for English patterns
            english_score = 0
            for pattern in self.language_indicators['english']['patterns']:
                if re.search(pattern, text_lower):
                    english_score += 0.15
            
            if english_score > 0.3:
                return 'english', min(english_score, 0.9), {
                    'script': script,
                    'pattern_matches': english_score
                }
            
            return 'unknown_latin', 0.3, {'script': script}
        
        # For Indic scripts, find specific language
        if script in ['devanagari', 'tamil', 'telugu', 'kannada', 'malayalam', 
                      'gujarati', 'bengali', 'gurmukhi', 'oriya']:
            
            # Get all languages that use this script
            candidate_languages = [
                lang for lang, info in self.language_indicators.items()
                if info.get('script') == script and lang != 'hinglish' and lang != 'english'
            ]
            
            if not candidate_languages:
                return script, 0.5, {'script': script}
            
            # Score each candidate language
            scores = {}
            for lang in candidate_languages:
                score = 0
                indicators = self.language_indicators.get(lang, {})
                
                # Check for common words
                for word in indicators.get('words', []):
                    if word in text:
                        score += 0.1
                
                # Check for scam words (bonus)
                for word in indicators.get('scam_words', []):
                    if word in text:
                        score += 0.15
                
                if score > 0:
                    scores[lang] = score
            
            if scores:
                best_lang = max(scores, key=scores.get)
                confidence = min(scores[best_lang] + script_conf * 0.3, 0.98)
                return best_lang, confidence, {
                    'script': script,
                    'script_confidence': script_conf,
                    'language_scores': scores
                }
            
            # If no language-specific words found, return just script
            return script, script_conf * 0.7, {'script': script}
        
        return 'unknown', 0.1, {'script': script}
    
    def extract_universal_scam_features(self, text):
        """
        Extract scam indicators that work across all languages
        Returns dictionary of feature scores
        """
        features = {}
        text_lower = text.lower()
        
        for category, keywords in self.universal_scam_indicators.items():
            matches = 0
            for keyword in keywords:
                if keyword in text_lower:
                    matches += 1
            features[f'scam_{category}_score'] = matches / len(keywords)
            features[f'scam_{category}_present'] = int(matches > 0)
        
        return features
    
    def get_language_name(self, lang_code):
        """Get display name in native script"""
        names = {
            'hindi': 'हिंदी',
            'marathi': 'मराठी',
            'tamil': 'தமிழ்',
            'telugu': 'తెలుగు',
            'kannada': 'ಕನ್ನಡ',
            'malayalam': 'മലയാളം',
            'gujarati': 'ગુજરાતી',
            'bengali': 'বাংলা',
            'punjabi': 'ਪੰਜਾਬੀ',
            'odia': 'ଓଡ଼ିଆ',
            'hinglish': 'हिंग्लिश',
            'english': 'English',
            'devanagari': 'देवनागरी',
            'tamil_script': 'தமிழ்',
            'telugu_script': 'తెలుగు',
            'kannada_script': 'ಕನ್ನಡ',
            'malayalam_script': 'മലയാളം',
            'gujarati_script': 'ગુજરાતી',
            'bengali_script': 'বাংলা',
            'gurmukhi_script': 'ਗੁਰਮੁਖੀ',
            'oriya_script': 'ଓଡ଼ିଆ'
        }
        return names.get(lang_code, lang_code)


# Test the detector
if __name__ == "__main__":
    detector = IndianLanguageDetector()
    
    test_texts = [
        # Marathi
        "तुमचे बँक खाते बंद होणार आहे. लगेच KYC अपडेट करा",
        
        # Tamil
        "உங்கள் வங்கி கணக்கு மூடப்படும். உடனே OTP பகிரவும்",
        
        # Telugu
        "మీ బ్యాంక్ ఖాతా మూసివేయబడుతుంది. వెంటనే OTP షేర్ చేయండి",
        
        # Kannada
        "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಯನ್ನು ಮುಚ್ಚಲಾಗುವುದು. ತಕ್ಷಣ OTP ಹಂಚಿಕೊಳ್ಳಿ",
        
        # Malayalam
        "നിങ്ങളുടെ ബാങ്ക് അക്കൗണ്ട് അടച്ചുപൂട്ടും. ഉടൻ OTP ഷെയർ ചെയ്യുക",
        
        # Gujarati
        "તમારું બેંક ખાતું બંધ થશે. તરત OTP શેર કરો",
        
        # Bengali
        "আপনার ব্যাঙ্ক অ্যাকাউন্ট বন্ধ হয়ে যাবে। এখনই OTP শেয়ার করুন",
        
        # Punjabi
        "ਤੁਹਾਡਾ ਬੈਂਕ ਖਾਤਾ ਬੰਦ ਹੋ ਜਾਵੇਗਾ। ਤੁਰੰਤ OTP ਸਾਂਝਾ ਕਰੋ",
        
        # Hinglish
        "Aapka bank account band ho jayega. Turant OTP share karein",
        
        # English
        "Your bank account will be closed. Share OTP immediately"
    ]
    
    print("=" * 80)
    print("LANGUAGE DETECTION TEST")
    print("=" * 80)
    
    for i, text in enumerate(test_texts, 1):
        lang, conf, details = detector.detect_language(text)
        display_name = detector.get_language_name(lang)
        
        print(f"\n{i}. Text: {text[:80]}...")
        print(f"   Language: {display_name} (confidence: {conf:.2%})")
        print(f"   Details: {details}")
        
        # Also show universal scam features
        scam_features = detector.extract_universal_scam_features(text)
        print(f"   Scam indicators: {scam_features}")
        print("-" * 80)