# feature_engineering/crypto_features.py
"""
Enhanced Cryptocurrency Fraud Feature Engineering with Multilingual Support
Detects crypto scams in multiple Indian languages
"""

import os
import pandas as pd
import joblib
import numpy as np
import re
from urllib.parse import urlparse
from .multilingual_utils import MultilingualFeatureExtractor
from .language_detector import IndianLanguageDetector

BASE_PATH = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system"
DATA_PATH = os.path.join(BASE_PATH, "data", "processed", "crypto_fraud_preprocessed.csv")
FEATURE_PATH = os.path.join(BASE_PATH, "feature_engineering")

class MultilingualCryptoFeatureExtractor:
    """
    Enhanced crypto fraud feature extractor with multilingual support
    """
    
    def __init__(self):
        # Load crypto data
        if os.path.exists(DATA_PATH):
            self.df = pd.read_csv(DATA_PATH)
            # Handle missing values
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].fillna("")
        else:
            print(f"⚠️ Crypto data not found at {DATA_PATH}")
            self.df = pd.DataFrame()
        
        # Initialize multilingual utilities
        self.multilingual_utils = MultilingualFeatureExtractor()
        self.language_detector = IndianLanguageDetector()
        
        # Crypto scam keywords in Indian languages
        self.crypto_scam_keywords = {
            'marathi': {
                'investment': ['गुंतवणूक', 'पैसे दुप्पट', 'बिटकॉइन', 'क्रिप्टो', 'ट्रेडिंग'],
                'schemes': ['योजना', 'स्कीम', 'कंपनी', 'बोनस', 'रिटर्न्स'],
                'urgency': ['तातडीचे', 'मर्यादित', 'शेवटची संधी', 'आजच'],
                'guarantee': ['हमी', 'निश्चित', 'गॅरंटीड', 'प्रॉफिट']
            },
            'hindi': {
                'investment': ['निवेश', 'पैसे दोगुने', 'बिटकॉइन', 'क्रिप्टो', 'ट्रेडिंग'],
                'schemes': ['योजना', 'स्कीम', 'कंपनी', 'बोनस', 'रिटर्न'],
                'urgency': ['तुरंत', 'सीमित', 'आखिरी मौका', 'आज ही'],
                'guarantee': ['गारंटी', 'निश्चित', 'पक्का', 'मुनाफा']
            },
            'tamil': {
                'investment': ['முதலீடு', 'பணம் இரட்டிப்பு', 'பிட்காயின்', 'கிரிப்டோ', 'டிரேடிங்'],
                'schemes': ['திட்டம்', 'ஸ்கீம்', 'நிறுவனம்', 'போனஸ்', 'வருமானம்'],
                'urgency': ['அவசரம்', 'குறைந்த', 'கடைசி வாய்ப்பு', 'இன்றே'],
                'guarantee': ['உத்தரவாதம்', 'நிச்சயம்', 'கேரண்டி', 'லாபம்']
            },
            'telugu': {
                'investment': ['పెట్టుబడి', 'డబ్బు రెట్టింపు', 'బిట్కాయిన్', 'క్రిప్టో', 'ట్రేడింగ్'],
                'schemes': ['పథకం', 'స్కీమ్', 'కంపెనీ', 'బోనస్', 'రిటర్న్స్'],
                'urgency': ['అత్యవసరం', 'పరిమితం', 'చివరి అవకాశం', 'ఈరోజే'],
                'guarantee': ['గ్యారంటీ', 'ఖచ్చితం', 'గ్యారెంటీడ్', 'లాభం']
            },
            'kannada': {
                'investment': ['ಹೂಡಿಕೆ', 'ಹಣ ದುಪ್ಪಟ್ಟು', 'ಬಿಟ್ಕಾಯಿನ್', 'ಕ್ರಿಪ್ಟೋ', 'ಟ್ರೇಡಿಂಗ್'],
                'schemes': ['ಯೋಜನೆ', 'ಸ್ಕೀಮ್', 'ಕಂಪನಿ', 'ಬೋನಸ್', 'ರಿಟರ್ನ್ಸ್'],
                'urgency': ['ತುರ್ತು', 'ಸೀಮಿತ', 'ಕೊನೆಯ ಅವಕಾಶ', 'ಇಂದೇ'],
                'guarantee': ['ಗ್ಯಾರಂಟಿ', 'ನಿಶ್ಚಿತ', 'ಗ್ಯಾರಂಟೀಡ್', 'ಲಾಭ']
            },
            'gujarati': {
                'investment': ['રોકાણ', 'પૈસા બમણા', 'બિટકોઇન', 'ક્રિપ્ટો', 'ટ્રેડિંગ'],
                'schemes': ['યોજના', 'સ્કીમ', 'કંપની', 'બોનસ', 'રિટર્ન'],
                'urgency': ['તાત્કાલિક', 'મર્યાદિત', 'છેલ્લી તક', 'આજે જ'],
                'guarantee': ['ગેરંટી', 'નિશ્ચિત', 'ગેરંટીડ', 'નફો']
            },
            'bengali': {
                'investment': ['বিনিয়োগ', 'টাকা দ্বিগুণ', 'বিটকয়েন', 'ক্রিপ্টো', 'ট্রেডিং'],
                'schemes': ['স্কিম', 'কোম্পানি', 'বোনাস', 'রিটার্ন'],
                'urgency': ['জরুরি', 'সীমিত', 'শেষ সুযোগ', 'আজই'],
                'guarantee': ['গ্যারান্টি', 'নিশ্চিত', 'গ্যারান্টিড', 'লাভ']
            }
        }
        
        # URL-based scam indicators
        self.url_scam_indicators = {
            'suspicious_tlds': ['.xyz', '.top', '.club', '.online', '.site', '.work', '.date', '.loan'],
            'crypto_related': ['bitcoin', 'btc', 'eth', 'crypto', 'mining', 'wallet', 'exchange'],
            'phishing_words': ['secure', 'verify', 'login', 'signin', 'account', 'update', 'confirm'],
            'indian_spellings': ['bitcoiin', 'bitcojn', 'crypt0', 'blockchian', 'wallrt']
        }
        
        # Indian payment gateway mentions
        self.indian_payment_gateways = [
            'paytm', 'phonepe', 'googlepay', 'gpay', 'amazonpay', 'bhimp',
            'upi', 'rupay', 'netbanking', 'imps', 'neft', 'rtgs'
        ]
        
        # Crypto scammer tactics in Indian context
        self.indian_crypto_tactics = [
            'double_money',  # पैसे दुप्पट / பணம் இரட்டிப்பு
            'guaranteed_returns',  # गॅरंटीड रिटर्न्स
            'mining_investment',  # मायनिंग इन्वेस्टमेंट
            'ico_fraud',  # ICO scams
            'ponzi_scheme',  # Ponzi schemes
            'referral_bonus',  # Referral bonuses
            'withdrawal_issues',  # Can't withdraw money
            'hidden_fees'  # Hidden fees
        ]
    
    def extract_url_features(self, url):
        """
        Extract features from URLs (language independent)
        """
        features = {}
        
        if not url or pd.isna(url):
            features['url_present'] = 0
            return features
        
        features['url_present'] = 1
        url = url.lower()
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split('/')[0]
            path = parsed.path
            
            # Domain features
            features['url_length'] = len(url)
            features['domain_length'] = len(domain)
            features['num_dots'] = domain.count('.')
            features['num_hyphens'] = domain.count('-')
            features['num_digits'] = sum(c.isdigit() for c in domain)
            
            # Suspicious TLDs
            for tld in self.url_scam_indicators['suspicious_tlds']:
                if domain.endswith(tld):
                    features[f'url_tld_{tld[1:]}'] = 1
            
            # Contains crypto keywords
            for keyword in self.url_scam_indicators['crypto_related']:
                if keyword in domain or keyword in path:
                    features[f'url_has_{keyword}'] = 1
            
            # Contains phishing words
            for word in self.url_scam_indicators['phishing_words']:
                if word in domain or word in path:
                    features[f'url_has_{word}'] = 1
            
            # Misspelled crypto words
            for spelling in self.url_scam_indicators['indian_spellings']:
                if spelling in domain or spelling in path:
                    features['url_misspelled'] = 1
            
            # IP address instead of domain
            features['url_is_ip'] = int(bool(re.match(r'\d+\.\d+\.\d+\.\d+', domain)))
            
            # Shortened URL
            features['url_shortened'] = int('bit.ly' in url or 'tinyurl' in url or 't.co' in url)
            
            # HTTPS check
            features['url_https'] = int(url.startswith('https'))
            
        except Exception as e:
            print(f"Error parsing URL {url}: {e}")
        
        return features
    
    def extract_transaction_features(self, transaction_data):
        """
        Extract features from transaction data
        """
        features = {}
        
        if not transaction_data:
            return features
        
        # Transaction velocity (how many transactions in short time)
        if 'timestamps' in transaction_data:
            timestamps = transaction_data['timestamps']
            if len(timestamps) > 1:
                time_diffs = np.diff(sorted(timestamps))
                features['tx_avg_time_between'] = np.mean(time_diffs) if len(time_diffs) > 0 else 0
                features['tx_velocity'] = len(timestamps) / max(np.max(time_diffs), 1) if len(time_diffs) > 0 else 0
        
        # Amount patterns
        if 'amounts' in transaction_data:
            amounts = transaction_data['amounts']
            features['tx_num_transactions'] = len(amounts)
            features['tx_total_amount'] = sum(amounts)
            features['tx_avg_amount'] = np.mean(amounts) if amounts else 0
            features['tx_max_amount'] = max(amounts) if amounts else 0
            features['tx_min_amount'] = min(amounts) if amounts else 0
            
            # Round amounts (common in scams)
            round_amounts = sum(1 for amt in amounts if amt % 1000 == 0)
            features['tx_round_amounts_ratio'] = round_amounts / len(amounts) if amounts else 0
        
        # Address patterns
        if 'addresses' in transaction_data:
            addresses = transaction_data['addresses']
            features['tx_unique_addresses'] = len(set(addresses))
            features['tx_new_addresses_ratio'] = transaction_data.get('new_addresses', 0) / max(len(addresses), 1)
        
        return features
    
    def extract_text_features(self, text):
        """
        Extract crypto scam features from text content
        """
        features = {}
        
        if not text:
            return features
        
        text_lower = text.lower()
        
        # Check for Indian payment gateways
        for gateway in self.indian_payment_gateways:
            if gateway in text_lower:
                features[f'payment_{gateway}'] = 1
        
        # Check for WhatsApp/Telegram groups (common for crypto scams)
        features['has_whatsapp'] = int('whatsapp' in text_lower or 'व्हाट्सएप' in text)
        features['has_telegram'] = int('telegram' in text_lower or 'टेलीग्राम' in text)
        
        # Check for promise words
        promise_words = ['guaranteed', 'assured', 'confirmed', 'हमी', 'गॅरंटी', 'உத்தரவாதம்']
        features['promise_word_count'] = sum(1 for word in promise_words if word in text_lower)
        
        # Check for "double money" in multiple languages
        double_patterns = [
            r'double|duplicate|दुप्पट|இரட்டிப்பு|రెట్టింపు|ದುಪ್ಪಟ್ಟು|બમણા|দ্বিগুণ'
        ]
        for pattern in double_patterns:
            if re.search(pattern, text_lower):
                features['has_double_money_claim'] = 1
                break
        
        return features
    
    def extract_all_features(self, url=None, text=None, transaction_data=None):
        """
        Extract ALL features for crypto fraud detection
        """
        features = {}
        
        # Extract URL features
        if url:
            features.update(self.extract_url_features(url))
        
        # Extract text features
        if text:
            # Get multilingual features from text
            features.update(self.multilingual_utils.extract_all_features(text))
            # Get crypto-specific text features
            features.update(self.extract_text_features(text))
        
        # Extract transaction features
        if transaction_data:
            features.update(self.extract_transaction_features(transaction_data))
        
        return features
    
    def prepare_training_data(self):
        """
        Prepare feature matrix for model training
        """
        if self.df.empty:
            print("⚠️ No crypto data available for training")
            return np.array([]), np.array([])
        
        print("📊 Preparing multilingual crypto training data...")
        
        all_features = []
        labels = []
        
        for idx, row in self.df.iterrows():
            url = row.get('url', '')
            text = row.get('description', row.get('text', ''))
            label = row.get('label', 0)
            
            # Extract features
            features = self.extract_all_features(url=url, text=text)
            
            # Flatten features into vector
            feature_vector = []
            for key, value in features.items():
                if isinstance(value, (int, float)):
                    feature_vector.append(value)
            
            if feature_vector:  # Only add if we have features
                all_features.append(feature_vector)
                labels.append(label)
            
            if idx % 100 == 0:
                print(f"  Processed {idx} records...")
        
        if all_features:
            # Pad vectors to same length
            max_len = max(len(v) for v in all_features)
            X_padded = np.array([v + [0] * (max_len - len(v)) for v in all_features])
            y = np.array(labels)
            print(f"✅ Crypto training data prepared: {X_padded.shape}")
            return X_padded, y
        else:
            print("⚠️ No features extracted from crypto data")
            return np.array([]), np.array([])
    
    def save_vectorizers(self):
        """
        Save vectorizers for crypto features
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import StandardScaler
        
        # Text vectorizer for crypto descriptions
        if not self.df.empty and 'description' in self.df.columns:
            text_vectorizer = TfidfVectorizer(max_features=1000)
            text_vectorizer.fit(self.df['description'].fillna(''))
            
            os.makedirs(FEATURE_PATH, exist_ok=True)
            joblib.dump(text_vectorizer, os.path.join(FEATURE_PATH, "crypto_text_vectorizer.pkl"))
            
            # Also save language detector
            joblib.dump(self.language_detector, os.path.join(FEATURE_PATH, "crypto_language_detector.pkl"))
            
            print("✅ Crypto vectorizers saved successfully")
        else:
            print("⚠️ No text data to fit vectorizer")


# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("MULTILINGUAL CRYPTO FRAUD FEATURE ENGINEERING")
    print("=" * 80)
    
    # Initialize extractor
    extractor = MultilingualCryptoFeatureExtractor()
    
    # Test on sample crypto scams
    test_samples = [
        {
            'url': 'bit.ly/bitcoin-double-investment',
            'text': 'बिटकॉइन में निवेश करें और 1 महीने में पैसे दोगुने करें। गारंटीड रिटर्न्स। आज ही जॉइन करें। व्हाट्सएप ग्रुप से जुड़ें।',
            'transaction_data': None
        },
        {
            'url': 'https://crypto-mining-india.xyz',
            'text': 'உங்கள் பணத்தை இரட்டிப்பாக்குங்கள்! பிட்காயின் முதலீடு - உத்தரவாத வருமானம். குறைந்த நேரம், அதிக லாபம்.',
            'transaction_data': None
        },
        {
            'url': 'https://secure-bank-crypto.com',
            'text': 'Invest in Bitcoin and get guaranteed monthly returns. Limited offer! Join our Telegram group for signals.',
            'transaction_data': {
                'amounts': [1000, 5000, 10000, 10000, 5000],
                'timestamps': [1, 2, 3, 4, 5],
                'addresses': ['addr1', 'addr2', 'addr1', 'addr3', 'addr1'],
                'new_addresses': 2
            }
        }
    ]
    
    print("\n🔍 TESTING CRYPTO FEATURE EXTRACTION:\n")
    
    for i, test in enumerate(test_samples, 1):
        print(f"Test Crypto Scam {i}:")
        features = extractor.extract_all_features(
            url=test['url'],
            text=test['text'],
            transaction_data=test['transaction_data']
        )
        
        # Show key features
        print(f"  URL: {test['url']}")
        print(f"  Language: {features.get('detected_language', 'unknown')}")
        print(f"  URL shortened: {features.get('url_shortened', 0)}")
        print(f"  Has WhatsApp: {features.get('has_whatsapp', 0)}")
        print(f"  Has double money claim: {features.get('has_double_money_claim', 0)}")
        
        if test['transaction_data']:
            print(f"  Transactions: {features.get('tx_num_transactions', 0)}")
            print(f"  Total amount: {features.get('tx_total_amount', 0)}")
        
        print("-" * 60)
    
    # Save vectorizers
    print("\n💾 Saving vectorizers...")
    extractor.save_vectorizers()
    
    print("\n✅ Crypto feature engineering module ready!")