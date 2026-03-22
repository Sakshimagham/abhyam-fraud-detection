import streamlit as st
import hashlib
import json
import os
from datetime import datetime

# File path for storing users
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.json')

# Initialize users file if it doesn't exist
def init_users_file():
    if not os.path.exists(USERS_FILE):
        default_users = {
            "sakshi": {
                "password_hash": hashlib.sha256("sakshi123".encode()).hexdigest(),
                "email": "sakshi@example.com",
                "created_at": datetime.now().isoformat()
            },
            "admin": {
                "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                "email": "admin@example.com",
                "created_at": datetime.now().isoformat()
            }
        }
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=2)

# Load users from file
def load_users():
    init_users_file()
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Language texts for login page - All 10 languages
LANG_TEXTS = {
    'English': {
        'title': 'अभयम् - Login',
        'subtitle': "India's 1st Multilingual Fraud Detection System",
        'username': 'Username',
        'password': 'Password',
        'login': '🔐 Login',
        'register': '📝 Register',
        'forgot_password': '❓ Forgot Password?',
        'enter_username': 'Enter your username',
        'enter_password': 'Enter your password',
        'reset_password': 'Reset Password',
        'create_account': '📝 Create New Account',
        'confirm_password': 'Confirm Password',
        'email': 'Email',
        'back_to_login': '← Back to Login',
        'register_btn': '✅ Register',
        'invalid_credentials': 'Invalid username or password!',
        'registration_success': 'Registration successful! Please login.',
        'username_exists': 'Username already exists!',
        'passwords_not_match': "Passwords don't match!",
        'fill_all_fields': 'Please fill all fields!',
        'user_not_found': 'Username not found!',
        'reset_demo': 'Demo: Use password for testing',
        'reset_link': 'Password reset link would be sent to:',
        'footer': '🇮🇳 National Cyber Crime Helpline: 1930',
        'home': '🏠 Home'
    },
    'हिंदी': {
        'title': 'अभयम् - लॉगिन',
        'subtitle': 'भारत की पहली बहुभाषी धोखाधड़ी पहचान प्रणाली',
        'username': 'उपयोगकर्ता नाम',
        'password': 'पासवर्ड',
        'login': '🔐 लॉगिन',
        'register': '📝 पंजीकरण',
        'forgot_password': '❓ पासवर्ड भूल गए?',
        'enter_username': 'अपना उपयोगकर्ता नाम दर्ज करें',
        'enter_password': 'अपना पासवर्ड दर्ज करें',
        'reset_password': 'पासवर्ड रीसेट करें',
        'create_account': '📝 नया खाता बनाएं',
        'confirm_password': 'पासवर्ड की पुष्टि करें',
        'email': 'ईमेल',
        'back_to_login': '← लॉगिन पर वापस जाएं',
        'register_btn': '✅ पंजीकरण करें',
        'invalid_credentials': 'गलत उपयोगकर्ता नाम या पासवर्ड!',
        'registration_success': 'पंजीकरण सफल! कृपया लॉगिन करें।',
        'username_exists': 'उपयोगकर्ता नाम पहले से मौजूद है!',
        'passwords_not_match': 'पासवर्ड मेल नहीं खाते!',
        'fill_all_fields': 'कृपया सभी फ़ील्ड भरें!',
        'user_not_found': 'उपयोगकर्ता नाम नहीं मिला!',
        'reset_demo': 'डेमो: परीक्षण के लिए पासवर्ड का उपयोग करें',
        'reset_link': 'पासवर्ड रीसेट लिंक यहां भेजा जाएगा:',
        'footer': '🇮🇳 राष्ट्रीय साइबर क्राइम हेल्पलाइन: 1930',
        'home': '🏠 होम'
    },
    'मराठी': {
        'title': 'अभयम् - लॉगिन',
        'subtitle': 'भारताची पहिली बहुभाषिक फसवणूक ओळख प्रणाली',
        'username': 'वापरकर्तानाव',
        'password': 'पासवर्ड',
        'login': '🔐 लॉगिन',
        'register': '📝 नोंदणी',
        'forgot_password': '❓ पासवर्ड विसरलात?',
        'enter_username': 'आपले वापरकर्तानाव प्रविष्ट करा',
        'enter_password': 'आपला पासवर्ड प्रविष्ट करा',
        'reset_password': 'पासवर्ड रीसेट करा',
        'create_account': '📝 नवीन खाते तयार करा',
        'confirm_password': 'पासवर्डची पुष्टी करा',
        'email': 'ईमेल',
        'back_to_login': '← लॉगिन वर परत जा',
        'register_btn': '✅ नोंदणी करा',
        'invalid_credentials': 'अवैध वापरकर्तानाव किंवा पासवर्ड!',
        'registration_success': 'नोंदणी यशस्वी! कृपया लॉगिन करा.',
        'username_exists': 'वापरकर्तानाव आधीपासून अस्तित्वात आहे!',
        'passwords_not_match': 'पासवर्ड जुळत नाहीत!',
        'fill_all_fields': 'कृपया सर्व फील्ड भरा!',
        'user_not_found': 'वापरकर्तानाव सापडले नाही!',
        'reset_demo': 'डेमो: चाचणीसाठी पासवर्ड वापरा',
        'reset_link': 'पासवर्ड रीसेट लिंक येथे पाठविला जाईल:',
        'footer': '🇮🇳 राष्ट्रीय सायबर क्राइम हेल्पलाइन: 1930',
        'home': '🏠 होम'
    },
    'தமிழ்': {
        'title': 'அபயம் - உள்நுழைவு',
        'subtitle': 'இந்தியாவின் முதல் பல்மொழி மோசடி கண்டறிதல் அமைப்பு',
        'username': 'பயனர் பெயர்',
        'password': 'கடவுச்சொல்',
        'login': '🔐 உள்நுழைக',
        'register': '📝 பதிவு செய்க',
        'forgot_password': '❓ கடவுச்சொல் மறந்துவிட்டதா?',
        'enter_username': 'உங்கள் பயனர் பெயரை உள்ளிடுக',
        'enter_password': 'உங்கள் கடவுச்சொல்லை உள்ளிடுக',
        'reset_password': 'கடவுச்சொல்லை மீட்டமைக்க',
        'create_account': '📝 புதிய கணக்கை உருவாக்கு',
        'confirm_password': 'கடவுச்சொல்லை உறுதி செய்',
        'email': 'மின்னஞ்சல்',
        'back_to_login': '← உள்நுழைவுக்குத் திரும்பு',
        'register_btn': '✅ பதிவு செய்',
        'invalid_credentials': 'தவறான பயனர் பெயர் அல்லது கடவுச்சொல்!',
        'registration_success': 'பதிவு வெற்றிகரமாக! தயவுசெய்து உள்நுழைக.',
        'username_exists': 'பயனர் பெயர் ஏற்கனவே உள்ளது!',
        'passwords_not_match': 'கடவுச்சொற்கள் பொருந்தவில்லை!',
        'fill_all_fields': 'அனைத்து புலங்களையும் நிரப்பவும்!',
        'user_not_found': 'பயனர் பெயர் கிடைக்கவில்லை!',
        'reset_demo': 'டெமோ: சோதனைக்கு கடவுச்சொல்லைப் பயன்படுத்தவும்',
        'reset_link': 'கடவுச்சொல் மீட்டமைப்பு இணைப்பு இங்கே அனுப்பப்படும்:',
        'footer': '🇮🇳 தேசிய சைபர் கிரைம் உதவி எண்: 1930',
        'home': '🏠 முகப்பு'
    },
    'తెలుగు': {
        'title': 'అభయం - లాగిన్',
        'subtitle': 'భారతదేశపు మొట్టమొదటి బహుభాషా మోస గుర్తింపు వ్యవస్థ',
        'username': 'వినియోగదారు పేరు',
        'password': 'పాస్వర్డ్',
        'login': '🔐 లాగిన్',
        'register': '📝 నమోదు',
        'forgot_password': '❓ పాస్వర్డ్ మరచిపోయారా?',
        'enter_username': 'మీ వినియోగదారు పేరును నమోదు చేయండి',
        'enter_password': 'మీ పాస్వర్డ్ నమోదు చేయండి',
        'reset_password': 'పాస్వర్డ్ రీసెట్ చేయండి',
        'create_account': '📝 కొత్త ఖాతాను సృష్టించండి',
        'confirm_password': 'పాస్వర్డ్ నిర్ధారించండి',
        'email': 'ఇమెయిల్',
        'back_to_login': '← లాగిన్ పేజీకి వెళ్ళండి',
        'register_btn': '✅ నమోదు చేయండి',
        'invalid_credentials': 'తప్పు వినియోగదారు పేరు లేదా పాస్వర్డ్!',
        'registration_success': 'నమోదు విజయవంతమైంది! దయచేసి లాగిన్ అవ్వండి.',
        'username_exists': 'వినియోగదారు పేరు ఇప్పటికే ఉంది!',
        'passwords_not_match': 'పాస్వర్డ్‌లు సరిపోలడం లేదు!',
        'fill_all_fields': 'దయచేసి అన్ని ఫీల్డ్‌లను పూరించండి!',
        'user_not_found': 'వినియోగదారు పేరు కనుగొనబడలేదు!',
        'reset_demo': 'డెమో: పరీక్ష కోసం పాస్వర్డ్ ఉపయోగించండి',
        'reset_link': 'పాస్వర్డ్ రీసెట్ లింక్ ఇక్కడికి పంపబడుతుంది:',
        'footer': '🇮🇳 జాతీయ సైబర్ క్రైమ్ హెల్ప్‌లైన్: 1930',
        'home': '🏠 హోమ్'
    },
    'ಕನ್ನಡ': {
        'title': 'ಅಭಯಂ - ಲಾಗಿನ್',
        'subtitle': 'ಭಾರತದ ಮೊದಲ ಬಹುಭಾಷಾ ವಂಚನೆ ಪತ್ತೆ ವ್ಯವಸ್ಥೆ',
        'username': 'ಬಳಕೆದಾರ ಹೆಸರು',
        'password': 'ಪಾಸ್ವರ್ಡ್',
        'login': '🔐 ಲಾಗಿನ್',
        'register': '📝 ನೋಂದಣಿ',
        'forgot_password': '❓ ಪಾಸ್ವರ್ಡ್ ಮರೆತಿರಾ?',
        'enter_username': 'ನಿಮ್ಮ ಬಳಕೆದಾರ ಹೆಸರನ್ನು ನಮೂದಿಸಿ',
        'enter_password': 'ನಿಮ್ಮ ಪಾಸ್ವರ್ಡ್ ನಮೂದಿಸಿ',
        'reset_password': 'ಪಾಸ್ವರ್ಡ್ ಮರುಹೊಂದಿಸಿ',
        'create_account': '📝 ಹೊಸ ಖಾತೆಯನ್ನು ರಚಿಸಿ',
        'confirm_password': 'ಪಾಸ್ವರ್ಡ್ ದೃಢೀಕರಿಸಿ',
        'email': 'ಇಮೇಲ್',
        'back_to_login': '← ಲಾಗಿನ್ ಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ',
        'register_btn': '✅ ನೋಂದಣಿ ಮಾಡಿ',
        'invalid_credentials': 'ತಪ್ಪಾದ ಬಳಕೆದಾರ ಹೆಸರು ಅಥವಾ ಪಾಸ್ವರ್ಡ್!',
        'registration_success': 'ನೋಂದಣಿ ಯಶಸ್ವಿಯಾಗಿದೆ! ದಯವಿಟ್ಟು ಲಾಗಿನ್ ಮಾಡಿ.',
        'username_exists': 'ಬಳಕೆದಾರ ಹೆಸರು ಈಗಾಗಲೇ ಅಸ್ತಿತ್ವದಲ್ಲಿದೆ!',
        'passwords_not_match': 'ಪಾಸ್ವರ್ಡ್‌ಗಳು ಹೊಂದಾಣಿಕೆಯಾಗುತ್ತಿಲ್ಲ!',
        'fill_all_fields': 'ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಕ್ಷೇತ್ರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ!',
        'user_not_found': 'ಬಳಕೆದಾರ ಹೆಸರು ಕಂಡುಬಂದಿಲ್ಲ!',
        'reset_demo': 'ಡೆಮೊ: ಪರೀಕ್ಷೆಗಾಗಿ ಪಾಸ್ವರ್ಡ್ ಅನ್ನು ಬಳಸಿ',
        'reset_link': 'ಪಾಸ್ವರ್ಡ್ ಮರುಹೊಂದಿಸುವ ಲಿಂಕ್ ಅನ್ನು ಇಲ್ಲಿ ಕಳುಹಿಸಲಾಗುವುದು:',
        'footer': '🇮🇳 ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಕ್ರೈಂ ಸಹಾಯವಾಣಿ: 1930',
        'home': '🏠 ಮುಖಪುಟ'
    },
    'മലയാളം': {
        'title': 'അഭയം - ലോഗിൻ',
        'subtitle': 'ഇന്ത്യയിലെ ആദ്യത്തെ ബഹുഭാഷാ തട്ടിപ്പ് കണ്ടെത്തൽ സംവിധാനം',
        'username': 'ഉപയോക്തൃനാമം',
        'password': 'പാസ്വേഡ്',
        'login': '🔐 ലോഗിൻ',
        'register': '📝 രജിസ്റ്റർ',
        'forgot_password': '❓ പാസ്വേഡ് മറന്നോ?',
        'enter_username': 'നിങ്ങളുടെ ഉപയോക്തൃനാമം നൽകുക',
        'enter_password': 'നിങ്ങളുടെ പാസ്വേഡ് നൽകുക',
        'reset_password': 'പാസ്വേഡ് പുനഃസജ്ജമാക്കുക',
        'create_account': '📝 പുതിയ അക്കൗണ്ട് സൃഷ്ടിക്കുക',
        'confirm_password': 'പാസ്വേഡ് സ്ഥിരീകരിക്കുക',
        'email': 'ഇമെയിൽ',
        'back_to_login': '← ലോഗിൻ പേജിലേക്ക് മടങ്ങുക',
        'register_btn': '✅ രജിസ്റ്റർ ചെയ്യുക',
        'invalid_credentials': 'തെറ്റായ ഉപയോക്തൃനാമം അല്ലെങ്കിൽ പാസ്വേഡ്!',
        'registration_success': 'രജിസ്ട്രേഷൻ വിജയകരം! ദയവായി ലോഗിൻ ചെയ്യുക.',
        'username_exists': 'ഉപയോക്തൃനാമം നിലവിലുണ്ട്!',
        'passwords_not_match': 'പാസ്വേഡുകൾ പൊരുത്തപ്പെടുന്നില്ല!',
        'fill_all_fields': 'ദയവായി എല്ലാ ഫീൽഡുകളും പൂരിപ്പിക്കുക!',
        'user_not_found': 'ഉപയോക്തൃനാമം കണ്ടെത്തിയില്ല!',
        'reset_demo': 'ഡെമോ: പരിശോധനയ്ക്കായി പാസ്വേഡ് ഉപയോഗിക്കുക',
        'reset_link': 'പാസ്വേഡ് പുനഃസജ്ജീകരണ ലിങ്ക് ഇവിടെ അയയ്ക്കും:',
        'footer': '🇮🇳 ദേശീയ സൈബർ ക്രൈം ഹെൽപ്പ്‌ലൈൻ: 1930',
        'home': '🏠 ഹോം'
    },
    'ગુજરાતી': {
        'title': 'અભયમ - લોગિન',
        'subtitle': 'ભારતની પ્રથમ બહુભાષીય છેતરપિંડી શોધ પ્રણાલી',
        'username': 'યૂઝરનામ',
        'password': 'પાસવર્ડ',
        'login': '🔐 લોગિન',
        'register': '📝 નોંધણી',
        'forgot_password': '❓ પાસવર્ડ ભૂલી ગયા?',
        'enter_username': 'તમારું યૂઝરનામ દાખલ કરો',
        'enter_password': 'તમારો પાસવર્ડ દાખલ કરો',
        'reset_password': 'પાસવર્ડ રીસેટ કરો',
        'create_account': '📝 નવું ખાતું બનાવો',
        'confirm_password': 'પાસવર્ડની પુષ્ટિ કરો',
        'email': 'ઇમેઇલ',
        'back_to_login': '← લોગિન પર પાછા જાઓ',
        'register_btn': '✅ નોંધણી કરો',
        'invalid_credentials': 'અમાન્ય યૂઝરનામ અથવા પાસવર્ડ!',
        'registration_success': 'નોંધણી સફળ! કૃપા કરી લોગિન કરો.',
        'username_exists': 'યૂઝરનામ પહેલેથી અસ્તિત્વમાં છે!',
        'passwords_not_match': 'પાસવર્ડ મેળ ખાતા નથી!',
        'fill_all_fields': 'કૃપા કરી બધા ફીલ્ડ ભરો!',
        'user_not_found': 'યૂઝરનામ મળ્યું નથી!',
        'reset_demo': 'ડેમો: પરીક્ષણ માટે પાસવર્ડનો ઉપયોગ કરો',
        'reset_link': 'પાસવર્ડ રીસેટ લિંક અહીં મોકલવામાં આવશે:',
        'footer': '🇮🇳 રાષ્ટ્રીય સાયબર ક્રાઇમ હેલ્પલાઇન: 1930',
        'home': '🏠 હોમ'
    },
    'ਪੰਜਾਬੀ': {
        'title': 'ਅਭਯਮ - ਲੌਗਿਨ',
        'subtitle': 'ਭਾਰਤ ਦੀ ਪਹਿਲੀ ਬਹੁ-ਭਾਸ਼ਾਈ ਧੋਖਾਧੜੀ ਖੋਜ ਪ੍ਰਣਾਲੀ',
        'username': 'ਉਪਭੋਗਤਾ ਨਾਮ',
        'password': 'ਪਾਸਵਰਡ',
        'login': '🔐 ਲੌਗਿਨ',
        'register': '📝 ਰਜਿਸਟਰ',
        'forgot_password': '❓ ਪਾਸਵਰਡ ਭੁੱਲ ਗਏ?',
        'enter_username': 'ਆਪਣਾ ਉਪਭੋਗਤਾ ਨਾਮ ਦਰਜ ਕਰੋ',
        'enter_password': 'ਆਪਣਾ ਪਾਸਵਰਡ ਦਰਜ ਕਰੋ',
        'reset_password': 'ਪਾਸਵਰਡ ਰੀਸੈਟ ਕਰੋ',
        'create_account': '📝 ਨਵਾਂ ਖਾਤਾ ਬਣਾਓ',
        'confirm_password': 'ਪਾਸਵਰਡ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ',
        'email': 'ਈਮੇਲ',
        'back_to_login': '← ਲੌਗਿਨ ਤੇ ਵਾਪਸ ਜਾਓ',
        'register_btn': '✅ ਰਜਿਸਟਰ ਕਰੋ',
        'invalid_credentials': 'ਗਲਤ ਉਪਭੋਗਤਾ ਨਾਮ ਜਾਂ ਪਾਸਵਰਡ!',
        'registration_success': 'ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਸਫਲ! ਕਿਰਪਾ ਕਰਕੇ ਲੌਗਿਨ ਕਰੋ।',
        'username_exists': 'ਉਪਭੋਗਤਾ ਨਾਮ ਪਹਿਲਾਂ ਤੋਂ ਮੌਜੂਦ ਹੈ!',
        'passwords_not_match': 'ਪਾਸਵਰਡ ਮੇਲ ਨਹੀਂ ਖਾਂਦੇ!',
        'fill_all_fields': 'ਕਿਰਪਾ ਕਰਕੇ ਸਾਰੇ ਫੀਲਡ ਭਰੋ!',
        'user_not_found': 'ਉਪਭੋਗਤਾ ਨਾਮ ਨਹੀਂ ਮਿਲਿਆ!',
        'reset_demo': 'ਡੈਮੋ: ਟੈਸਟਿੰਗ ਲਈ ਪਾਸਵਰਡ ਵਰਤੋ',
        'reset_link': 'ਪਾਸਵਰਡ ਰੀਸੈਟ ਲਿੰਕ ਇੱਥੇ ਭੇਜਿਆ ਜਾਵੇਗਾ:',
        'footer': '🇮🇳 ਰਾਸ਼ਟਰੀ ਸਾਈਬਰ ਕ੍ਰਾਈਮ ਹੈਲਪਲਾਈਨ: 1930',
        'home': '🏠 ਹੋਮ'
    },
    'বাংলা': {
        'title': 'অভয় - লগইন',
        'subtitle': 'ভারতের প্রথম বহুভাষিক জালিয়াতি সনাক্তকরণ ব্যবস্থা',
        'username': 'ব্যবহারকারীর নাম',
        'password': 'পাসওয়ার্ড',
        'login': '🔐 লগইন',
        'register': '📝 নিবন্ধন',
        'forgot_password': '❓ পাসওয়ার্ড ভুলে গেছেন?',
        'enter_username': 'আপনার ব্যবহারকারীর নাম লিখুন',
        'enter_password': 'আপনার পাসওয়ার্ড লিখুন',
        'reset_password': 'পাসওয়ার্ড রিসেট করুন',
        'create_account': '📝 নতুন অ্যাকাউন্ট তৈরি করুন',
        'confirm_password': 'পাসওয়ার্ড নিশ্চিত করুন',
        'email': 'ইমেইল',
        'back_to_login': '← লগইন পৃষ্ঠায় ফিরে যান',
        'register_btn': '✅ নিবন্ধন করুন',
        'invalid_credentials': 'ভুল ব্যবহারকারীর নাম বা পাসওয়ার্ড!',
        'registration_success': 'নিবন্ধন সফল! অনুগ্রহ করে লগইন করুন।',
        'username_exists': 'ব্যবহারকারীর নাম ইতিমধ্যে বিদ্যমান!',
        'passwords_not_match': 'পাসওয়ার্ড মেলে না!',
        'fill_all_fields': 'অনুগ্রহ করে সব ফিল্ড পূরণ করুন!',
        'user_not_found': 'ব্যবহারকারীর নাম পাওয়া যায়নি!',
        'reset_demo': 'ডেমো: পরীক্ষার জন্য পাসওয়ার্ড ব্যবহার করুন',
        'reset_link': 'পাসওয়ার্ড রিসেট লিংক এখানে পাঠানো হবে:',
        'footer': '🇮🇳 জাতীয় সাইবার ক্রাইম হেল্পলাইন: 1930',
        'home': '🏠 হোম'
    }
}

