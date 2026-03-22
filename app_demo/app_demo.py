# app_demo/app.py
"""
Complete Multilingual Fraud Detection System Frontend
Supports 10+ Indian languages with regional context
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
import json
import joblib
from datetime import datetime
import base64
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feature_engineering.feature_router import get_feature_router
from risk_engine.rule_engine import MultilingualRuleEngine
from risk_engine.rule_config import HELPLINE_NUMBERS, RESPONSE_TEMPLATES
from feature_engineering.language_detector import IndianLanguageDetector

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="भारत सुरक्षा | Bharat Suraksha",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD TRAINED MODELS (with caching)
# ============================================
@st.cache_resource
def load_models():
    models = {}
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_path = os.path.join(base_path, "models")
    
    model_files = {
        'sms': 'sms_model.pkl',
        'call': 'call_model.pkl',
        'crypto': 'crypto_model.pkl',
        'job': 'fake_jobs_model.pkl',
        'social': 'social_media_model.pkl',
        'website': 'web_model.pkl'
    }
    scaler_files = {
        'sms': 'sms_scaler.pkl',
        'call': 'call_scaler.pkl',
        'crypto': 'crypto_scaler.pkl',
        'job': 'fake_jobs_scaler.pkl',
        'social': 'social_media_scaler.pkl',
        'website': 'web_scaler.pkl'
    }
    
    for fraud_type, filename in model_files.items():
        model_path = os.path.join(models_path, filename)
        scaler_path = os.path.join(models_path, scaler_files[fraud_type])
        if os.path.exists(model_path):
            try:
                model_data = {
                    'model': joblib.load(model_path),
                    'scaler': joblib.load(scaler_path) if os.path.exists(scaler_path) else None
                }
                models[fraud_type] = model_data
                print(f"✅ Loaded {fraud_type} model")
            except Exception as e:
                print(f"❌ Error loading {fraud_type} model: {e}")
                models[fraud_type] = None
        else:
            print(f"⚠️ Model not found: {model_path}")
            models[fraud_type] = None
    return models

# ============================================
# INITIALIZATION
# ============================================
@st.cache_resource
def init_system():
    """Initialize all system components"""
    try:
        router = get_feature_router()
        rule_engine = MultilingualRuleEngine()
        language_detector = IndianLanguageDetector()
        models = load_models()
        print("✅ System initialized successfully")
        return router, rule_engine, language_detector, models
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        st.error(f"System initialization error: {e}")
        return None, None, None, None

router, rule_engine, language_detector, models = init_system()

# ============================================
# LANGUAGE SUPPORT
# ============================================
LANGUAGES = {
    'english': {'name': 'English', 'flag': '🇬🇧', 'native_name': 'English'},
    'hindi': {'name': 'हिंदी', 'flag': '🇮🇳', 'native_name': 'हिंदी'},
    'marathi': {'name': 'मराठी', 'flag': '🇮🇳', 'native_name': 'मराठी'},
    'tamil': {'name': 'தமிழ்', 'flag': '🇮🇳', 'native_name': 'தமிழ்'},
    'telugu': {'name': 'తెలుగు', 'flag': '🇮🇳', 'native_name': 'తెలుగు'},
    'kannada': {'name': 'ಕನ್ನಡ', 'flag': '🇮🇳', 'native_name': 'ಕನ್ನಡ'},
    'malayalam': {'name': 'മലയാളം', 'flag': '🇮🇳', 'native_name': 'മലയാളം'},
    'gujarati': {'name': 'ગુજરાતી', 'flag': '🇮🇳', 'native_name': 'ગુજરાતી'},
    'bengali': {'name': 'বাংলা', 'flag': '🇮🇳', 'native_name': 'বাংলা'},
    'punjabi': {'name': 'ਪੰਜਾਬੀ', 'flag': '🇮🇳', 'native_name': 'ਪੰਜਾਬੀ'},
}

# ============================================
# TRANSLATION DICTIONARY (English only for UI)
# ============================================
TRANSLATIONS = {
    'english': {
        'app_name': 'BHARAT SURAKSHA',
        'app_subtitle': "INDIA'S 1ST MULTILINGUAL FRAUD DETECTION SYSTEM",
        'tagline': 'Protecting 1.4 Billion Indians in Their Own Language',
        'detector': '🔍 DETECTOR',
        'learn': '🎓 LEARN',
        'help': '🆘 HELP',
        'stats': '📊 STATS',
        'community': '👥 COMMUNITY',
        'about': 'ℹ️ ABOUT',
        'language': '🌐 Language',
        'fraud_type': '🎯 Fraud Type',
        'today_stats': '📊 Today\'s Stats',
        'scans_today': 'Scans Today',
        'frauds_blocked': 'Frauds Blocked',
        'active_users': 'Active Users',
        'languages': 'Languages',
        'sms': '📱 SMS/Email',
        'call': '📞 Call',
        'crypto': '💰 Crypto',
        'job': '💼 Fake Job',
        'social': '👥 Social Media',
        'website': '🌐 Website',
        'enter_sms': '📝 Enter SMS/Message',
        'sender_id': '📱 Sender ID (optional)',
        'enter_transcript': '📞 Call Transcript',
        'duration': '⏱️ Duration (seconds)',
        'caller_id': '📞 Caller ID',
        'crypto_message': '💰 Crypto Message',
        'url': '🔗 URL (if any)',
        'job_title': '📌 Job Title',
        'company_name': '🏢 Company Name',
        'job_description': '📄 Job Description',
        'contact_email': '📧 Contact Email',
        'username': '👤 Username',
        'followers': '👥 Followers',
        'bio': '📝 Bio',
        'following': '🔁 Following',
        'posts': '📸 Posts',
        'website_url': '🌐 Website URL',
        'page_title': '📌 Page Title',
        'trust_data': '🔒 Trust Data (if available)',
        'domain_age': '📅 Domain Age (days)',
        'has_ssl': '🔐 Has SSL/HTTPS',
        'has_contact': '📞 Has Contact Page',
        'detect_language': '🔍 DETECT LANGUAGE',
        'check_fraud': '🚨 CHECK FOR FRAUD',
        'high_risk': '🚨 HIGH RISK DETECTED!',
        'medium_risk': '⚠️ MEDIUM RISK',
        'low_risk': '✅ LOW RISK',
        'risk_score': 'Risk Score',
        'action_steps': '📋 Action Steps',
        'detailed_analysis': '🔍 Detailed Analysis',
        'helplines': '📞 Helplines',
        'share_alert': '📤 Share Alert',
        'detected_language': '✅ Detected Language',
        'confidence': 'Confidence',
        'unknown_language': 'Unknown',
        'education_center': '🎓 FRAUD EDUCATION CENTER',
        'common_scams': '📱 Common Scams',
        'kyc_scams': '🚨 KYC Scams',
        'otp_fraud': '🚨 OTP Fraud',
        'digital_arrest': '🚨 Digital Arrest',
        'lottery_scams': '🚨 Lottery Scams',
        'job_scams': '🚨 Job Scams',
        'how_to_protect': '🛡️ How to Protect',
        'never_share_otp': '✅ Never share OTP',
        'verify_caller': '✅ Verify caller ID',
        'check_urls': '✅ Check URLs carefully',
        'dont_pay_jobs': '✅ Don\'t pay for jobs',
        'report_immediately': '✅ Report immediately',
        'who_to_contact': '📞 Who to Contact',
        'cyber_crime': '🚔 Cyber Crime: 1930',
        'police': '👮 Police: 100',
        'ambulance': '🚑 Ambulance: 102',
        'women': '👩 Women: 1091',
        'child': '🧒 Child: 1098',
        'video_tutorials': '🎥 Video Tutorials',
        'emergency_helplines': '🆘 EMERGENCY HELPLINES',
        'national_helplines': '🇮🇳 NATIONAL HELPLINES',
        'state_cyber_cells': '📍 STATE-WISE CYBER CELLS',
        'select_state': 'Select State',
        'live_statistics': '📊 LIVE FRAUD STATISTICS',
        'total_scams': 'Total Scams Reported',
        'amount_saved': 'Amount Saved',
        'detection_accuracy': 'Detection Accuracy',
        'languages_supported': 'Languages Supported',
        'fraud_by_type': 'Fraud by Type',
        'trending_scams': 'Trending Scams',
        'community_forum': '👥 COMMUNITY FORUM',
        'recent_discussions': 'Recent Discussions',
        'share_story': 'Share Your Story',
        'join_discussion': 'Join Discussion',
        'about_project': 'ℹ️ ABOUT THE PROJECT',
        'project_description': 'Bharat Suraksha is India\'s first multilingual fraud detection system...',
        'creator': '👨‍💻 Created by',
        'guide': '👩‍🏫 Guided by',
        'institution': '🏛️ Institution',
        'technologies': '🔧 Technologies Used',
        'contact': '📧 Contact',
        'footer_text': '🇮🇳 भारत सुरक्षा - Protecting India from Fraud | 12 Indian Languages | 24x7 Free Service',
        'footer_helpline': '📞 National Cyber Crime Helpline: 1930 | 📧 report@cybercrime.gov.in',
        'footer_copyright': '© 2024 Bharat Suraksha - MSc Data Science & AI Project',
        'sms_placeholder': 'Paste any suspicious message here...\n\nExample: तुमचे बँक खाते बंद होणार आहे. लगेच KYC अपडेट करा: bit.ly/bankupdate',
        'call_placeholder': 'Paste the call transcript here...\n\nExample: Caller: मी पोलीस अधिकारी बोलतोय. तुमच्यावर केस आहे.',
        'crypto_placeholder': 'Enter crypto investment message...\n\nExample: बिटकॉइन में निवेश करें और 1 महीने में पैसे दोगुने करें',
        'url_placeholder': 'bit.ly/crypto-double or https://crypto-site.xyz',
        'job_placeholder': 'Paste job description here...\n\nExample: No experience required, registration fee ₹500',
        'bio_placeholder': 'Paste profile bio here...\n\nExample: बिटकॉइन गुरु। पैसे दोगुने करें। लिंक इन बायो',
        'website_placeholder': 'https://example.com or https://sbi-secure-login.xyz',
    }
}

# For other languages, fallback to English (can be extended)
for lang in ['marathi','hindi', 'tamil', 'telugu', 'kannada', 'malayalam', 'gujarati', 'bengali', 'punjabi']:
    TRANSLATIONS[lang] = TRANSLATIONS['english'].copy()

# ============================================
# MULTILINGUAL EXAMPLE SCAMS (for demo)
# ============================================
EXAMPLE_SCAMS = {
    'मराठी': "तुमचे बँक खाते बंद होणार आहे. लगेच KYC अपडेट करा: bit.ly/bankupdate",
    'हिंदी': "आपका बैंक खाता बंद हो रहा है। तुरंत OTP देकर KYC अपडेट करें",
    'தமிழ்': "உங்கள் வங்கி கணக்கு மூடப்படும். உடனே OTP பகிரவும்",
    'తెలుగు': "మీ బ్యాంక్ ఖాతా మూసివేయబడుతుంది. వెంటనే OTP షేర్ చేయండి",
    'ಕನ್ನಡ': "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಯನ್ನು ಮುಚ್ಚಲಾಗುವುದು. ತಕ್ಷಣ OTP ಹಂಚಿಕೊಳ್ಳಿ",
    'മലയാളം': "നിങ്ങളുടെ ബാങ്ക് അക്കൗണ്ട് അടച്ചുപൂട്ടും. ഉടൻ OTP ഷെയർ ചെയ്യുക",
    'ગુજરાતી': "તમારું બેંક ખાતું બંધ થશે. તરત OTP શેર કરો",
    'বাংলা': "আপনার ব্যাঙ্ক অ্যাকাউন্ট বন্ধ হয়ে যাবে। এখনই OTP শেয়ার করুন",
    'ਪੰਜਾਬੀ': "ਤੁਹਾਡਾ ਬੈਂਕ ਖਾਤਾ ਬੰਦ ਹੋ ਜਾਵੇਗਾ। ਤੁਰੰਤ OTP ਸਾਂਝਾ ਕਰੋ",
}

# ============================================
# CUSTOM CSS (unchanged – keep your existing CSS)
# ============================================
st.markdown("""
<style>
    /* Your existing CSS – copy from your current file */
    :root {
        --primary: #FF6B35;
        --secondary: #00F0FF;
        --dark: #0B1026;
        --light: #F5F5F5;
        --danger: #FF0000;
        --success: #00FF00;
        --warning: #FFFF00;
        --saffron: #FF9933;
        --green: #138808;
        --navy: #000080;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0B1026 0%, #1a1f3a 100%);
        color: white;
    }
    
    h1 {
        color: var(--primary) !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 10px var(--primary), 0 0 20px var(--secondary);
        margin-bottom: 1rem !important;
    }
    
    h2 {
        color: var(--secondary) !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        border-left: 5px solid var(--primary);
        padding-left: 1rem;
    }
    
    h3 {
        color: white !important;
        font-size: 1.8rem !important;
    }
    
    .fraud-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid var(--primary);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.3);
        transition: transform 0.3s;
    }
    
    .fraud-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 0 50px rgba(255, 107, 53, 0.5);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--primary) 0%, #ff8c5a 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 107, 53, 0.5);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        color: white;
    }
    
    .metric-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, var(--primary), var(--secondary)) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 0.75rem 2rem !important;
        border: none !important;
        border-radius: 50px !important;
        box-shadow: 0 0 20px var(--primary) !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 40px var(--primary) !important;
    }
    
    .risk-high {
        background: linear-gradient(90deg, #ff0000, #ff4444);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    .risk-medium {
        background: linear-gradient(90deg, #ffaa00, #ffbb33);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
    }
    
    .risk-low {
        background: linear-gradient(90deg, #00ff00, #44ff44);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px #ff0000; }
        50% { box-shadow: 0 0 60px #ff0000; }
        100% { box-shadow: 0 0 20px #ff0000; }
    }
    
    .language-btn {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 2px solid var(--primary);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        margin: 0.2rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .language-btn:hover, .language-btn.active {
        background: var(--primary);
        transform: scale(1.05);
    }
    
    .helpline-box {
        background: linear-gradient(135deg, #000080, #0000ff);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-left: 5px solid var(--primary);
    }
    
    .helpline-number {
        font-size: 1.8rem;
        font-weight: 900;
        color: var(--primary);
        text-shadow: 0 0 10px var(--primary);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 20px;
        margin-top: 3rem;
    }
    
    .ticker-wrap {
        background: rgba(255, 107, 53, 0.2);
        padding: 1rem;
        border-radius: 50px;
        margin: 1rem 0;
        border: 1px solid var(--primary);
        overflow: hidden;
    }
    
    .ticker {
        animation: ticker 20s linear infinite;
        white-space: nowrap;
        display: inline-block;
    }
    
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary);
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
if 'language' not in st.session_state:
    st.session_state.language = 'english'
if 'detected_lang' not in st.session_state:
    st.session_state.detected_lang = 'english'
if 'fraud_type' not in st.session_state:
    st.session_state.fraud_type = 'sms'
if 'results' not in st.session_state:
    st.session_state.results = None
if 'history' not in st.session_state:
    st.session_state.history = []

# ============================================
# HELPER FUNCTION TO GET TRANSLATIONS
# ============================================
def t(key):
    """Get translated text for current language (falls back to English)"""
    lang = st.session_state.language
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    return TRANSLATIONS['english'].get(key, key)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem;">
        <h1 style="font-size: 2rem !important;">🛡️</h1>
        <h3 style="color: #FF6B35;">{t('app_name')}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Language selector
    st.markdown(f"### {t('language')}")
    
    lang_options = list(LANGUAGES.keys())
    selected_idx = lang_options.index(st.session_state.language) if st.session_state.language in lang_options else 0
    selected_lang = st.selectbox(
        "Select Language",
        options=lang_options,
        format_func=lambda x: f"{LANGUAGES[x]['flag']} {LANGUAGES[x]['name']}",
        index=selected_idx,
        label_visibility="collapsed"
    )
    
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    
    # Fraud type selector
    st.markdown(f"### {t('fraud_type')}")
    
    fraud_types = {
        'sms': {'icon': '📱', 'name_key': 'sms'},
        'call': {'icon': '📞', 'name_key': 'call'},
        'crypto': {'icon': '💰', 'name_key': 'crypto'},
        'job': {'icon': '💼', 'name_key': 'job'},
        'social': {'icon': '👥', 'name_key': 'social'},
        'website': {'icon': '🌐', 'name_key': 'website'}
    }
    
    for fraud_code, fraud_info in fraud_types.items():
        if st.button(
            f"{fraud_info['icon']} {t(fraud_info['name_key'])}",
            key=f"fraud_{fraud_code}",
            use_container_width=True,
            type="secondary" if st.session_state.fraud_type != fraud_code else "primary"
        ):
            st.session_state.fraud_type = fraud_code
            st.rerun()
    
    st.markdown("---")
    
    # Quick stats
    st.markdown(f"### {t('today_stats')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(t('scans_today'), "1,234", "+12%")
    with col2:
        st.metric(t('frauds_blocked'), "456", "+8%")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(t('active_users'), "5,678", "+23%")
    with col2:
        st.metric(t('languages'), "12", "🇮🇳")

# ============================================
# MAIN HEADER
# ============================================
if router is None or rule_engine is None:
    st.error("⚠️ System initialization failed. Please check your installation.")
    st.stop()

st.markdown(f"""
<div style="text-align: center; padding: 2rem;">
    <h1>🛡️ {t('app_subtitle')}</h1>
    <h3 style="color: #00F0FF;">{t('tagline')}</h3>
</div>
""", unsafe_allow_html=True)

# Stats bar
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-value">1,23,456</div>
        <div class="stat-label">{t('total_scams')}</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">₹45.6Cr</div>
        <div class="stat-label">{t('amount_saved')}</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">94%</div>
        <div class="stat-label">{t('detection_accuracy')}</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">12</div>
        <div class="stat-label">{t('languages_supported')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Alert ticker
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker">
        🚨 ALERT: KYC Scam in Mumbai • OTP Fraud in Chennai • Job Scam in Bengaluru • Digital Arrest in Delhi • Lottery Scam in Pune 🚨
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# TABS
# ============================================
tabs = st.tabs([
    t('detector'),
    t('learn'),
    t('help'),
    t('stats'),
    t('community'),
    t('about')
])

# ============================================
# TAB 1: DETECTOR
# ============================================
with tabs[0]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fraud_name_key = fraud_types[st.session_state.fraud_type]['name_key']
        st.markdown(f"""
        <div class="fraud-card">
            <h2>{fraud_types[st.session_state.fraud_type]['icon']} {t(fraud_name_key)} {t('detector')}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # ----- MULTILINGUAL DEMO BUTTONS -----
        st.markdown("### 🌐 Try an example in your language")
        cols = st.columns(5)
        for i, (lang, text) in enumerate(EXAMPLE_SCAMS.items()):
            with cols[i % 5]:
                if st.button(f"📝 {lang}", key=f"ex_{lang}"):
                    st.session_state['example_text'] = text
                    st.rerun()
        # --------------------------------------
        
        # Dynamic input fields based on fraud type
        input_data = {}
        
        if st.session_state.fraud_type == 'sms':
            default_text = st.session_state.get('example_text', '')
            input_data['text'] = st.text_area(
                t('enter_sms'),
                height=150,
                placeholder=t('sms_placeholder'),
                value=default_text,
                help="Works in ANY Indian language"
            )
            if default_text:
                st.session_state['example_text'] = ''
            input_data['sender_id'] = st.text_input(t('sender_id'), placeholder="BANKALERT, UNKNOWN")
            
        elif st.session_state.fraud_type == 'call':
            input_data['transcript'] = st.text_area(
                t('enter_transcript'),
                height=150,
                placeholder=t('call_placeholder'),
                help="Include speaker labels if possible"
            )
            col_a, col_b = st.columns(2)
            with col_a:
                input_data['duration'] = st.number_input(t('duration'), min_value=0, value=120)
            with col_b:
                input_data['caller_id'] = st.text_input(t('caller_id'), placeholder="+91XXXXXXXXXX")
                
        elif st.session_state.fraud_type == 'crypto':
            input_data['text'] = st.text_area(
                t('crypto_message'),
                height=100,
                placeholder=t('crypto_placeholder')
            )
            input_data['url'] = st.text_input(t('url'), placeholder=t('url_placeholder'))
            
        elif st.session_state.fraud_type == 'job':
            col_a, col_b = st.columns(2)
            with col_a:
                input_data['title'] = st.text_input(t('job_title'), placeholder="Work From Home")
            with col_b:
                input_data['company'] = st.text_input(t('company_name'), placeholder="Google, Amazon")
            
            input_data['description'] = st.text_area(
                t('job_description'),
                height=100,
                placeholder=t('job_placeholder')
            )
            input_data['email'] = st.text_input(t('contact_email'), placeholder="hr@example.com")
            
        elif st.session_state.fraud_type == 'social':
            col_a, col_b = st.columns(2)
            with col_a:
                input_data['username'] = st.text_input(t('username'), placeholder="@username")
            with col_b:
                input_data['followers'] = st.number_input(t('followers'), min_value=0, value=0)
            
            input_data['bio'] = st.text_area(
                t('bio'),
                height=100,
                placeholder=t('bio_placeholder')
            )
            
            col_c, col_d = st.columns(2)
            with col_c:
                input_data['following'] = st.number_input(t('following'), min_value=0, value=0)
            with col_d:
                input_data['posts'] = st.number_input(t('posts'), min_value=0, value=0)
                
        elif st.session_state.fraud_type == 'website':
            input_data['url'] = st.text_input(
                t('website_url'),
                placeholder=t('website_placeholder')
            )
            input_data['title'] = st.text_input(t('page_title'), placeholder="SBI - Secure Login")
            
            with st.expander(t('trust_data')):
                col_a, col_b = st.columns(2)
                with col_a:
                    input_data['domain_age'] = st.number_input(t('domain_age'), min_value=0, value=0)
                with col_b:
                    input_data['has_ssl'] = st.checkbox(t('has_ssl'), value=True)
                input_data['has_contact'] = st.checkbox(t('has_contact'), value=False)
        
        # Detect language button
        if st.button(t('detect_language'), use_container_width=True):
            text_to_analyze = ""
            for field in ['text', 'transcript', 'description', 'bio', 'title']:
                if field in input_data and input_data[field]:
                    text_to_analyze = input_data[field]
                    break
            
            if text_to_analyze and language_detector:
                try:
                    result = language_detector.detect_language(text_to_analyze)
                    if isinstance(result, tuple) and len(result) >= 2:
                        lang = result[0]
                        conf = result[1]
                        st.session_state.detected_lang = lang
                        lang_name = LANGUAGES.get(lang, {}).get('name', t('unknown_language'))
                        st.success(f"{t('detected_language')}: {lang_name} ({t('confidence')}: {conf:.2%})")
                    else:
                        st.info("Language detection complete")
                except Exception as e:
                    st.warning(f"Language detection error: {e}")
        
        # Check fraud button – uses ML for English, rule engine for others
        if st.button(t('check_fraud'), use_container_width=True, type="primary"):
            if any(input_data.values()):
                with st.spinner("🔍 Analyzing with AI models..."):
                    try:
                        features = router.extract_features(st.session_state.fraud_type, input_data)
                        detected_lang = features.get('detected_language', 'english')
                        
                        # --- Get ML prediction from trained model (if available and language is English) ---
                        ml_prob = 0.5  # default
                        model_source = "Rule Engine only"
                        fraud_type = st.session_state.fraud_type
                        
                        # Use ML only if detected language is English-like and model exists
                        if detected_lang in ['english', 'unknown_latin'] and fraud_type in models and models[fraud_type] is not None:
                            model_data = models[fraud_type]
                            model = model_data['model']
                            scaler = model_data['scaler']
                            
                            # Load feature names (saved during training)
                            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                            models_path = os.path.join(base_path, "models")
                            feature_names_path = os.path.join(models_path, f"{fraud_type}_feature_names.pkl")
                            
                            if os.path.exists(feature_names_path):
                                feature_names = joblib.load(feature_names_path)
                                # Create a DataFrame row aligned to training features
                                row_df = pd.DataFrame([features])          # 'features' is the dict we already extracted
                                row_df = row_df.reindex(columns=feature_names, fill_value=0)
                                feature_vector = row_df.values.astype(float)
                                source_detail = "aligned"
                            else:
                                # Fallback: use raw feature vector and force to expected size
                                feature_vector = router.get_feature_vector(fraud_type, input_data, model_type='ml')
                                feature_vector = feature_vector.reshape(1, -1)
                                # If dimensions still mismatch, pad or truncate to 163
                                if feature_vector.shape[1] != 163:
                                    if feature_vector.shape[1] > 163:
                                        feature_vector = feature_vector[:, :163]
                                    else:
                                        feature_vector = np.pad(feature_vector, ((0,0),(0,163-feature_vector.shape[1])), mode='constant')
                                source_detail = "fallback (padded/truncated)"
                            
                            # Scale if scaler exists
                            if scaler is not None:
                                feature_vector = scaler.transform(feature_vector)
                            
                            # Predict probability
                            if hasattr(model, 'predict_proba'):
                                proba = model.predict_proba(feature_vector)[0]
                                # Determine which class is fraud (usually 1)
                                if model.classes_[1] == 1:
                                    ml_prob = proba[1]
                                else:
                                    ml_prob = proba[0]
                            else:
                                pred = model.predict(feature_vector)[0]
                                ml_prob = 0.9 if pred == 1 else 0.1
                            model_source = f"ML Model (English, {source_detail})"
                        
                        # --- Rule engine score (always runs) ---
                        rule_score, reasons, helplines = rule_engine.calculate_risk(
                            fraud_type, 
                            input_data,
                            detected_lang
                        )
                        
                        # Combine: if ML used, 70% ML + 30% rules; else 100% rules
                        if model_source.startswith("ML"):
                            combined = (ml_prob * 0.7) + (min(rule_score / 100, 1.0) * 0.3)
                        else:
                            combined = min(rule_score / 100, 1.0)
                        
                        result = rule_engine.combine_risk(
                            combined, 
                            rule_score,
                            detected_lang,
                            features.get('is_code_mixed', False)
                        )
                        
                        st.session_state.results = {
                            'result': result,
                            'reasons': reasons,
                            'helplines': helplines,
                            'ml_prob': ml_prob,
                            'model_source': model_source,
                            'detected_lang': detected_lang
                        }
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter some data")
    
    with col2:
        if st.session_state.results:
            result = st.session_state.results['result']
            ml_prob = st.session_state.results.get('ml_prob', 0)
            model_source = st.session_state.results.get('model_source', 'Unknown')
            detected_lang = st.session_state.results.get('detected_lang', 'english')
            
            st.info(f"🤖 **{model_source}** | ML Confidence: {ml_prob:.2%} | Detected language: {LANGUAGES.get(detected_lang, {}).get('name', detected_lang)}")
            
            # Risk level display
            risk_level = result['risk_level']
            if risk_level == 'HIGH':
                st.markdown(f"""
                <div class="risk-high">
                    <h1 style="color: white; font-size: 3rem;">🚨🚨🚨</h1>
                    <h2 style="color: white;">{t('high_risk')}</h2>
                    <p style="color: white; font-size: 1.5rem;">90%+ Fraud Probability</p>
                </div>
                """, unsafe_allow_html=True)
            elif risk_level == 'MEDIUM':
                st.markdown(f"""
                <div class="risk-medium">
                    <h1 style="color: black; font-size: 3rem;">⚠️⚠️⚠️</h1>
                    <h2 style="color: black;">{t('medium_risk')}</h2>
                    <p style="color: black; font-size: 1.5rem;">50-80% Fraud Probability</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="risk-low">
                    <h1 style="color: black; font-size: 3rem;">✅✅✅</h1>
                    <h2 style="color: black;">{t('low_risk')}</h2>
                    <p style="color: black; font-size: 1.5rem;">Seems Safe</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Score meter
            st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <h3>{t('risk_score')}: {result['final_score']:.1f}%</h3>
                <progress value="{result['final_score']}" max="100" style="width: 100%; height: 30px;"></progress>
            </div>
            """, unsafe_allow_html=True)
            
            # User message in detected language
            st.info(result['user_message'])
            
            # Action steps
            if result.get('action_steps'):
                st.markdown(f"### {t('action_steps')}")
                for step in result['action_steps']:
                    st.markdown(f"- {step}")
            
            # Reasons
            if st.session_state.results['reasons']:
                with st.expander(t('detailed_analysis')):
                    for reason in st.session_state.results['reasons'][:5]:
                        if isinstance(reason, dict):
                            st.markdown(f"- {reason.get('message', str(reason))}")
                        else:
                            st.markdown(f"- {reason}")
            
            # Helplines
            if st.session_state.results['helplines']:
                st.markdown(f"### {t('helplines')}")
                for helpline in st.session_state.results['helplines'][:3]:
                    st.markdown(f"<div class='helpline-number'>{helpline}</div>", unsafe_allow_html=True)
            
            # Share buttons
            st.markdown(f"### {t('share_alert')}")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("📱 WhatsApp", use_container_width=True):
                    st.info("Share feature coming soon!")
            with col_b:
                if st.button("📧 Email", use_container_width=True):
                    st.info("Share feature coming soon!")
            with col_c:
                if st.button("🐦 Twitter", use_container_width=True):
                    st.info("Share feature coming soon!")

# ============================================
# TAB 2: LEARN (simplified)
# ============================================
with tabs[1]:
    st.markdown(f"<h2>{t('education_center')}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="fraud-card">
            <h3>{t('common_scams')}</h3>
            <ul style="color: white;">
                <li>{t('kyc_scams')}</li>
                <li>{t('otp_fraud')}</li>
                <li>{t('digital_arrest')}</li>
                <li>{t('lottery_scams')}</li>
                <li>{t('job_scams')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="fraud-card">
            <h3>{t('how_to_protect')}</h3>
            <ul style="color: white;">
                <li>{t('never_share_otp')}</li>
                <li>{t('verify_caller')}</li>
                <li>{t('check_urls')}</li>
                <li>{t('dont_pay_jobs')}</li>
                <li>{t('report_immediately')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="fraud-card">
            <h3>{t('who_to_contact')}</h3>
            <ul style="color: white;">
                <li>{t('cyber_crime')}</li>
                <li>{t('police')}</li>
                <li>{t('ambulance')}</li>
                <li>{t('women')}</li>
                <li>{t('child')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <p>{t('footer_text')}</p>
    <p>{t('footer_helpline')}</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">{t('footer_copyright')}</p>
</div>
""", unsafe_allow_html=True)