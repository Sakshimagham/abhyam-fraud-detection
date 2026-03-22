# feature_engineering/social_media_features.py
"""
Enhanced Social Media Fraud Feature Engineering with Multilingual Support
Detects fake profiles and social media scams in multiple Indian languages
"""

import os
import pandas as pd
import joblib
import numpy as np
import re
from datetime import datetime
from .multilingual_utils import MultilingualFeatureExtractor
from .language_detector import IndianLanguageDetector

BASE_PATH = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system"
DATA_PATH = os.path.join(BASE_PATH, "data", "processed", "social_media_preprocessed.csv")
FEATURE_PATH = os.path.join(BASE_PATH, "feature_engineering")

class MultilingualSocialMediaFeatureExtractor:
    """
    Enhanced social media fraud feature extractor with multilingual support
    """
    
    def __init__(self):
        # Load social media data
        if os.path.exists(DATA_PATH):
            self.df = pd.read_csv(DATA_PATH)
            # Handle missing values
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].fillna("")
        else:
            print(f"⚠️ Social media data not found at {DATA_PATH}")
            self.df = pd.DataFrame()
        
        # Initialize multilingual utilities
        self.multilingual_utils = MultilingualFeatureExtractor()
        self.language_detector = IndianLanguageDetector()
        
        # Social media scam keywords in Indian languages
        self.social_scam_keywords = {
            'marathi': {
                'romance': ['प्रेम', 'लव्ह', 'डेटिंग', 'सिंगल', 'मॅरेज'],
                'investment': ['गुंतवणूक', 'पैसे', 'शेअर बाजार', 'क्रिप्टो'],
                'friendship': ['मैत्री', 'फ्रेंडशिप', 'नवीन ओळख', 'भेट'],
                'urgent': ['तातडीचे', 'मदत', 'पैसे लागले', 'हॉस्पिटल']
            },
            'hindi': {
                'romance': ['प्यार', 'लव', 'डेटिंग', 'सिंगल', 'शादी'],
                'investment': ['निवेश', 'पैसे', 'शेयर मार्केट', 'क्रिप्टो'],
                'friendship': ['दोस्ती', 'नया परिचय', 'मिलना'],
                'urgent': ['तुरंत', 'मदद', 'पैसे चाहिए', 'अस्पताल']
            },
            'tamil': {
                'romance': ['காதல்', 'டேட்டிங்', 'திருமணம்', 'சிங்கிள்'],
                'investment': ['முதலீடு', 'பணம்', 'பங்குச் சந்தை', 'கிரிப்டோ'],
                'friendship': ['நட்பு', 'புதிய அறிமுகம்', 'சந்திப்பு'],
                'urgent': ['அவசரம்', 'உதவி', 'பணம் தேவை', 'மருத்துவமனை']
            },
            'telugu': {
                'romance': ['ప్రేమ', 'డేటింగ్', 'పెళ్లి', 'సింగిల్'],
                'investment': ['పెట్టుబడి', 'డబ్బు', 'షేర్ మార్కెట్', 'క్రిప్టో'],
                'friendship': ['స్నేహం', 'కొత్త పరిచయం', 'కలవడం'],
                'urgent': ['అత్యవసరం', 'సహాయం', 'డబ్బు అవసరం', 'ఆసుపత్రి']
            },
            'kannada': {
                'romance': ['ಪ್ರೇಮ', 'ಡೇಟಿಂಗ್', 'ಮದುವೆ', 'ಸಿಂಗಲ್'],
                'investment': ['ಹೂಡಿಕೆ', 'ಹಣ', 'ಶೇರು ಮಾರುಕಟ್ಟೆ', 'ಕ್ರಿಪ್ಟೋ'],
                'friendship': ['ಸ್ನೇಹ', 'ಹೊಸ ಪರಿಚಯ', 'ಭೇಟಿ'],
                'urgent': ['ತುರ್ತು', 'ಸಹಾಯ', 'ಹಣ ಬೇಕು', 'ಆಸ್ಪತ್ರೆ']
            }
        }
        
        # Profile-based features for fake detection
        self.profile_red_flags = {
            'name_patterns': [
                r'[0-9]{4,}',  # Many numbers in name
                r'^[a-z]{1,2}\d+$',  # Short name with numbers
                r'(admin|support|help|official|real|original)'  # Pretending to be official
            ],
            'bio_patterns': [
                'link in bio', 'click link', 'DM me', 'message me',
                'लिंक', 'คลิก', 'சுட்டி', 'లింక్'
            ],
            'suspicious_links': [
                'bit.ly', 'tinyurl', 'goo.gl', 'instagram.com/', 'youtube.com/'
            ]
        }
        
        # Indian social media trends
        self.indian_social_media_platforms = [
            'instagram', 'facebook', 'twitter', 'telegram', 'whatsapp',
            'sharechat', 'moj', 'mitron', 'chingari'
        ]
        
        # Bot-like behavior patterns
        self.bot_patterns = [
            r'(@\w+\s?){3,}',  # Multiple mentions
            r'(#\w+\s?){5,}',  # Multiple hashtags
            r'(https?://[^\s]+\s?){3,}',  # Multiple links
            r'(buy|shop|order|purchase|खरीदें|வாங்க|కొనండి)'  # Promotional
        ]
    
    def extract_profile_features(self, profile_data):
        """
        Extract features from social media profile
        """
        features = {}
        
        # Extract profile fields
        username = profile_data.get('username', '')
        name = profile_data.get('name', '')
        bio = profile_data.get('bio', profile_data.get('description', ''))
        followers = profile_data.get('followers', 0)
        following = profile_data.get('following', 0)
        posts = profile_data.get('posts', profile_data.get('tweets', 0))
        account_age = profile_data.get('account_age', 0)
        is_verified = profile_data.get('is_verified', 0)
        profile_pic = profile_data.get('has_profile_pic', 1)
        
        # Username analysis
        if username:
            features['username_length'] = len(username)
            features['username_has_numbers'] = int(any(c.isdigit() for c in username))
            features['username_has_special'] = int(any(not c.isalnum() for c in username))
            features['username_numbers_ratio'] = sum(c.isdigit() for c in username) / len(username)
            
            # Check for default username patterns
            features['username_looks_auto'] = int(bool(re.match(r'user_\d+|user\d+', username.lower())))
        
        # Name analysis
        if name:
            features['name_length'] = len(name)
            features['name_has_numbers'] = int(any(c.isdigit() for c in name))
            features['name_all_caps'] = int(name.isupper() and len(name) > 3)
            
            # Check suspicious name patterns
            for pattern in self.profile_red_flags['name_patterns']:
                if re.search(pattern, name):
                    features['name_suspicious_pattern'] = 1
        else:
            features['name_missing'] = 1
        
        # Bio analysis
        if bio:
            features['bio_length'] = len(bio)
            features['bio_has_emoji'] = int(bool(re.search(r'[\U0001F600-\U0001F64F]', bio)))
            
            # Check bio for suspicious patterns
            for pattern in self.profile_red_flags['bio_patterns']:
                if pattern in bio.lower():
                    features['bio_suspicious'] = 1
            
            # Check for links in bio
            features['bio_has_link'] = int('http' in bio or 'www.' in bio)
            
            # Check for promotional content
            for pattern in self.bot_patterns:
                if re.search(pattern, bio.lower()):
                    features['bio_promotional'] = 1
            
            # Extract language from bio
            if bio:
                lang, conf, _ = self.language_detector.detect_language(bio)
                features['bio_language'] = lang
                features['bio_language_confidence'] = conf
        else:
            features['bio_missing'] = 1
        
        # Follower/Following analysis
        if followers > 0 or following > 0:
            features['followers'] = followers
            features['following'] = following
            features['total_engagement'] = followers + following
            
            if following > 0:
                features['follower_following_ratio'] = followers / following
                features['following_too_high'] = int(following > 1000 and followers < 100)
            
            if followers > 0:
                features['followers_too_high'] = int(followers > 10000 and following < 10)
        
        # Posts analysis
        if posts > 0:
            features['posts_count'] = posts
            
            # Posts per day (if account age available)
            if account_age > 0:
                features['posts_per_day'] = posts / account_age
                features['too_many_posts'] = int(posts / account_age > 10)  # Bot-like posting
                features['too_few_posts'] = int(posts / account_age < 0.01)  # Dormant account
        
        # Account age
        if account_age > 0:
            features['account_age_days'] = account_age
            features['new_account'] = int(account_age < 7)  # Less than a week
            features['very_new_account'] = int(account_age < 1)  # Less than a day
        
        # Verification and profile completeness
        features['is_verified'] = is_verified
        features['has_profile_pic'] = profile_pic
        features['profile_completeness'] = sum([
            profile_pic,
            bool(name),
            bool(bio),
            bool(username)
        ]) / 4.0
        
        return features
    
    def extract_post_features(self, posts):
        """
        Extract features from user's posts
        """
        features = {}
        
        if not posts or len(posts) == 0:
            features['has_posts'] = 0
            return features
        
        features['has_posts'] = 1
        
        # Combine all posts
        all_posts_text = ' '.join([str(post.get('text', '')) for post in posts])
        all_posts_text_lower = all_posts_text.lower()
        
        # Post frequency patterns
        timestamps = [post.get('timestamp', 0) for post in posts if post.get('timestamp')]
        if len(timestamps) > 1:
            time_diffs = np.diff(sorted(timestamps))
            features['avg_time_between_posts'] = np.mean(time_diffs) if len(time_diffs) > 0 else 0
            features['post_regularity'] = np.std(time_diffs) / max(np.mean(time_diffs), 1)  # Lower = more regular (bots)
        
        # Content analysis
        features['total_posts_text_length'] = len(all_posts_text)
        
        # Hashtag analysis
        hashtags = re.findall(r'#(\w+)', all_posts_text)
        features['num_hashtags'] = len(hashtags)
        features['unique_hashtags'] = len(set(hashtags))
        features['hashtag_reuse_ratio'] = features['num_hashtags'] / max(features['unique_hashtags'], 1)
        
        # Mention analysis
        mentions = re.findall(r'@(\w+)', all_posts_text)
        features['num_mentions'] = len(mentions)
        features['unique_mentions'] = len(set(mentions))
        
        # Link analysis
        links = re.findall(r'https?://[^\s]+', all_posts_text)
        features['num_links'] = len(links)
        features['unique_links'] = len(set(links))
        
        # Check for suspicious links
        for link_pattern in self.profile_red_flags['suspicious_links']:
            if link_pattern in all_posts_text_lower:
                features['has_suspicious_links'] = 1
        
        # Language diversity in posts
        if all_posts_text:
            lang, conf, _ = self.language_detector.detect_language(all_posts_text)
            features['posts_primary_language'] = lang
        
        return features
    
    def extract_all_features(self, profile_data, posts=None):
        """
        Extract ALL features for social media fraud detection
        """
        features = {}
        
        # Extract profile features
        features.update(self.extract_profile_features(profile_data))
        
        # Extract post features if available
        if posts:
            features.update(self.extract_post_features(posts))
        
        # Get multilingual features from bio
        bio = profile_data.get('bio', profile_data.get('description', ''))
        if bio:
            bio_features = self.multilingual_utils.extract_all_features(bio)
            # Add key bio features
            features['bio_has_code_mixed'] = bio_features.get('code_mixed', 0)
            features['bio_has_indic_script'] = bio_features.get('script_devanagari_present', 0) or \
                                               bio_features.get('script_tamil_present', 0) or \
                                               bio_features.get('script_telugu_present', 0)
        
        return features
    
    def prepare_training_data(self):
        """
        Prepare feature matrix for model training
        """
        if self.df.empty:
            print("⚠️ No social media data available for training")
            return np.array([]), np.array([])
        
        print("📊 Preparing multilingual social media training data...")
        
        all_features = []
        labels = []
        
        for idx, row in self.df.iterrows():
            # Convert row to profile dict
            profile_data = {
                'username': row.get('username', ''),
                'name': row.get('name', row.get('display_name', '')),
                'bio': row.get('bio', row.get('description', '')),
                'followers': row.get('followers', 0),
                'following': row.get('following', 0),
                'posts': row.get('posts', row.get('tweets', row.get('statuses_count', 0))),
                'account_age': row.get('account_age', row.get('account_age_days', 0)),
                'is_verified': row.get('is_verified', 0),
                'has_profile_pic': row.get('has_profile_pic', row.get('default_profile', 1))
            }
            label = row.get('fake', row.get('bot', row.get('label', 0)))
            
            # For posts, if available in data
            posts = None
            if 'posts_data' in row and row['posts_data']:
                # Parse posts data if stored as JSON
                try:
                    posts = eval(row['posts_data']) if isinstance(row['posts_data'], str) else row['posts_data']
                except:
                    posts = None
            
            # Extract features
            features = self.extract_all_features(profile_data, posts)
            
            # Flatten features into vector
            feature_vector = []
            for key, value in features.items():
                if isinstance(value, (int, float)):
                    feature_vector.append(value)
                elif key == 'bio_language' and isinstance(value, str):
                    # One-hot encode bio language
                    for lang in ['hindi', 'marathi', 'tamil', 'telugu', 'kannada', 
                               'malayalam', 'gujarati', 'bengali', 'punjabi', 'hinglish', 'english']:
                        feature_vector.append(1 if value == lang else 0)
            
            all_features.append(feature_vector)
            labels.append(label)
            
            if idx % 100 == 0:
                print(f"  Processed {idx} profiles...")
        
        if all_features:
            # Pad vectors to same length
            max_len = max(len(v) for v in all_features)
            X_padded = np.array([v + [0] * (max_len - len(v)) for v in all_features])
            y = np.array(labels)
            print(f"✅ Social media training data prepared: {X_padded.shape}")
            return X_padded, y
        else:
            print("⚠️ No features extracted from social media data")
            return np.array([]), np.array([])
    
    def save_scaler(self):
        """
        Save feature scaler for social media features
        """
        from sklearn.preprocessing import StandardScaler
        
        # Prepare features for scaling
        X, _ = self.prepare_training_data()
        
        if X.size > 0:
            scaler = StandardScaler()
            scaler.fit(X)
            
            os.makedirs(FEATURE_PATH, exist_ok=True)
            joblib.dump(scaler, os.path.join(FEATURE_PATH, "social_media_scaler.pkl"))
            
            # Also save language detector
            joblib.dump(self.language_detector, os.path.join(FEATURE_PATH, "social_language_detector.pkl"))
            
            print("✅ Social media scaler saved successfully")
        else:
            print("⚠️ No data to fit scaler")


# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("MULTILINGUAL SOCIAL MEDIA FEATURE ENGINEERING")
    print("=" * 80)
    
    # Initialize extractor
    extractor = MultilingualSocialMediaFeatureExtractor()
    
    # Test on sample profiles
    test_profiles = [
        {
            'profile_data': {
                'username': 'priya_singh_23',
                'name': 'Priya Singh',
                'bio': 'सिंगल और रेडी टू मैरिज 💕 DM me for friendship प्यार के लिए तैयार',
                'followers': 15000,
                'following': 120,
                'posts': 45,
                'account_age': 30,
                'is_verified': 0,
                'has_profile_pic': 1
            },
            'posts': [
                {'text': 'मुझे सच्चा प्यार चाहिए 💕 DM me', 'timestamp': 1},
                {'text': 'कोई है जो मुझसे प्यार करेगा?', 'timestamp': 2},
                {'text': 'आज बहुत अकेला feel हो रहा है', 'timestamp': 3}
            ]
        },
        {
            'profile_data': {
                'username': 'crypto_king_india',
                'name': 'Crypto King',
                'bio': 'बिटकॉइन में निवेश करें और पैसे दोगुने करें। लिंक इन बायो 👆 गारंटीड प्रॉफिट',
                'followers': 500,
                'following': 1500,
                'posts': 120,
                'account_age': 5,
                'is_verified': 0,
                'has_profile_pic': 0
            },
            'posts': [
                {'text': 'नया ऑफर - 1 महीने में पैसे दोगुने', 'timestamp': 1},
                {'text': 'जल्दी करें सीमित सीटें bit.ly/invest-now', 'timestamp': 2},
                {'text': 'मेरे 100 क्लाइंट ने प्रॉफिट कमाया', 'timestamp': 3},
                {'text': 'व्हाट्सएप ग्रुप से जुड़ें लिंक इन बायो', 'timestamp': 4}
            ]
        },
        {
            'profile_data': {
                'username': 'real_ananya_offl',
                'name': 'Ananya Sharma',
                'bio': 'Travel | Fashion | Lifestyle 📍Mumbai',
                'followers': 25000,
                'following': 850,
                'posts': 320,
                'account_age': 365,
                'is_verified': 1,
                'has_profile_pic': 1
            },
            'posts': [
                {'text': 'Beautiful day at Marine Drive! #mumbai #sunset', 'timestamp': 100},
                {'text': 'New blog post - check link in bio', 'timestamp': 200}
            ]
        }
    ]
    
    print("\n🔍 TESTING SOCIAL MEDIA FEATURE EXTRACTION:\n")
    
    for i, test in enumerate(test_profiles, 1):
        print(f"Test Profile {i}: {test['profile_data']['username']}")
        features = extractor.extract_all_features(
            test['profile_data'],
            test.get('posts')
        )
        
        # Show key features
        print(f"  Bio language: {features.get('bio_language', 'unknown')}")
        print(f"  Profile completeness: {features.get('profile_completeness', 0):.2f}")
        print(f"  Follower/Following ratio: {features.get('follower_following_ratio', 0):.2f}")
        print(f"  New account: {features.get('new_account', 0)}")
        print(f"  Bio has link: {features.get('bio_has_link', 0)}")
        print(f"  Has posts: {features.get('has_posts', 0)}")
        print("-" * 60)
    
    # Save scaler
    print("\n💾 Saving scaler...")
    extractor.save_scaler()
    
    print("\n✅ Social media feature engineering module ready!")