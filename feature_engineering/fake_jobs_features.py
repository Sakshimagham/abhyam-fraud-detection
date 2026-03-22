# feature_engineering/fake_jobs_features.py
"""
Enhanced Fake Job Posting Feature Engineering with Multilingual Support
Detects job scams in multiple Indian languages
"""

import os
import pandas as pd
import joblib
import numpy as np
import re
from .multilingual_utils import MultilingualFeatureExtractor
from .language_detector import IndianLanguageDetector

BASE_PATH = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system"
DATA_PATH = os.path.join(BASE_PATH, "data", "processed", "fake_jobs_preprocessed.csv")
FEATURE_PATH = os.path.join(BASE_PATH, "feature_engineering")

class MultilingualFakeJobsFeatureExtractor:
    """
    Enhanced fake job posting feature extractor with multilingual support
    """
    
    def __init__(self):
        # Load job data
        if os.path.exists(DATA_PATH):
            self.df = pd.read_csv(DATA_PATH)
            # Handle missing values
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].fillna("")
        else:
            print(f"⚠️ Job data not found at {DATA_PATH}")
            self.df = pd.DataFrame()
        
        # Initialize multilingual utilities
        self.multilingual_utils = MultilingualFeatureExtractor()
        self.language_detector = IndianLanguageDetector()
        
        # Job scam keywords in Indian languages
        self.job_scam_keywords = {
            'marathi': {
                'red_flags': ['फी', 'पैसे भरा', 'रजिस्ट्रेशन फी', 'प्रोसेसिंग फी', 'ट्रेनिंग फी'],
                'too_good': ['जास्त पगार', 'घर बसल्या काम', 'कोणतीही पदवी नको', 'एक्सपीरियंस नको'],
                'pressure': ['तातडीचे', 'आजच अर्ज करा', 'मर्यादित जागा', 'शेवटची संधी'],
                'company': ['कंपनीचे नाव नाही', 'विदेशी कंपनी', 'मोठी कंपनी']
            },
            'hindi': {
                'red_flags': ['फीस', 'पैसे भरें', 'रजिस्ट्रेशन फीस', 'प्रोसेसिंग फीस', 'ट्रेनिंग फीस'],
                'too_good': ['ऊंची सैलरी', 'घर बैठे काम', 'बिना डिग्री', 'बिना एक्सपीरियंस'],
                'pressure': ['तुरंत', 'आज ही आवेदन करें', 'सीमित सीटें', 'आखिरी मौका'],
                'company': ['कंपनी का नाम नहीं', 'विदेशी कंपनी', 'बड़ी कंपनी']
            },
            'tamil': {
                'red_flags': ['கட்டணம்', 'பணம் செலுத்தவும்', 'பதிவுக் கட்டணம்', 'செயலாக்கக் கட்டணம்'],
                'too_good': ['அதிக சம்பளம்', 'வீட்டிலிருந்து வேலை', 'தகுதி தேவையில்லை', 'அனுபவம் தேவையில்லை'],
                'pressure': ['அவசரம்', 'இன்றே விண்ணப்பிக்கவும்', 'குறைந்த இடங்கள்', 'கடைசி வாய்ப்பு'],
                'company': ['நிறுவனப் பெயர் இல்லை', 'வெளிநாட்டு நிறுவனம்']
            },
            'telugu': {
                'red_flags': ['ఫీజు', 'డబ్బు చెల్లించండి', 'రిజిస్ట్రేషన్ ఫీజు', 'ప్రాసెసింగ్ ఫీజు'],
                'too_good': ['ఎక్కువ జీతం', 'ఇంటి నుంచి పని', 'డిగ్రీ అవసరం లేదు', 'అనుభవం అవసరం లేదు'],
                'pressure': ['అత్యవసరం', 'ఈరోజే దరఖాస్తు చేయండి', 'పరిమిత సీట్లు', 'చివరి అవకాశం'],
                'company': ['కంపెనీ పేరు లేదు', 'విదేశీ కంపెనీ']
            },
            'kannada': {
                'red_flags': ['ಶುಲ್ಕ', 'ಹಣ ಪಾವತಿಸಿ', 'ನೋಂದಣಿ ಶುಲ್ಕ', 'ಸಂಸ್ಕರಣ ಶುಲ್ಕ'],
                'too_good': ['ಹೆಚ್ಚಿನ ಸಂಬಳ', 'ಮನೆಯಿಂದ ಕೆಲಸ', 'ಪದವಿ ಅಗತ್ಯವಿಲ್ಲ', 'ಅನುಭವ ಅಗತ್ಯವಿಲ್ಲ'],
                'pressure': ['ತುರ್ತು', 'ಇಂದೇ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ', 'ಸೀಮಿತ ಸ್ಥಾನಗಳು', 'ಕೊನೆಯ ಅವಕಾಶ'],
                'company': ['ಕಂಪನಿ ಹೆಸರು ಇಲ್ಲ', 'ವಿದೇಶಿ ಕಂಪನಿ']
            },
            'gujarati': {
                'red_flags': ['ફી', 'પૈસા ભરો', 'રજિસ્ટ્રેશન ફી', 'પ્રોસેસિંગ ફી'],
                'too_good': ['વધુ પગાર', 'ઘરેથી કામ', 'ડિગ્રી ન જોઈએ', 'અનુભવ ન જોઈએ'],
                'pressure': ['તાત્કાલિક', 'આજે જ અરજી કરો', 'મર્યાદિત બેઠકો', 'છેલ્લી તક'],
                'company': ['કંપનીનું નામ નથી', 'વિદેશી કંપની']
            },
            'bengali': {
                'red_flags': ['ফি', 'টাকা দিতে হবে', 'রেজিস্ট্রেশন ফি', 'প্রসেসিং ফি'],
                'too_good': ['উচ্চ বেতন', 'বাড়ি থেকে কাজ', 'ডিগ্রি দরকার নেই', 'অভিজ্ঞতা দরকার নেই'],
                'pressure': ['জরুরি', 'আজই আবেদন করুন', 'সীমিত আসন', 'শেষ সুযোগ'],
                'company': ['কোম্পানির নাম নেই', 'বিদেশি কোম্পানি']
            },
            'punjabi': {
                'red_flags': ['ਫੀਸ', 'ਪੈਸੇ ਭਰੋ', 'ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਫੀਸ', 'ਪ੍ਰੋਸੈਸਿੰਗ ਫੀਸ'],
                'too_good': ['ਉੱਚ ਤਨਖਾਹ', 'ਘਰ ਬੈਠੇ ਕੰਮ', 'ਡਿਗਰੀ ਦੀ ਲੋੜ ਨਹੀਂ', 'ਤਜਰਬੇ ਦੀ ਲੋੜ ਨਹੀਂ'],
                'pressure': ['ਜ਼ਰੂਰੀ', 'ਅੱਜ ਹੀ ਅਪਲਾਈ ਕਰੋ', 'ਸੀਮਤ ਸੀਟਾਂ', 'ਆਖਰੀ ਮੌਕਾ'],
                'company': ['ਕੰਪਨੀ ਦਾ ਨਾਮ ਨਹੀਂ', 'ਵਿਦੇਸ਼ੀ ਕੰਪਨੀ']
            }
        }
        
        # Common fake job patterns in India
        self.indian_job_scam_patterns = {
            'fee_based': [
                'registration fee', 'processing fee', 'training fee', 'security deposit',
                'फीस', 'फी', 'कட்டணம்', 'శుల్క', 'ಶುಲ್ಕ', 'ફી', 'ফি', 'ਫੀਸ'
            ],
            'whatsapp_telegram': [
                'whatsapp', 'telegram', 'व्हाट्सएप', 'टेलीग्राम', 'வாட்ஸ்அப்', 'టెలిగ్రామ్'
            ],
            'no_interview': [
                'direct joining', 'no interview', 'immediate joining',
                'बिना इंटरव्यू', 'நேரடி நியமனம்', 'నేరుగా చేరడం'
            ],
            'work_from_home': [
                'work from home', 'online work', 'part time', 'data entry',
                'घर से काम', 'वर्क फ्रॉम होम', 'வீட்டிலிருந்து வேலை'
            ],
            'unrealistic_salary': [
                '50,000', '1 lakh', '2 lakh', '5 lakh', '10 lakh',
                '50000', '1 लाख', '2 लाख', '5 लाख'
            ]
        }
        
        # Legitimate Indian companies (common in scams)
        self.legitimate_companies_misused = [
            'amazon', 'flipkart', 'google', 'microsoft', 'tcs', 'infosys', 'wipro',
            'hdfc', 'icici', 'sbi', 'reliance', 'tata', 'mahindra', 'airtel', 'jio'
        ]
        
        # Suspicious contact methods
        self.suspicious_contacts = [
            'gmail.com', 'yahoo.com', 'rediffmail.com', 'hotmail.com',  # Free emails
            'whatsapp', 'telegram', 'signal',  # Messaging apps
        ]
    
    def extract_job_specific_features(self, job_data):
        """
        Extract features from job posting data
        """
        features = {}
        
        # Extract fields from job_data dict
        title = job_data.get('title', '')
        description = job_data.get('description', '')
        company = job_data.get('company', '')
        location = job_data.get('location', '')
        salary = job_data.get('salary', '')
        email = job_data.get('email', '')
        phone = job_data.get('phone', '')
        requirements = job_data.get('requirements', '')
        
        # Combine text for analysis
        full_text = f"{title} {description} {requirements}".lower()
        
        # Check for red flags
        features['has_fee_mention'] = 0
        features['has_whatsapp_mention'] = 0
        features['has_no_interview_claim'] = 0
        features['has_work_from_home'] = 0
        features['unrealistic_salary'] = 0
        
        for pattern, keywords in self.indian_job_scam_patterns.items():
            for keyword in keywords:
                if keyword.lower() in full_text:
                    features[f'pattern_{pattern}'] = features.get(f'pattern_{pattern}', 0) + 1
        
        # Company name analysis
        if company:
            features['company_name_length'] = len(company)
            features['company_name_has_numbers'] = int(any(c.isdigit() for c in company))
            
            # Check if misusing legitimate company names
            for legit_company in self.legitimate_companies_misused:
                if legit_company in company.lower() and legit_company != company.lower():
                    features['misusing_legitimate_company'] = 1
                    break
        else:
            features['company_name_missing'] = 1
        
        # Email analysis
        if email:
            features['has_company_email'] = int('@' in email and not any(domain in email for domain in ['gmail', 'yahoo', 'hotmail', 'rediffmail']))
            features['has_free_email'] = int(any(domain in email for domain in ['gmail', 'yahoo', 'hotmail', 'rediffmail']))
        else:
            features['email_missing'] = 1
        
        # Phone analysis
        if phone:
            # Check for Indian phone number
            features['has_indian_phone'] = int(bool(re.search(r'(\+91|0)?[6-9]\d{9}', phone)))
        else:
            features['phone_missing'] = 1
        
        # Salary analysis
        if salary:
            # Extract numbers from salary
            salary_numbers = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', salary)
            if salary_numbers:
                max_salary = max([float(n.replace(',', '')) for n in salary_numbers])
                features['salary_max'] = max_salary
                features['unrealistic_salary_flag'] = int(max_salary > 1000000)  # > 10 lakhs suspicious for entry level
        else:
            features['salary_missing'] = 1
        
        # Location analysis
        if location:
            features['location_specified'] = 1
            # Check for foreign locations (common in scams)
            foreign_keywords = ['dubai', 'canada', 'usa', 'uk', 'australia', 'singapore']
            features['foreign_location'] = int(any(keyword in location.lower() for keyword in foreign_keywords))
        else:
            features['location_missing'] = 1
        
        return features
    
    def extract_all_features(self, job_data):
        """
        Extract ALL features for fake job detection
        """
        features = {}
        
        # Combine all text fields for multilingual analysis
        all_text = ' '.join([
            str(job_data.get('title', '')),
            str(job_data.get('description', '')),
            str(job_data.get('requirements', '')),
            str(job_data.get('company', ''))
        ])
        
        if all_text:
            # Get base multilingual features
            features.update(self.multilingual_utils.extract_all_features(all_text))
            
            # Add language-specific scam patterns
            detected_lang = features.get('detected_language', 'unknown')
            if detected_lang in self.job_scam_keywords:
                lang_patterns = self.job_scam_keywords[detected_lang]
                for category, keywords in lang_patterns.items():
                    matches = 0
                    for keyword in keywords:
                        if keyword in all_text:
                            matches += 1
                    features[f'job_{detected_lang}_{category}_score'] = matches / len(keywords)
        
        # Add job-specific features
        features.update(self.extract_job_specific_features(job_data))
        
        return features
    
    def prepare_training_data(self):
        """
        Prepare feature matrix for model training
        """
        if self.df.empty:
            print("⚠️ No job data available for training")
            return np.array([]), np.array([])
        
        print("📊 Preparing multilingual fake jobs training data...")
        
        all_features = []
        labels = []
        
        for idx, row in self.df.iterrows():
            # Convert row to dict
            job_data = {
                'title': row.get('title', ''),
                'description': row.get('description', row.get('job_description', '')),
                'company': row.get('company', row.get('company_name', '')),
                'location': row.get('location', ''),
                'salary': row.get('salary', row.get('salary_range', '')),
                'email': row.get('email', row.get('contact_email', '')),
                'phone': row.get('phone', row.get('contact_phone', '')),
                'requirements': row.get('requirements', row.get('qualifications', ''))
            }
            label = row.get('fraudulent', row.get('label', 0))
            
            # Extract features
            features = self.extract_all_features(job_data)
            
            # Flatten features into vector
            feature_vector = []
            for key, value in features.items():
                if isinstance(value, (int, float)):
                    feature_vector.append(value)
            
            all_features.append(feature_vector)
            labels.append(label)
            
            if idx % 100 == 0:
                print(f"  Processed {idx} job postings...")
        
        if all_features:
            # Pad vectors to same length
            max_len = max(len(v) for v in all_features)
            X_padded = np.array([v + [0] * (max_len - len(v)) for v in all_features])
            y = np.array(labels)
            print(f"✅ Jobs training data prepared: {X_padded.shape}")
            return X_padded, y
        else:
            print("⚠️ No features extracted from job data")
            return np.array([]), np.array([])
    
    def save_vectorizers(self):
        """
        Save vectorizers for job features
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import StandardScaler
        
        # Text vectorizer for job descriptions
        if not self.df.empty:
            # Combine title and description for vectorizer
            texts = []
            for _, row in self.df.iterrows():
                text = f"{row.get('title', '')} {row.get('description', row.get('job_description', ''))}"
                texts.append(text)
            
            if texts:
                vectorizer = TfidfVectorizer(max_features=2000)
                vectorizer.fit(texts)
                
                os.makedirs(FEATURE_PATH, exist_ok=True)
                joblib.dump(vectorizer, os.path.join(FEATURE_PATH, "fake_jobs_vectorizer.pkl"))
                
                # Also save language detector
                joblib.dump(self.language_detector, os.path.join(FEATURE_PATH, "jobs_language_detector.pkl"))
                
                print("✅ Jobs vectorizers saved successfully")
        else:
            print("⚠️ No text data to fit vectorizer")


# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("MULTILINGUAL FAKE JOBS FEATURE ENGINEERING")
    print("=" * 80)
    
    # Initialize extractor
    extractor = MultilingualFakeJobsFeatureExtractor()
    
    # Test on sample job postings
    test_jobs = [
        {
            'title': 'बँक में नौकरी - घर बैठे काम',
            'description': 'बिना इंटरव्यू सीधी भर्ती। रजिस्ट्रेशन फीस ₹500 जमा करें। व्हाट्सएप ग्रुप से जुड़ें।',
            'company': 'Unknown Services',
            'location': 'Work from home',
            'salary': '₹50,000 per month',
            'email': 'hr.jobs@gmail.com',
            'phone': '9876543210'
        },
        {
            'title': 'வங்கி வேலை - நேரடி நியமனம்',
            'description': 'பதிவுக் கட்டணம் ₹1000 செலுத்தவும். நேர்காணல் இல்லை. உடனடி சேர்வு.',
            'company': 'Banking Services',
            'location': 'Chennai',
            'salary': '₹35,000 - 45,000',
            'email': 'careers@banking.in',
            'phone': '+919876543210'
        },
        {
            'title': 'Software Developer at Google',
            'description': 'Google is hiring freshers. Submit registration fee of ₹2000 for processing.',
            'company': 'Google India',
            'location': 'Bengaluru',
            'salary': '15 LPA',
            'email': 'hr.googl@gmail.com',
            'phone': '9876543210'
        }
    ]
    
    print("\n🔍 TESTING JOB FEATURE EXTRACTION:\n")
    
    for i, job in enumerate(test_jobs, 1):
        print(f"Test Job {i}: {job['title']}")
        features = extractor.extract_all_features(job)
        
        # Show key features
        print(f"  Language: {features.get('detected_language', 'unknown')}")
        print(f"  Has fee mention: {features.get('has_fee_mention', 0)}")
        print(f"  Has WhatsApp: {features.get('has_whatsapp_mention', 0)}")
        print(f"  Company name missing: {features.get('company_name_missing', 0)}")
        print(f"  Free email used: {features.get('has_free_email', 0)}")
        print(f"  Unrealistic salary: {features.get('unrealistic_salary_flag', 0)}")
        print("-" * 60)
    
    # Save vectorizers
    print("\n💾 Saving vectorizers...")
    extractor.save_vectorizers()
    
    print("\n✅ Fake jobs feature engineering module ready!")