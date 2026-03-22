# pages/bengali.py
import sys
import os
import traceback
import time
import random
from datetime import datetime, timedelta

# Set up global exception handler
def global_excepthook(exctype, value, tb):
    import streamlit as st
    st.error(f"**Uncaught exception:** {value}")
    st.code(''.join(traceback.format_exception(exctype, value, tb)))
    st.stop()

sys.excepthook = global_excepthook

try:
    import pytesseract
    import platform

    # Set Tesseract path based on operating system
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    else:
        pytesseract.pytesseract.tesseract_cmd = 'tesseract'
    
    import streamlit as st
    import pandas as pd
    import numpy as np
    import joblib
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime

    # Add project root to path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Add app_advanced to path so components can be found
    app_advanced_path = os.path.join(project_root, 'app_advanced')
    if app_advanced_path not in sys.path:
        sys.path.insert(0, app_advanced_path)

    from components.ocr_utils import extract_text_from_image
    from components.company_verifier import extract_company_mentions, verify_sender
    from components.feedback_db import save_feedback
    from components.share_utils import get_whatsapp_link, get_email_link, get_twitter_link
    from components.community_db import load_posts, save_post

    from feature_engineering.feature_router import get_feature_router
    from risk_engine.rule_engine import MultilingualRuleEngine
    from risk_engine.rule_config import HELPLINE_NUMBERS
    from feature_engineering.language_detector import IndianLanguageDetector

    # ============================================
    # PAGE CONFIG
    # ============================================
    st.set_page_config(
        page_title="অভয় – Fraud Shield",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # ============================================
    # DARK MODERN CSS with beige background
    # ============================================
    st.markdown("""
    <style>
        .stApp {
            background-color: #F5F5DC !important;
        }

        /* MAIN CONTENT AREA */
        section.main > div {
            background-color: #F5F5DC !important;
        }

        /* INNER CONTAINER */
        .block-container {
            background-color: #F5F5DC !important;
        }

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        /* Dark background */
        body {
            background: #0A0C10;
            background-image: radial-gradient(circle at 20% 30%, rgba(24,183,190,0.05) 0%, transparent 50%);
        }

        /* Main container – light card */
        .main-container {
            background: rgba(245, 245, 220, 1);
            border-radius: 32px;
            padding: 2rem;
            margin: 1rem 1rem 1rem 280px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 1px solid rgba(24,183,190,0.3);
        }

        /* Rotating language letters – vibrant from the sets */
        .title-wrapper {
            position: relative;
            width: 320px;
            height: 320px;
            margin: 0 auto 2rem auto;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .title-center {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #18B7BE, #FEDD89);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(24,183,190,0.3);
            z-index: 2;
        }
        .lang-letter {
            position: absolute;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: #1E2A36;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.4rem;
            font-weight: bold;
            animation: rotate3d 15s linear infinite;
            border: 1px solid rgba(24,183,190,0.5);
            color: #EFF7F6;
        }
        .lang-letter:nth-child(1) { background: #403234; color: #FEDD89; animation-delay: 0s; }
        .lang-letter:nth-child(2) { background: #31383F; color: #18B7BE; animation-delay: -1.5s; }
        .lang-letter:nth-child(3) { background: #178CA4; color: #F9F7F0; animation-delay: -3s; }
        .lang-letter:nth-child(4) { background: #DD8EA4; color: #072A40; animation-delay: -4.5s; }
        .lang-letter:nth-child(5) { background: #64766A; color: #F2E9EB; animation-delay: -6s; }
        .lang-letter:nth-child(6) { background: #C0A9BD; color: #31383F; animation-delay: -7.5s; }
        .lang-letter:nth-child(7) { background: #94A7AE; color: #403234; animation-delay: -9s; }
        .lang-letter:nth-child(8) { background: #687477; color: #FEDD89; animation-delay: -10.5s; }
        .lang-letter:nth-child(9) { background: #E2C2B3; color: #072A40; animation-delay: -12s; }
        .lang-letter:nth-child(10) { background: #F7F3F5; color: #178CA4; animation-delay: -13.5s; }

        @keyframes rotate3d {
            from { transform: rotate(0deg) translateX(130px) rotate(0deg); }
            to   { transform: rotate(360deg) translateX(130px) rotate(-360deg); }
        }

        /* Stat cards – dark with subtle gradient and accent border */
        .stat-card {
            background: linear-gradient(145deg, #1A2632, #10171F);
            border-radius: 24px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid rgba(24,183,190,0.3);
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(24,183,190,0.2);
            border-color: #18B7BE;
        }
        .stat-card .value {
            font-size: 2.5rem;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
            color: #FEDD89;
        }
        .stat-card .label {
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #9BB8C9;
            margin-top: 0.5rem;
            font-weight: 600;
        }

        /* Input card – dark glass */
        .input-card {
            background: rgba(18, 25, 35, 0.7);
            border-radius: 28px;
            padding: 1.8rem;
            border: 1px solid rgba(24,183,190,0.4);
            backdrop-filter: blur(8px);
        }

        /* Buttons – vibrant */
        .stButton button {
            border-radius: 40px !important;
            font-weight: 600 !important;
            transition: all 0.2s !important;
            background: #18B7BE !important;
            color: #0A0C10 !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(24,183,190,0.3) !important;
        }
        .stButton button:hover {
            background: #FEDD89 !important;
            color: #0A0C10 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(254,221,137,0.3) !important;
        }
        .stButton button[kind="primary"] {
            background: #DD8EA4 !important;
            color: #0A0C10 !important;
        }
        .stButton button[kind="primary"]:hover {
            background: #C0A9BD !important;
        }

        /* Inputs – dark mode */
        .stTextInput > div > div > input, .stTextArea textarea, .stSelectbox > div > div {
            background: rgba(10,12,16,0.8) !important;
            border: 1px solid #2D3A46 !important;
            border-radius: 16px !important;
            color: #EFF7F6 !important;
        }
        .stTextInput > div > div > input:focus, .stTextArea textarea:focus {
            border-color: #18B7BE !important;
            box-shadow: 0 0 0 2px rgba(24,183,190,0.2) !important;
        }

        /* Slider */
        .stSlider > div > div > div {
            background: #18B7BE !important;
        }

        /* Progress bar */
        .stProgress > div > div > div > div {
            background: #FEDD89 !important;
            height: 8px !important;
            border-radius: 4px !important;
        }

        /* Risk badges – dark background with bright accents */
        .risk-high, .risk-medium, .risk-low {
            border-radius: 40px;
            padding: 1rem;
            font-weight: 600;
            text-align: center;
        }
        .risk-high {
            background: #2D1A1F;
            color: #FFA07A;
            border-left: 4px solid #DD8EA4;
        }
        .risk-medium {
            background: #2A2A1A;
            color: #FEDD89;
            border-left: 4px solid #FEDD89;
        }
        .risk-low {
            background: #1A2A24;
            color: #9AD7D1;
            border-left: 4px solid #18B7BE;
        }

        /* Ticker */
        .ticker-wrap {
            background: rgba(10,12,16,0.6);
            border-radius: 40px;
            padding: 12px;
            margin: 20px 0;
            border: 1px solid #2D3A46;
        }
        .ticker {
            color: #AAC8E0;
            font-size: 1rem;
            font-weight: 500;
        }

        /* Footer */
        .footer {
            background: rgba(10,12,16,0.8);
            border-radius: 30px 30px 0 0;
            padding: 2rem;
            color: #8AA9C0;
            text-align: center;
            margin-top: 2rem;
            font-size: 0.9rem;
            border-top: 1px solid #2D3A46;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] button {
            background: transparent;
            font-weight: 600;
            color: #9BB8C9;
            border-radius: 40px;
            padding: 0.4rem 1.2rem;
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background: #18B7BE;
            color: #0A0C10;
        }

        /* General text for main content (light background) */
        .main-container h1, .main-container h2, .main-container h3,
        .main-container h4, .main-container h5, .main-container h6,
        .main-container p, .main-container span, .main-container div,
        .main-container label {
            font-weight: 600;
            font-size: 1rem;
            color: #0A0C10;
        }

        /* Sidebar text (dark background) – all text inside sidebar */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stTextInput,
        section[data-testid="stSidebar"] .stRadio,
        section[data-testid="stSidebar"] .stSelectbox {
            color: #EFF7F6;
            font-weight: 600;
        }

        /* Sidebar headings specifically larger and bold */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            font-weight: 700;
            font-size: 1.2rem;
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background: #0A0C10;
            border-right: 1px solid #1E2A36;
        }

        /* Ensure input card text inside main container is dark */
        .input-card h3, .input-card p, .input-card span, .input-card label {
            color: #0A0C10 !important;
        }

        /* Stat card text (already set) – but ensure they stay light on dark */
        .stat-card .value {
            color: #FEDD89;
        }
        .stat-card .label {
            color: #9BB8C9;
        }

        /* Remove blur from main container if desired (optional) */
        .main-container {
            backdrop-filter: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # ============================================
    # LANGUAGE‑SPECIFIC TEXTS (Bengali)
    # ============================================
    TEXTS = {
        'app_subtitle': "ভারতের প্রথম বহুভাষিক জালিয়াতি সনাক্তকরণ ব্যবস্থা",
        'tagline': 'নির্ভীক জালিয়াতি ঢাল – ১.৪ বিলিয়ন ভারতীয়কে তাদের নিজস্ব ভাষায় সুরক্ষা',
        'detector': '🔍 শনাক্তকারী',
        'learn': '🎓 শিখুন',
        'help': '🆘 সাহায্য',
        'stats': '📊 পরিসংখ্যান',
        'community': '👥 সম্প্রদায়',
        'about': 'ℹ️ প্রকল্প সম্পর্কে',
        'login': '🔐 লগইন / ব্যবহারকারীর নাম',
        'language': '🌐 ভাষা',
        'fraud_type': '🎯 জালিয়াতির ধরন',
        'today_stats': "📊 আজকের পরিসংখ্যান",
        'scans_today': 'আজকের স্ক্যান',
        'frauds_blocked': 'অবরুদ্ধ জালিয়াতি',
        'active_users': 'সক্রিয় ব্যবহারকারী',
        'languages': 'ভাষাসমূহ',
        'sms': '📱 এসএমএস/ইমেইল',
        'call': '📞 কল',
        'crypto': '💰 ক্রিপ্টো',
        'job': '💼 নকল চাকরি',
        'social': '👥 সোশ্যাল মিডিয়া',
        'website': '🌐 ওয়েবসাইট',
        'enter_sms': '📝 এসএমএস/বার্তা লিখুন',
        'sender_id': '📱 প্রেরকের আইডি (ঐচ্ছিক)',
        'high_risk': '🚨 উচ্চ ঝুঁকি সনাক্ত!',
        'medium_risk': '⚠️ মাঝারি ঝুঁকি',
        'low_risk': '✅ কম ঝুঁকি',
        'risk_score': 'ঝুঁকি স্কোর',
        'detailed_analysis': '🔍 বিস্তারিত বিশ্লেষণ',
        'helplines': '📞 হেল্পলাইন',
        'share_alert': '📤 সতর্কতা শেয়ার করুন',
        'detected_language': '✅ সনাক্তকৃত ভাষা',
        'confidence': 'আস্থা',
        'footer_text': '🇮🇳 অভয় – ভারতকে জালিয়াতি থেকে রক্ষা করে | ১২টি ভারতীয় ভাষা | ২৪x৭ বিনামূল্যে সেবা',
        'footer_helpline': '📞 জাতীয় সাইবার ক্রাইম হেল্পলাইন: 1930 | 📧 report@cybercrime.gov.in',
        'footer_copyright': '© ২০২৪ অভয় – এমএসসি ডেটা সায়েন্স & এআই প্রকল্প',
        'sms_placeholder': 'যেকোনো সন্দেহজনক বার্তা এখানে পেস্ট করুন...',
        'new_post': '📝 নতুন পোস্ট',
        'author': 'লেখক',
        'title': 'শিরোনাম',
        'content': 'বিষয়বস্তু',
        'category': 'বিভাগ',
        'link': 'লিঙ্ক (ঐচ্ছিক)',
        'post_btn': 'পোস্ট করুন',
        'recent_posts': 'সাম্প্রতিক পোস্ট',
    }

    # ============================================
    # LOAD MODELS (unchanged)
    # ============================================
    @st.cache_resource
    def load_models():
        models = {}
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        
        for ft, fname in model_files.items():
            model_path = os.path.join(models_path, fname)
            scaler_path = os.path.join(models_path, scaler_files[ft])
            if os.path.exists(model_path):
                try:
                    models[ft] = {
                        'model': joblib.load(model_path),
                        'scaler': joblib.load(scaler_path) if os.path.exists(scaler_path) else None
                    }
                except Exception as e:
                    print(f"Error loading {ft}: {e}")
                    models[ft] = None
            else:
                models[ft] = None
        return models

    @st.cache_resource
    def init_system():
        router = get_feature_router()
        rule_engine = MultilingualRuleEngine()
        language_detector = IndianLanguageDetector()
        models = load_models()
        return router, rule_engine, language_detector, models

    router, rule_engine, language_detector, models = init_system()

    # ============================================
    # ML PREDICTION FUNCTION (unchanged)
    # ============================================
    def get_ml_prediction(fraud_type, input_data, features):
        if fraud_type not in models or models[fraud_type] is None:
            return 0.5, "Rule Engine only (no model)"
        try:
            model_data = models[fraud_type]
            model = model_data['model']
            scaler = model_data['scaler']
            
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            models_path = os.path.join(base_path, "models")
            feature_names_path = os.path.join(models_path, f"{fraud_type}_feature_names.pkl")
            
            if os.path.exists(feature_names_path):
                feature_names = joblib.load(feature_names_path)
                row_df = pd.DataFrame([features])
                row_df = row_df.reindex(columns=feature_names, fill_value=0)
                feature_vector = row_df.values.astype(float)
            else:
                feature_vector = router.get_feature_vector(fraud_type, input_data, model_type='ml')
                feature_vector = feature_vector.reshape(1, -1)
                expected = 163
                if feature_vector.shape[1] != expected:
                    if feature_vector.shape[1] > expected:
                        feature_vector = feature_vector[:, :expected]
                    else:
                        feature_vector = np.pad(feature_vector, ((0,0),(0,expected-feature_vector.shape[1])), mode='constant')
            
            if scaler is not None:
                feature_vector = scaler.transform(feature_vector)
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(feature_vector)[0]
                ml_prob = proba[1] if len(proba) == 2 else proba[0]
            else:
                pred = model.predict(feature_vector)[0]
                ml_prob = 0.9 if pred == 1 else 0.1
            return ml_prob, "ML Model (English)"
        except Exception as e:
            print(f"ML prediction error: {e}")
            return 0.5, "Rule Engine only (ML error)"

    # ============================================
    # SESSION STATE (unchanged)
    # ============================================
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False
    if 'show_proof' not in st.session_state:
        st.session_state.show_proof = False

    # ============================================
    # SIDEBAR – dark, with language dropdown
    # ============================================
    with st.sidebar:
        st.markdown("""
        <div style="display:flex; justify-content:center; margin-bottom:20px;">
            <div style="background:#18B7BE; border-radius:50%; padding:15px;">
                <span style="font-size:3rem; color:#0A0C10;">🛡️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"### {TEXTS['login']}")
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'username' not in st.session_state:
            st.session_state.username = ''

        if not st.session_state.logged_in:
            if st.button("🔐 লগইন করুন", use_container_width=True):
                st.query_params["lang"] = "বাংলা"
                st.query_params["redirect"] = "pages/bengali.py"
                st.switch_page("pages/login.py")
            st.info("সব বৈশিষ্ট্য অ্যাক্সেস করতে দয়া করে লগইন করুন")
        else:
            st.success(f"✅ লগইন করেছেন: **{st.session_state.username}**")
            if st.button("🚪 লগআউট", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ''
                st.rerun()
        st.markdown("---")
        st.markdown(f"### {TEXTS['language']}")
        
        # Language dropdown (same as in English page)
        languages = {
            'English': 'english.py',
            'मराठी': 'marathi.py',
            'हिंदी': 'hindi.py',
            'தமிழ்': 'tamil.py',
            'తెలుగు': 'telugu.py',
            'ಕನ್ನಡ': 'kannada.py',
            'മലയാളം': 'malayalam.py',
            'ગુજરાતી': 'gujarati.py',
            'বাংলা': 'bengali.py',
            'ਪੰਜਾਬੀ': 'punjabi.py'
        }
        # Set default selection to current language (Bengali)
        default_index = list(languages.keys()).index('বাংলা')
        selected_lang = st.selectbox("Select Language", list(languages.keys()), index=default_index)
        if selected_lang != "বাংলা":
            st.switch_page(f"pages/{languages[selected_lang]}")
        
        st.markdown("---")
        st.markdown(f"### {TEXTS['fraud_type']}")
        fraud_type = st.radio(
            "Fraud type",
            options=['sms', 'call', 'crypto', 'job', 'social', 'website'],
            label_visibility="collapsed",
            format_func=lambda x: {'sms':TEXTS['sms'], 'call':TEXTS['call'], 'crypto':TEXTS['crypto'],
                                   'job':TEXTS['job'], 'social':TEXTS['social'], 'website':TEXTS['website']}[x],
            index=0
        )
        
        st.markdown("---")
        st.markdown(f"### {TEXTS['today_stats']}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(TEXTS['scans_today'], "1,234", "+12%")
        with col2:
            st.metric(TEXTS['frauds_blocked'], "456", "+8%")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(TEXTS['active_users'], "5,678", "+23%")
        with col2:
            st.metric(TEXTS['languages'], "10", "🇮🇳")

    # ============================================
    # MAIN CONTENT WRAPPED IN UNIFIED BOX
    # ============================================
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # ============================================
    # MAIN TITLE WITH ROTATING LETTERS
    # ============================================
    st.markdown("""
    <div class="title-wrapper">
        <div class="lang-letter lang1">A</div>
        <div class="lang-letter lang2">অ</div>
        <div class="lang-letter lang3">ব</div>
        <div class="lang-letter lang4">ত</div>
        <div class="lang-letter lang5">ক</div>
        <div class="lang-letter lang6">ম</div>
        <div class="lang-letter lang7">ಗ</div>
        <div class="lang-letter lang8">ਪ</div>
        <div class="lang-letter lang9">ગ</div>
        <div class="lang-letter lang10">മ</div>
        <div class="title-center">অভয়</div>
    </div>
    <div style="text-align:center; margin-top:20px;">
        <h1 style="font-family:'Orbitron', sans-serif; font-size:3rem; font-weight:700; background:linear-gradient(135deg, #0A0C10, #1B263B); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">THE FEARLESS FRAUD SHIELD</h1>
        <p style="color:#660033; font-weight:600; font-size:1.2rem;">{}</p>
        <p style="color:#722F37; font-weight:600; font-size:1.1rem;">{}</p>
    </div>
    """.format(TEXTS['app_subtitle'], TEXTS['tagline']), unsafe_allow_html=True)

    # ============================================
    # STATS CARDS
    # ============================================
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="value">1,23,456</div>
            <div class="label">TOTAL SCAMS</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="value">₹45.6Cr</div>
            <div class="label">AMOUNT SAVED</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="value">94%</div>
            <div class="label">ACCURACY</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="value">10</div>
            <div class="label">LANGUAGES</div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================
    # TICKER
    # ============================================
    st.markdown("""
    <div class="ticker-wrap" style="background-color: #301934; padding: 10px;">
        <div class="ticker" style="color: #F4C2C2; font-weight: bold;">
            🚨 KYC Scam in Mumbai • OTP Fraud in Chennai • Job Scam in Bengaluru • Digital Arrest in Delhi • Lottery Scam in Pune 🚨
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================
    # TABS
    # ============================================
    tab_names = [TEXTS['detector'], TEXTS['learn'], TEXTS['help'], TEXTS['stats'], TEXTS['community'], TEXTS['about']]
    tabs = st.tabs(tab_names)

    # Custom CSS to change the Tab Font Color
    st.markdown(f"""
       <style>
       button[data-baseweb="tab"] p {{
        color: #3B2F2F;
        font-weight: bold;
        font-size: 16px;
      }}
      button[data-baseweb="tab"][aria-selected="true"] p {{
        color: #FFFFFF;
      }}
      </style>
    """, unsafe_allow_html=True)

    # ============================================
    # TAB 1: DETECTOR (unchanged functionality)
    # ============================================
    with tabs[0]:
        col_input, col_output = st.columns([2, 1.5])
        
        with col_input:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            st.markdown("### 📥 ইনপুট", unsafe_allow_html=True)
            
            method = st.radio("ইনপুট পদ্ধতি বেছে নিন", ["লেখা", "ছবি", "ইমেইল"], horizontal=True)
            text_input = ""
            sender_id = ""
            
            if method == "লেখা":
                text_input = st.text_area(TEXTS['enter_sms'], height=150, placeholder=TEXTS['sms_placeholder'])
                sender_id = st.text_input(TEXTS['sender_id'], placeholder="যেমন, BANKALERT")
            elif method == "ছবি":
                st.markdown('<div style="border:2px dashed #18B7BE; border-radius:20px; padding:20px;">', unsafe_allow_html=True)
                uploaded = st.file_uploader("ছবি আপলোড করুন", type=['png','jpg','jpeg'], label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)
                if uploaded:
                    with st.spinner("লেখা বের করা হচ্ছে..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        text_input = extract_text_from_image(uploaded)
                        st.text_area("বের করা লেখা", text_input, height=150)
            else:  # ইমেইল
                text_input = st.text_area("ইমেইলের লেখা", height=150)
                sender_id = st.text_input("প্রেরকের ইমেইল", placeholder="prerak@example.com")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔍 ভাষা শনাক্ত করুন", use_container_width=True):
                    if text_input:
                        with st.spinner("ভাষা শনাক্ত করা হচ্ছে..."):
                            progress_bar = st.progress(0)
                            for i in range(100):
                                time.sleep(0.01)
                                progress_bar.progress(i + 1)
                            lang, conf, _ = language_detector.detect_language(text_input)
                            st.success(f"{TEXTS['detected_language']}: {lang} ({TEXTS['confidence']}: {conf:.2%})")
            with col_btn2:
                if st.button("🚨 জালিয়াতি পরীক্ষা করুন", type="primary", use_container_width=True):
                    if not text_input:
                        st.warning("অনুগ্রহ করে কিছু লেখা দিন।")
                    else:
                        with st.spinner("বিশ্লেষণ চলছে..."):
                            progress_bar = st.progress(0)
                            for i in range(100):
                                time.sleep(0.02)
                                progress_bar.progress(i + 1)
                            input_data = {'text': text_input, 'sender_id': sender_id}
                            features = router.extract_features(fraud_type, input_data)
                            detected_lang = features.get('detected_language', 'unknown')
                            
                            if detected_lang in ['english', 'unknown_latin']:
                                ml_prob, model_source = get_ml_prediction(fraud_type, input_data, features)
                            else:
                                ml_prob = 0.5
                                model_source = "শুধু নিয়ম ইঞ্জিন"
                            
                            rule_score, reasons, helplines = rule_engine.calculate_risk(fraud_type, input_data, detected_lang)
                            
                            if "ML" in model_source:
                                combined = (ml_prob * 0.7) + (min(rule_score/100, 1.0) * 0.3)
                            else:
                                combined = min(rule_score/100, 1.0)
                            
                            result = rule_engine.combine_risk(combined, rule_score, detected_lang, features.get('is_code_mixed', False))
                            
                            st.session_state.results = {
                                'text': text_input,
                                'sender': sender_id,
                                'ml_prob': ml_prob,
                                'model_source': model_source,
                                'rule_score': rule_score,
                                'reasons': reasons,
                                'helplines': helplines,
                                'result': result,
                                'detected_lang': detected_lang
                            }
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_output:
            if st.session_state.results:
                res = st.session_state.results
                result = res['result']
                
                companies = extract_company_mentions(res['text'])
                if companies:
                    st.markdown("### 🏢 কোম্পানি যাচাই")
                    for comp in companies:
                        st.markdown(f"**{comp['name']}**")
                        st.caption(f"অফিসিয়াল ডোমেন: {comp['domain']}")
                        if res['sender']:
                            if verify_sender(comp['domain'], res['sender']):
                                st.success("✅ প্রেরকের ডোমেন মিলেছে")
                            else:
                                st.warning("⚠️ প্রেরকের ডোমেন মেলেনি")
                
                risk_level = result['risk_level']
                if risk_level == 'HIGH':
                    st.markdown(f'<div class="risk-high"><h3>{TEXTS["high_risk"]}</h3></div>', unsafe_allow_html=True)
                elif risk_level == 'MEDIUM':
                    st.markdown(f'<div class="risk-medium"><h3>{TEXTS["medium_risk"]}</h3></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="risk-low"><h3>{TEXTS["low_risk"]}</h3></div>', unsafe_allow_html=True)
                
                st.progress(result['final_score']/100)
                st.write(f"**{TEXTS['risk_score']}:** {result['final_score']:.1f}%")
                st.info(result['user_message'])
                
                with st.expander(TEXTS['detailed_analysis']):
                    for r in res['reasons'][:5]:
                        msg = r.get('message', str(r)) if isinstance(r, dict) else str(r)
                        st.write(f"- {msg}")
                
                if res['helplines']:
                    st.markdown(f"### {TEXTS['helplines']}")
                    for h in res['helplines'][:3]:
                        st.write(f"**{h}**")
                
                if st.session_state.username:
                    st.markdown(f"### {TEXTS['share_alert']} / মতামত")
                    col_f1, col_f2, col_f3 = st.columns(3)
                    with col_f1:
                        if st.button("👍 হ্যাঁ"):
                            save_feedback(res['text'], res['ml_prob'], res['rule_score'], result['final_score'], True, "", "")
                            st.success("ধন্যবাদ!")
                    with col_f2:
                        if st.button("👎 না"):
                            st.session_state.show_feedback = True
                    with col_f3:
                        if st.button("🔗 প্রমাণ লিঙ্ক"):
                            st.session_state.show_proof = True
                    
                    if st.session_state.show_feedback:
                        comment = st.text_area("কি ভুল হয়েছে?")
                        if st.button("মতামত জমা দিন"):
                            save_feedback(res['text'], res['ml_prob'], res['rule_score'], result['final_score'], False, comment, "")
                            st.success("মতামত নথিভুক্ত করা হয়েছে")
                            st.session_state.show_feedback = False
                    
                    if st.session_state.show_proof:
                        proof = st.text_input("অফিসিয়াল লিঙ্ক পেস্ট করুন")
                        if st.button("প্রমাণ জমা দিন"):
                            save_feedback(res['text'], res['ml_prob'], res['rule_score'], result['final_score'], False, "", proof)
                            st.success("প্রমাণ জমা দেওয়া হয়েছে")
                            st.session_state.show_proof = False
                else:
                    st.info("মতামত দিতে অনুগ্রহ করে লগইন করুন।")
                
                share_text = f"আমি এই বার্তাটি অভয় দিয়ে পরীক্ষা করেছি। ঝুঁকি: {result['final_score']}% ({risk_level}). আপনি নিজেও পরীক্ষা করুন!"
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    st.markdown(f"[![WhatsApp](https://img.icons8.com/color/48/000000/whatsapp--v1.png)]({get_whatsapp_link(share_text)})")
                with col_s2:
                    st.markdown(f"[![Email](https://img.icons8.com/color/48/000000/email.png)]({get_email_link('জালিয়াতি সতর্কতা', share_text)})")
                with col_s3:
                    st.markdown(f"[![Twitter](https://img.icons8.com/color/48/000000/twitter--v1.png)]({get_twitter_link(share_text)})")

    # ============================================
    # TAB 2: LEARN
    # ============================================
    with tabs[1]:
        st.markdown(f"<h2>{TEXTS['learn']}</h2>", unsafe_allow_html=True)
        st.write("জালিয়াতি সম্পর্কে শিক্ষামূলক বিষয়বস্তু এখানে যুক্ত করতে পারেন – নিবন্ধ, ভিডিও ইত্যাদি।")
        st.image("https://img.freepik.com/free-vector/cyber-fraud-concept-illustration_114360-5520.jpg", use_column_width=True)

    # ============================================
    # TAB 3: HELP – cards (unchanged)
    # ============================================
    with tabs[2]:
        st.markdown(f"<h2>{TEXTS['help']}</h2>", unsafe_allow_html=True)
        
        helplines_data = HELPLINE_NUMBERS if isinstance(HELPLINE_NUMBERS, dict) else {
            "National": {"cyber_crime": "1930", "women_helpline": "1091", "child_helpline": "1098", "police": "100", "ambulance": "102", "disaster": "108"},
            "Maharashtra": {"mumbai_cyber": "022-22620111", "pune_cyber": "020-26124220", "nagpur_cyber": "0712-2562111", "thane_cyber": "022-25341234", "women_helpline": "1091", "police": "100"},
            "Karnataka": {"bangalore_cyber": "080-23456789", "mysore_cyber": "0821-1234567", "women_helpline": "1091"},
            "West Bengal": {"kolkata_cyber": "033-23456789", "howrah_cyber": "033-1234567"},
            "Uttar Pradesh": {"lucknow_cyber": "0522-2345678", "kanpur_cyber": "0512-2345678"},
            "Telangana": {"hyderabad_cyber": "040-23456789", "warangal_cyber": "0870-1234567"},
            "Punjab": {"chandigarh_cyber": "0172-2345678", "ludhiana_cyber": "0161-1234567"},
            "Bihar": {"patna_cyber": "0612-2345678", "police": "100"},
            "Tamil Nadu": {"chennai_cyber": "044-23456789", "coimbatore_cyber": "0422-1234567", "madurai_cyber": "0452-2345678", "women_helpline": "1091"},
            "Gujarat": {"ahmedabad_cyber": "079-23456789", "surat_cyber": "0261-1234567"},
            "Delhi": {"delhi_cyber": "011-23456789", "women_helpline": "1091"},
            "Odisha": {"bhubaneswar_cyber": "0674-2345678", "cuttack_cyber": "0671-2345678"}
        }
        
        states = list(helplines_data.keys())
        cols = st.columns(2)
        for i, state in enumerate(states):
            with cols[i % 2]:
                with st.expander(f"📞 {state}", expanded=False):
                    helplines = helplines_data[state]
                    for name, number in helplines.items():
                        display_name = name.replace('_', ' ').title()
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #2D3A46;">
                            <span style="font-weight: 500;">{display_name}</span>
                            <span style="font-family: monospace; font-size: 1.1rem; color: #18B7BE;">{number}</span>
                        </div>
                        """, unsafe_allow_html=True)

    # ============================================
    # TAB 4: STATS – graphs
    # ============================================
    with tabs[3]:
        st.markdown(f"<h2>{TEXTS['stats']}</h2>", unsafe_allow_html=True)
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        fraud_counts = np.random.poisson(lam=50, size=30) + np.sin(np.linspace(0, 3*np.pi, 30))*20
        fraud_counts = np.maximum(fraud_counts, 0).astype(int)
        df = pd.DataFrame({
            'Date': dates,
            'Fraud Cases': fraud_counts,
            'Type': np.random.choice(['SMS', 'Call', 'Crypto', 'Job', 'Social', 'Website'], 30)
        })

        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            date_range = st.date_input("তারিখের পরিসীমা নির্বাচন করুন", [dates[0], dates[-1]])
        with col_filter2:
            fraud_types = st.multiselect("জালিয়াতির ধরন", df['Type'].unique(), default=df['Type'].unique())

        risk_threshold = st.slider("ঝুঁকি মাত্রা (%)", 0, 100, 50)

        filtered_df = df[(df['Date'] >= pd.Timestamp(date_range[0])) & 
                         (df['Date'] <= pd.Timestamp(date_range[1])) &
                         (df['Type'].isin(fraud_types))]

        fig = px.line(filtered_df, x='Date', y='Fraud Cases', title='দৈনিক জালিয়াতি ঘটনা',
                      color_discrete_sequence=['#18B7BE'])
        fig.update_layout(
            plot_bgcolor='rgba(244, 194, 194, 1)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FF8C00',
            title_font_color='#301934'
        )
        st.plotly_chart(fig, use_container_width=True)

        type_counts = filtered_df.groupby('Type')['Fraud Cases'].sum().reset_index()
        fig2 = px.bar(type_counts, x='Type', y='Fraud Cases', title='প্রকারভেদে মোট জালিয়াতি',
                      color='Type', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig2.update_layout(
            plot_bgcolor='rgba(244, 194, 194, 1)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FF8C00',
            title_font_color='#301934'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ============================================
    # TAB 5: COMMUNITY – cards
    # ============================================
    with tabs[4]:
        st.markdown(f"<h2>{TEXTS['community']}</h2>", unsafe_allow_html=True)
        
        posts = load_posts()
        if not posts.empty:
            for _, row in posts.sort_values('timestamp', ascending=False).iterrows():
                st.markdown(f"""
                <div style="background:rgba(10,12,16,0.6); border-radius:24px; padding:1.5rem; margin-bottom:1rem; border:1px solid #2D3A46;">
                    <div style="font-size:1.3rem; font-weight:bold; color:#FEDD89;">{row['title']}</div>
                    <div style="color:#9BB8C9; font-size:0.9rem;">by {row['author']} • {row['timestamp']}</div>
                    <div style="margin-top:1rem; color:#EFF7F6;">{row['content']}</div>
                    <div style="margin-top:0.8rem;">
                        <span style="color:#18B7BE;">বিভাগ: {row['category']}</span>
                        {f' <a href="{row["link"]}" target="_blank" style="color:#18B7BE;">🔗 লিঙ্ক</a>' if row['link'] else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("এখনও কোন পোস্ট নেই। প্রথম পোস্ট তৈরি করুন!")
        
        if st.session_state.username:
            st.markdown(f"### {TEXTS['new_post']}")
            with st.form("new_post_form"):
                title = st.text_input(TEXTS['title'])
                content = st.text_area(TEXTS['content'])
                category = st.selectbox(TEXTS['category'], ["সাধারণ", "জালিয়াতি সতর্কতা", "প্রশ্ন", "সাফল্যের গল্প"])
                link = st.text_input(TEXTS['link'])
                submitted = st.form_submit_button(TEXTS['post_btn'])
                if submitted and title and content:
                    save_post(st.session_state.username, title, content, category, link)
                    st.success("পোস্ট যোগ করা হয়েছে!")
                    st.rerun()
        else:
            st.info("পোস্ট করতে দয়া করে লগইন করুন।")

    # ============================================
    # TAB 6: ABOUT
    # ============================================
    with tabs[5]:
        st.markdown(f"<h2>{TEXTS['about']}</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(10,12,16,0.6); border-radius:32px; padding:2rem; border:1px solid #2D3A46;">
            <h3 style="color:#FEDD89;">অভয় – নির্ভীক জালিয়াতি ঢাল</h3>
            <p style="color:#EFF7F6;"><strong>কেন অভয়?</strong> এমন একটি দেশে যেখানে লক্ষ লক্ষ মানুষ তাদের মাতৃভাষায় জালিয়াতির শিকার হয়, আমরা এমন একটি ব্যবস্থা তৈরি করেছি যা আপনাকে বোঝে – আপনি হিন্দি, মারাঠি, তামিল বা ভারতের ১২টি সরকারি ভাষার যেকোনোটি বলুন না কেন। উন্নত মেশিন লার্নিং এবং একটি শক্তিশালী নিয়ম ইঞ্জিনের সংমিশ্রণে, অভয় ১.৪ বিলিয়ন ভারতীয়কে জালিয়াতি থেকে রক্ষা করে, একটি বার্তায়।</p>
            <hr style="border-color:#2D3A46;">
            <p><strong style="color:#18B7BE;">👩‍💻 স্রষ্টা:</strong> <span style="color:#9BB8C9;">সাক্ষী শ্রীকৃষ্ণ মাগাম</span></p>
            <p><strong style="color:#18B7BE;">🎓 পড়াশোনা:</strong> <span style="color:#9BB8C9;">এমএসসি ডেটা সায়েন্স এবং আর্টিফিশিয়াল ইন্টেলিজেন্স</span></p>
            <p><strong style="color:#18B7BE;">🏛️ প্রতিষ্ঠান:</strong> <span style="color:#9BB8C9;">রামনিরঞ্জন ঝুনঝুনওয়ালা কলেজ</span></p>
            <p><strong style="color:#18B7BE;">🔧 প্রযুক্তি:</strong> <span style="color:#9BB8C9;">Python, Scikit‑learn, XGBoost, Streamlit, কাস্টম নিয়ম ইঞ্জিন, বহুভাষিক NLP, OCR, এবং আরও অনেক কিছু।</span></p>
            <p><strong style="color:#18B7BE;">📧 যোগাযোগ:</strong> <span style="color:#9BB8C9;">sakshimagham@gmail.com</span></p>
            <p><strong style="color:#18B7BE;">🌟 লক্ষ্য:</strong> <span style="color:#9BB8C9;">প্রত্যেক নাগরিককে রিয়েল-টাইম, ভাষা-স্বাধীন সুরক্ষা প্রদান করে জালিয়াতি-মুক্ত ডিজিটাল ভারত তৈরি করা।</span></p>
            <p><em style="color:#DD8EA4;">এই প্রকল্পটি এমএসসি ডেটা সায়েন্স & এআই কোর্সের চূড়ান্ত বর্ষের প্রয়োজনীয়তা হিসাবে জমা দেওয়া হয়েছে। আমরা আশা করি এটি একটি পরিবর্তন আনবে।</em></p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================
    # FOOTER (inside main container)
    # ============================================
    st.markdown("---")
    st.markdown(f"""
    <div class="footer">
        <p>{TEXTS['footer_text']}</p>
        <p>{TEXTS['footer_helpline']}</p>
        <p style="font-size:0.8rem;">{TEXTS['footer_copyright']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"**একটি ত্রুটি দেখা দিয়েছে:** {e}")
    st.code(traceback.format_exc())
    st.stop()