# Get language and redirect from query params
lang = st.query_params.get("lang", "English")
redirect = st.query_params.get("redirect", "pages/english.py")

# Set page config
st.set_page_config(
    page_title="अभयम् - Login",
    page_icon="🛡️",
    layout="centered"
)

# Get current language
current_lang = lang if lang in LANG_TEXTS else 'English'
texts = LANG_TEXTS[current_lang]

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FDFBD4 0%, #F5F5DC 100%);
    }
    .login-container {
        max-width: 450px;
        margin: auto;
        padding: 2rem;
        background: rgba(10, 12, 16, 0.85);
        border-radius: 32px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(24, 183, 190, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .title {
        text-align: center;
        margin-bottom: 2rem;
    }
    .title h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #18B7BE, #FEDD89);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #9BB8C9;
        font-size: 0.8rem;
    }
    .home-button {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Home button to go back
st.markdown('<div class="home-button">', unsafe_allow_html=True)
if st.button(texts['home'], use_container_width=True):
    st.switch_page(redirect)
st.markdown('</div>', unsafe_allow_html=True)

# Language selector in sidebar
with st.sidebar:
    st.markdown("### 🌐 Language / भाषा")
    lang_options = list(LANG_TEXTS.keys())
    selected_lang = st.selectbox("Select Language", lang_options, index=lang_options.index(current_lang))
    if selected_lang != current_lang:
        st.query_params["lang"] = selected_lang
        st.query_params["redirect"] = redirect
        st.rerun()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'show_register' not in st.session_state:
    st.session_state.show_register = False

# Login Page
st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown(f'<div class="title"><h1>🛡️ अभयम्</h1><p style="color:#9BB8C9;">{texts["subtitle"]}</p></div>', unsafe_allow_html=True)

if not st.session_state.show_register:
    # Login Form
    with st.form("login_form"):
        username = st.text_input(texts['username'], placeholder=texts['enter_username'])
        password = st.text_input(texts['password'], type="password", placeholder=texts['enter_password'])
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button(texts['login'], use_container_width=True)
        with col2:
            register_btn = st.form_submit_button(texts['register'], use_container_width=True)
        
        if submit:
            users = load_users()
            if username in users and users[username]['password_hash'] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.switch_page(redirect)
            else:
                st.error(texts['invalid_credentials'])
        
        if register_btn:
            st.session_state.show_register = True
            st.rerun()
    
    # Forgot Password
    with st.expander(texts['forgot_password']):
        forgot_username = st.text_input(texts['username'])
        if st.button(texts['reset_password']):
            users = load_users()
            if forgot_username in users:
                st.info(f"{texts['reset_link']} {users[forgot_username]['email']}")
                st.info(texts['reset_demo'])
            else:
                st.error(texts['user_not_found'])

else:
    # Registration Form
    st.markdown(f"### {texts['create_account']}")
    with st.form("register_form"):
        new_username = st.text_input(texts['username'])
        new_password = st.text_input(texts['password'], type="password")
        confirm_password = st.text_input(texts['confirm_password'], type="password")
        new_email = st.text_input(texts['email'])
        
        col1, col2 = st.columns(2)
        with col1:
            register = st.form_submit_button(texts['register_btn'], use_container_width=True)
        with col2:
            back_btn = st.form_submit_button(texts['back_to_login'], use_container_width=True)
        
        if register:
            if new_username and new_password and new_email:
                if new_password == confirm_password:
                    users = load_users()
                    if new_username not in users:
                        users[new_username] = {
                            "password_hash": hash_password(new_password),
                            "email": new_email,
                            "created_at": datetime.now().isoformat()
                        }
                        save_users(users)
                        st.success(texts['registration_success'])
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(texts['username_exists'])
                else:
                    st.error(texts['passwords_not_match'])
            else:
                st.error(texts['fill_all_fields'])
        
        if back_btn:
            st.session_state.show_register = False
            st.rerun()

st.markdown(f'<div class="footer"><p>{texts["footer"]}</p></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)