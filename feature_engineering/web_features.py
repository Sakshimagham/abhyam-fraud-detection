"""
Enhanced Website Fraud Feature Engineering with Multilingual Support
Detects fake/scam websites in multiple Indian languages
"""

import os
import pandas as pd
import joblib
import numpy as np
import re
from urllib.parse import urlparse
from .multilingual_utils import MultilingualFeatureExtractor
from .language_detector import IndianLanguageDetector

# ============================================================================
# DYNAMIC PATH SETUP – replace absolute Windows paths
# ============================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
DATA_PATH = os.path.join(repo_root, "data", "processed", "websites_preprocessed.csv")
FEATURE_PATH = current_dir   # where vectorizers will be saved

class MultilingualWebsiteFeatureExtractor:
    """
    Enhanced website fraud feature extractor with multilingual support
    """
    
    def __init__(self):
        # Load website data
        if os.path.exists(DATA_PATH):
            self.df = pd.read_csv(DATA_PATH)
            # Handle missing values
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].fillna("")
        else:
            print(f"⚠️ Website data not found at {DATA_PATH}")
            self.df = pd.DataFrame()
        
        # Initialize multilingual utilities
        self.multilingual_utils = MultilingualFeatureExtractor()
        self.language_detector = IndianLanguageDetector()
        
        # Indian-specific domain patterns
        self.indian_domain_patterns = {
            'govt_domains': ['.gov.in', '.nic.in', '.ac.in', '.edu.in'],
            'popular_indian': ['.co.in', '.in', '.bharat'],
            'bank_domains': ['sbi.co.in', 'hdfcbank.com', 'icicibank.com'],
            'payment_domains': ['paytm.com', 'phonepe.com', 'razorpay.com']
        }
        
        # Suspicious TLDs common in scams
        self.suspicious_tlds = [
            '.xyz', '.top', '.club', '.online', '.site', '.work', 
            '.date', '.loan', '.win', '.bid', '.trade', '.webcam'
        ]
        
        # Scam website keywords in Indian languages
        self.website_scam_keywords = {
            'marathi': {
                'banking': ['बँक', 'खाते', 'लॉगिन', 'पासवर्ड', 'ओटीपी'],
                'govt': ['सरकार', 'आधार', 'पॅन', 'योजना'],
                'offers': ['ऑफर', 'स्कीम', 'बक्षीस', 'मोफत'],
                'urgent': ['तातडीचे', 'अपडेट', 'व्हेरिफाय']
            },
            'hindi': {
                'banking': ['बैंक', 'खाता', 'लॉगिन', 'पासवर्ड', 'ओटीपी'],
                'govt': ['सरकार', 'आधार', 'पैन', 'योजना'],
                'offers': ['ऑफर', 'स्कीम', 'इनाम', 'मुफ्त'],
                'urgent': ['तुरंत', 'अपडेट', 'वेरिफाई']
            },
            'tamil': {
                'banking': ['வங்கி', 'கணக்கு', 'உள்நுழை', 'கடவுச்சொல்', 'ஓடிபி'],
                'govt': ['அரசு', 'ஆதார்', 'திட்டம்'],
                'offers': ['சலுகை', 'பரிசு', 'இலவசம்'],
                'urgent': ['அவசரம்', 'புதுப்பிப்பு', 'சரிபார்']
            }
        }
        
        # URL-based features
        self.url_features = {
            'suspicious_words': [
                'secure', 'login', 'signin', 'verify', 'update', 'confirm',
                'bank', 'account', 'payment', 'transaction', 'otp', 'password'
            ],
            'typo_words': [
                'faceboook', 'gooogle', 'amazoon', 'flipkartt', 'paytmm',
                'sbii', 'hdfc', 'iciciii', 'whatsappp', 'telegramm'
            ]
        }
    
    def extract_url_features(self, url):
        """
        Extract features from URL
        """
        features = {}
        
        if not url or pd.isna(url):
            features['url_present'] = 0
            return features
        
        features['url_present'] = 1
        url_lower = url.lower()
        
        try:
            parsed = urlparse(url_lower)
            domain = parsed.netloc or parsed.path.split('/')[0]
            path = parsed.path
            query = parsed.query
            
            # Basic URL features
            features['url_length'] = len(url)
            features['domain_length'] = len(domain)
            features['num_subdomains'] = domain.count('.') - 1
            features['num_digits'] = sum(c.isdigit() for c in domain)
            features['num_hyphens'] = domain.count('-')
            features['num_slashes'] = path.count('/')
            features['num_params'] = query.count('&') + (1 if query else 0)
            
            # Check for HTTPS
            features['https'] = int(url_lower.startswith('https'))
            
            # Check for IP address instead of domain
            features['is_ip'] = int(bool(re.match(r'\d+\.\d+\.\d+\.\d+', domain)))
            
            # Check TLD
            for tld in self.suspicious_tlds:
                if domain.endswith(tld):
                    features[f'tld_{tld[1:]}'] = 1
            
            # Indian domains
            for pattern in self.indian_domain_patterns['govt_domains']:
                if domain.endswith(pattern):
                    features['is_gov_domain'] = 1
            
            if domain.endswith('.in') or domain.endswith('.co.in'):
                features['is_indian_domain'] = 1
            
            # Check for suspicious words in URL
            for word in self.url_features['suspicious_words']:
                if word in domain or word in path:
                    features[f'url_has_{word}'] = 1
            
            # Check for typos of popular sites
            for typo in self.url_features['typo_words']:
                if typo in domain:
                    features['url_has_typo'] = 1
            
            # Check for brand names in suspicious context
            brands = ['sbi', 'hdfc', 'icici', 'axis', 'paytm', 'google', 'amazon', 'flipkart']
            for brand in brands:
                if brand in domain and any(word in domain for word in ['secure', 'login', 'verify']):
                    features['brand_in_suspicious_context'] = 1
            
            # Check for @ in URL (phishing)
            features['has_at_symbol'] = int('@' in url)
            
            # Check for multiple dots
            features['many_dots'] = int(domain.count('.') > 3)
            
        except Exception as e:
            print(f"Error parsing URL {url}: {e}")
        
        return features
    
    def extract_content_features(self, html_content, title, meta_description):
        """
        Extract features from webpage content
        """
        features = {}
        
        # Combine all text
        all_text = f"{title} {meta_description} {html_content}".lower()
        
        if not all_text:
            return features
        
        # Language detection
        lang, conf, _ = self.language_detector.detect_language(all_text)
        features['content_language'] = lang
        features['content_language_confidence'] = conf
        
        # Content length features
        features['content_length'] = len(all_text)
        features['title_length'] = len(title) if title else 0
        
        # Check for payment-related content
        payment_keywords = [
            'upi', 'credit card', 'debit card', 'netbanking', 'payment',
            'भुगतान', 'பணம்', 'చెల్లింపు', 'ಪಾವತಿ'
        ]
        features['has_payment_keywords'] = sum(1 for kw in payment_keywords if kw in all_text)
        
        # Check for login forms
        login_keywords = ['login', 'signin', 'log in', 'sign in', 'लॉगिन']
        features['has_login_form'] = int(any(kw in all_text for kw in login_keywords))
        
        # Check for multiple languages on page
        script_counts = self.multilingual_utils.extract_script_features(all_text)
        features['page_multilingual'] = script_counts.get('code_mixed', 0)
        
        return features
    
    def extract_trust_features(self, trust_data):
        """
        Extract trust-related features
        """
        features = {}
        
        # Domain age
        if 'domain_age' in trust_data:
            features['domain_age_days'] = trust_data['domain_age']
            features['new_domain'] = int(trust_data['domain_age'] < 30)  # Less than 30 days
        
        # SSL certificate
        if 'has_ssl' in trust_data:
            features['has_ssl'] = trust_data['has_ssl']
        
        # Contact information
        if 'has_contact' in trust_data:
            features['has_contact_page'] = trust_data['has_contact']
        
        if 'has_phone' in trust_data:
            features['has_phone'] = trust_data['has_phone']
            
            # Check if Indian phone
            if trust_data.get('phone', ''):
                features['has_indian_phone'] = int(bool(re.search(r'(\+91|0)?[6-9]\d{9}', trust_data['phone'])))
        
        if 'has_email' in trust_data:
            features['has_email'] = trust_data['has_email']
            
            # Check email domain
            email = trust_data.get('email', '')
            if email:
                features['email_has_company_domain'] = int('@' in email and 
                                                          not any(domain in email for domain in 
                                                                 ['gmail', 'yahoo', 'hotmail', 'rediffmail']))
        
        # Social media presence
        if 'has_social_links' in trust_data:
            features['has_social_links'] = trust_data['has_social_links']
        
        # Privacy policy and terms
        if 'has_privacy_policy' in trust_data:
            features['has_privacy_policy'] = trust_data['has_privacy_policy']
        
        if 'has_terms' in trust_data:
            features['has_terms'] = trust_data['has_terms']
        
        return features
    
    def extract_all_features(self, url=None, html_content=None, title=None, 
                           meta_description=None, trust_data=None):
        """
        Extract ALL features for website fraud detection
        """
        features = {}
        
        # Extract URL features
        if url:
            features.update(self.extract_url_features(url))
        
        # Extract content features
        if html_content or title or meta_description:
            features.update(self.extract_content_features(
                html_content or '', 
                title or '', 
                meta_description or ''
            ))
        
        # Extract trust features
        if trust_data:
            features.update(self.extract_trust_features(trust_data))
        
        return features
    
    def prepare_training_data(self):
        """
        Prepare feature matrix for model training
        """
        if self.df.empty:
            print("⚠️ No website data available for training")
            return np.array([]), np.array([])
        
        print("📊 Preparing multilingual website training data...")
        
        all_features = []
        labels = []
        
        for idx, row in self.df.iterrows():
            url = row.get('url', '')
            content = row.get('html_content', row.get('content', ''))
            title = row.get('title', '')
            meta = row.get('meta_description', '')
            
            trust_data = {
                'domain_age': row.get('domain_age', 0),
                'has_ssl': row.get('has_ssl', 0),
                'has_contact': row.get('has_contact', 0),
                'has_phone': row.get('has_phone', 0),
                'phone': row.get('phone', ''),
                'has_email': row.get('has_email', 0),
                'email': row.get('email', ''),
                'has_social_links': row.get('has_social_links', 0),
                'has_privacy_policy': row.get('has_privacy_policy', 0),
                'has_terms': row.get('has_terms', 0)
            }
            
            label = row.get('fraudulent', row.get('fake', row.get('label', 0)))
            
            # Extract features
            features = self.extract_all_features(
                url=url,
                html_content=content,
                title=title,
                meta_description=meta,
                trust_data=trust_data
            )
            
            # Flatten features into vector
            feature_vector = []
            for key, value in features.items():
                if isinstance(value, (int, float)):
                    feature_vector.append(value)
                elif key == 'content_language' and isinstance(value, str):
                    # One-hot encode language
                    for lang in ['hindi', 'marathi', 'tamil', 'telugu', 'kannada', 
                               'malayalam', 'gujarati', 'bengali', 'punjabi', 'hinglish', 'english']:
                        feature_vector.append(1 if value == lang else 0)
            
            all_features.append(feature_vector)
            labels.append(label)
            
            if idx % 100 == 0:
                print(f"  Processed {idx} websites...")
        
        if all_features:
            # Pad vectors to same length
            max_len = max(len(v) for v in all_features)
            X_padded = np.array([v + [0] * (max_len - len(v)) for v in all_features])
            y = np.array(labels)
            print(f"✅ Website training data prepared: {X_padded.shape}")
            return X_padded, y
        else:
            print("⚠️ No features extracted from website data")
            return np.array([]), np.array([])
    
    def save_vectorizers(self):
        """
        Save vectorizers for website features
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import StandardScaler
        
        # Text vectorizer for website content
        if not self.df.empty:
            texts = []
            for _, row in self.df.iterrows():
                text = f"{row.get('title', '')} {row.get('meta_description', '')} {row.get('content', '')[:1000]}"
                texts.append(text)
            
            if texts:
                vectorizer = TfidfVectorizer(max_features=2000)
                vectorizer.fit(texts)
                
                os.makedirs(FEATURE_PATH, exist_ok=True)
                joblib.dump(vectorizer, os.path.join(FEATURE_PATH, "web_text_vectorizer.pkl"))
                
                # Also save language detector
                joblib.dump(self.language_detector, os.path.join(FEATURE_PATH, "web_language_detector.pkl"))
                
                print("✅ Website vectorizers saved successfully")
        else:
            print("⚠️ No text data to fit vectorizer")


# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("MULTILINGUAL WEBSITE FRAUD FEATURE ENGINEERING")
    print("=" * 80)
    
    # Initialize extractor
    extractor = MultilingualWebsiteFeatureExtractor()
    
    # Test on sample websites
    test_websites = [
        {
            'url': 'https://sbi-secure-login.com',
            'title': 'SBI - Secure Login',
            'meta_description': 'Login to your SBI account',
            'trust_data': {
                'domain_age': 5,
                'has_ssl': 1,
                'has_contact': 0,
                'has_phone': 1,
                'phone': '9876543210',
                'has_email': 1,
                'email': 'support@gmail.com',
                'has_social_links': 0,
                'has_privacy_policy': 0,
                'has_terms': 0
            }
        },
        {
            'url': 'https://pmkisan.gov.in',
            'title': 'PM Kisan Samman Nidhi',
            'meta_description': 'Official website for PM Kisan scheme',
            'trust_data': {
                'domain_age': 800,
                'has_ssl': 1,
                'has_contact': 1,
                'has_phone': 1,
                'phone': '1800-123-4567',
                'has_email': 1,
                'email': 'help@pmkisan.gov.in',
                'has_social_links': 1,
                'has_privacy_policy': 1,
                'has_terms': 1
            }
        },
        {
            'url': 'https://flipkartt-offer.xyz',
            'title': 'Flipkart Big Billion Days - Win ₹1 Lakh',
            'meta_description': 'Click here to claim your prize',
            'trust_data': {
                'domain_age': 2,
                'has_ssl': 0,
                'has_contact': 0,
                'has_phone': 0,
                'has_email': 1,
                'email': 'offers@gmail.com',
                'has_social_links': 0,
                'has_privacy_policy': 0,
                'has_terms': 0
            }
        }
    ]
    
    print("\n🔍 TESTING WEBSITE FEATURE EXTRACTION:\n")
    
    for i, test in enumerate(test_websites, 1):
        print(f"Test Website {i}: {test['url']}")
        features = extractor.extract_all_features(
            url=test['url'],
            title=test['title'],
            meta_description=test['meta_description'],
            trust_data=test['trust_data']
        )
        
        # Show key features
        print(f"  HTTPS: {features.get('https', 0)}")
        print(f"  Domain age: {features.get('domain_age_days', 0)} days")
        print(f"  New domain: {features.get('new_domain', 0)}")
        print(f"  Suspicious TLD: {any(features.get(f'tld_{tld[1:]}', 0) for tld in extractor.suspicious_tlds)}")
        print(f"  Has contact: {features.get('has_contact_page', 0)}")
        print(f"  Has privacy policy: {features.get('has_privacy_policy', 0)}")
        print("-" * 60)
    
    # Save vectorizers
    print("\n💾 Saving vectorizers...")
    extractor.save_vectorizers()
    
    print("\n✅ Website feature engineering module ready!")
