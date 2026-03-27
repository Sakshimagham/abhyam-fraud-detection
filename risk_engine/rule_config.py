# risk_engine/rule_config.py
"""
Enhanced Rule Configuration – Complete for All Fraud Types & 10 Languages
Fraud Types: SMS/Email, Call, Crypto, Fake Job, Social Media, Website
Languages: Marathi, Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Bengali, Punjabi, English, Hinglish
"""

# ============================================
# 1. LANGUAGE-SPECIFIC SCAM PATTERNS
# ============================================

# ---- MARATHI (मराठी) ----
MARATHI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'बँक', 'खाते', 'एटीएम', 'पिन', 'ओटीपी', 'केवाईसी', 'बंद', 'अपडेट',
            'डेबिट', 'क्रेडिट', 'कार्ड', 'बॅलन्स', 'रक्कम', 'व्याज', 'कर्ज',
            'एसबीआय', 'एचडीएफसी', 'आयसीआयसीआय', 'फसवणूक', 'ब्लॉक', 'सुरक्षा'
        ],
        'weight': 25,
        'description': 'बँक संबंधित फसवणूक',
        'helpline': 'बँक हेल्पलाइन: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'बक्षीस', 'लॉटरी', 'जिंकलात', 'पैसे', 'रक्कम', 'कूपन', 'ऑफर',
            'स्कीम', 'योजना', 'भेट', 'फ्री', 'मोफत', 'डिस्काउंट', 'सूट',
            'आयफोन', 'गाडी', 'नशीब', 'विजेता', 'निवडले', 'दावा करा'
        ],
        'weight': 35,
        'description': 'बक्षीस/लॉटरी फसवणूक',
        'helpline': 'सायबर सेल: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'सरकार', 'पोलीस', 'कोर्ट', 'नोटीस', 'दंड', 'आधार', 'पॅन',
            'जीएसटी', 'आयकर', 'व्होटर', 'राशन', 'डिजिटल अटक', 'वॉरंट',
            'सीबीआय', 'ईडी', 'तपास', 'खटला', 'न्यायाधीश'
        ],
        'weight': 40,
        'description': 'सरकारी अधिकारी बनून फसवणूक',
        'helpline': 'पोलीस हेल्पलाइन: 100'
    },
    'job_fraud': {
        'keywords': [
            'नोकरी', 'जॉब', 'फी', 'पैसे भरा', 'रजिस्ट्रेशन', 'ट्रेनिंग',
            'घरबसल्या', 'पार्ट टाइम', 'डेटा एंट्री', 'कमिशन', 'वर्क फ्रॉम होम',
            'यूट्यूब', 'लाईक', 'रिव्ह्यू', 'रेटिंग', 'टास्क', 'जॉइनिंग बोनस'
        ],
        'weight': 35,
        'description': 'बनावट नोकरी ऑफर',
        'helpline': 'श्रम मंत्रालय: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'क्रिप्टो', 'बिटकॉइन', 'इथेरियम', 'इन्व्हेस्टमेंट', 'डबल', 'दुप्पट',
            'गॅरंटी', 'गॅरंटीड', 'क्लाउड मायनिंग', 'ट्रेडिंग', 'आर्बिट्राज',
            'विथड्रॉवल', 'एएमएल', 'टॅक्स', 'रिस्क कंट्रोल'
        ],
        'weight': 35,
        'description': 'क्रिप्टो गुंतवणूक फसवणूक',
        'helpline': 'सायबर सेल: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'तातडीचे', 'लगेच', 'आज', 'उद्या', 'शेवटची', 'बंद होणार',
            'एक्सपायर', 'थांबा', 'ताबडतोब', 'आत्ताच', '२४ तास', 'तुरंत'
        ],
        'weight': 25,
        'description': 'तातडीची कारवाईचा दबाव',
        'helpline': 'मदत हेल्पलाइन: 181'
    },
    'social_scam': {
        'keywords': [
            'फेसबुक', 'इन्स्टाग्राम', 'व्हॉट्सअॅप', 'टेलिग्राम', 'मैत्री', 'रोमान्स',
            'प्रेम', 'भेट', 'गिफ्ट', 'व्हिडिओ कॉल', 'अश्लील', 'ब्लॅकमेल'
        ],
        'weight': 30,
        'description': 'सोशल मीडिया फसवणूक',
        'helpline': 'महिला हेल्पलाइन: 1091'
    }
}

# ---- HINDI (हिंदी) ----
HINDI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'बैंक', 'खाता', 'एटीएम', 'पिन', 'ओटीपी', 'केवाईसी', 'बंद', 'अपडेट',
            'डेबिट', 'क्रेडिट', 'कार्ड', 'बैलेंस', 'रकम', 'ब्याज', 'कर्ज',
            'एसबीआई', 'एचडीएफसी', 'आईसीआईसीआई', 'धोखाधड़ी', 'ब्लॉक', 'सुरक्षा'
        ],
        'weight': 25,
        'description': 'बैंक संबंधित धोखाधड़ी',
        'helpline': 'बैंक हेल्पलाइन: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'इनाम', 'लॉटरी', 'जीत', 'पैसे', 'रकम', 'कूपन', 'ऑफर',
            'स्कीम', 'योजना', 'गिफ्ट', 'फ्री', 'मुफ्त', 'डिस्काउंट', 'छूट',
            'आईफोन', 'गाड़ी', 'किस्मत', 'विजेता', 'चयनित', 'दावा करें'
        ],
        'weight': 35,
        'description': 'इनाम/लॉटरी धोखाधड़ी',
        'helpline': 'साइबर सेल: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'सरकार', 'पुलिस', 'कोर्ट', 'नोटिस', 'जुर्माना', 'आधार', 'पैन',
            'जीएसटी', 'इनकम टैक्स', 'वोटर', 'राशन', 'डिजिटल अरेस्ट', 'वारंट',
            'सीबीआई', 'ईडी', 'जांच', 'केस', 'जज'
        ],
        'weight': 40,
        'description': 'सरकारी अधिकारी बनकर धोखाधड़ी',
        'helpline': 'पुलिस हेल्पलाइन: 100'
    },
    'job_fraud': {
        'keywords': [
            'नौकरी', 'जॉब', 'फीस', 'पैसे जमा करें', 'रजिस्ट्रेशन', 'ट्रेनिंग',
            'घर बैठे', 'पार्ट टाइम', 'डाटा एंट्री', 'कमीशन', 'वर्क फ्रॉम होम',
            'यूट्यूब', 'लाइक', 'रिव्यू', 'रेटिंग', 'टास्क', 'ज्वाइनिंग बोनस'
        ],
        'weight': 35,
        'description': 'नकली नौकरी ऑफर',
        'helpline': 'श्रम मंत्रालय: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'क्रिप्टो', 'बिटकॉइन', 'एथेरियम', 'निवेश', 'डबल', 'दोगुना',
            'गारंटी', 'गारंटीड', 'क्लाउड माइनिंग', 'ट्रेडिंग', 'आर्बिट्रेज',
            'विदड्रॉवल', 'एएमएल', 'टैक्स', 'रिस्क कंट्रोल', 'पिग बूचरिंग'
        ],
        'weight': 35,
        'description': 'क्रिप्टो निवेश धोखाधड़ी',
        'helpline': 'साइबर सेल: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'तुरंत', 'अभी', 'आज', 'कल', 'आखिरी', 'बंद हो रहा',
            'एक्सपायर', 'जल्दी', 'तत्काल', '२४ घंटे', 'अभी करें'
        ],
        'weight': 25,
        'description': 'तत्काल कार्रवाई का दबाव',
        'helpline': 'मदद हेल्पलाइन: 181'
    },
    'social_scam': {
        'keywords': [
            'फेसबुक', 'इंस्टाग्राम', 'व्हाट्सएप', 'टेलीग्राम', 'दोस्ती', 'रोमांस',
            'प्यार', 'मिलन', 'गिफ्ट', 'वीडियो कॉल', 'अश्लील', 'ब्लैकमेल'
        ],
        'weight': 30,
        'description': 'सोशल मीडिया धोखाधड़ी',
        'helpline': 'महिला हेल्पलाइन: 1091'
    }
}

# ---- TAMIL (தமிழ்) ----
TAMIL_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'வங்கி', 'கணக்கு', 'ஏடிஎம்', 'பின்', 'ஓடிபி', 'கேஒய்சி', 'மூடல்', 'புதுப்பிப்பு',
            'டெபிட்', 'கிரெடிட்', 'கார்டு', 'இருப்பு', 'தொகை', 'வட்டி', 'கடன்',
            'எஸ்பிஐ', 'எச்டிஎப்சி', 'ஐசிஐசிஐ', 'மோசடி', 'தடுப்பு'
        ],
        'weight': 25,
        'description': 'வங்கி மோசடி',
        'helpline': 'வங்கி உதவி எண்: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'பரிசு', 'லாட்டரி', 'வெற்றி', 'பணம்', 'தொகை', 'கூப்பன்', 'சலுகை',
            'திட்டம்', 'இலவசம்', 'தள்ளுபடி', 'ஐபோன்', 'கார்', 'அதிர்ஷ்டம்',
            'வெற்றியாளர்', 'தேர்வு', 'கோரிக்கை'
        ],
        'weight': 35,
        'description': 'பரிசு/லாட்டரி மோசடி',
        'helpline': 'சைபர் செல்: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'அரசு', 'போலீஸ்', 'நீதிமன்றம்', 'நோட்டீஸ்', 'அபராதம்', 'ஆதார்', 'பான்',
            'ஜிஎஸ்டி', 'வருமான வரி', 'வாக்காளர்', 'ரேஷன்', 'டிஜிட்டல் கைது', 'வாரண்ட்',
            'சிபிஐ', 'ஈடி', 'வழக்கு', 'நீதிபதி'
        ],
        'weight': 40,
        'description': 'அரசு அதிகாரி போல் மோசடி',
        'helpline': 'போலீஸ் உதவி: 100'
    },
    'job_fraud': {
        'keywords': [
            'வேலை', 'பதவி', 'கட்டணம்', 'பணம் செலுத்து', 'பதிவு', 'பயிற்சி',
            'வீட்டிலிருந்து', 'பகுதி நேரம்', 'தரவு உள்ளீடு', 'தரகு', 'வேலை வீட்டில்',
            'யூடியூப்', 'லைக்', 'விமர்சனம்', 'மதிப்பீடு', 'பணி', 'சேரும் போனஸ்'
        ],
        'weight': 35,
        'description': 'போலி வேலை சலுகை',
        'helpline': 'தொழிலாளர் அமைச்சகம்: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'கிரிப்டோ', 'பிட்காயின்', 'எத்தீரியம்', 'முதலீடு', 'இரட்டிப்பு',
            'உத்தரவாதம்', 'உத்தரவாத', 'கிளவுட் மைனிங்', 'வர்த்தகம்', 'ஆர்பிட்ரேஜ்',
            'பணம் எடுப்பு', 'ஏஎம்எல்', 'வரி', 'இடர் கட்டுப்பாடு'
        ],
        'weight': 35,
        'description': 'கிரிப்டோ முதலீட்டு மோசடி',
        'helpline': 'சைபர் செல்: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'அவசரம்', 'இப்போது', 'இன்று', 'நாளை', 'கடைசி', 'மூடப்படும்',
            'காலாவதி', 'உடனடி', '24 மணி', 'உடனே'
        ],
        'weight': 25,
        'description': 'அவசர நடவடிக்கை அழுத்தம்',
        'helpline': 'உதவி எண்: 181'
    },
    'social_scam': {
        'keywords': [
            'பேஸ்புக்', 'இன்ஸ்டாகிராம்', 'வாட்ஸ்அப்', 'டெலிகிராம்', 'நட்பு', 'காதல்',
            'அன்பு', 'சந்திப்பு', 'பரிசு', 'வீடியோ அழைப்பு', 'ஆபாச', 'மிரட்டல்'
        ],
        'weight': 30,
        'description': 'சமூக ஊடக மோசடி',
        'helpline': 'பெண்கள் உதவி: 1091'
    }
}

# ---- TELUGU (తెలుగు) ----
TELUGU_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'బ్యాంక్', 'ఖాతా', 'ఏటీఎం', 'పిన్', 'ఓటిపి', 'కేవైసీ', 'మూసివేత', 'అప్డేట్',
            'డెబిట్', 'క్రెడిట్', 'కార్డు', 'బ్యాలెన్స్', 'మొత్తం', 'వడ్డీ', 'రుణం',
            'ఎస్బీఐ', 'ఎచ్డీఎఫ్సీ', 'ఐసీఐసీఐ', 'మోసం', 'బ్లాక్'
        ],
        'weight': 25,
        'description': 'బ్యాంక్ మోసం',
        'helpline': 'బ్యాంక్ హెల్ప్‌లైన్: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'బహుమతి', 'లాటరీ', 'గెలుపు', 'డబ్బు', 'మొత్తం', 'కూపన్', 'ఆఫర్',
            'పథకం', 'ఉచితం', 'తగ్గింపు', 'ఐఫోన్', 'కారు', 'అదృష్టం',
            'విజేత', 'ఎంపిక', 'క్లెయిమ్'
        ],
        'weight': 35,
        'description': 'బహుమతి/లాటరీ మోసం',
        'helpline': 'సైబర్ సెల్: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'ప్రభుత్వం', 'పోలీస్', 'కోర్ట్', 'నోటీసు', 'జరిమానా', 'ఆధార్', 'పాన్',
            'జీఎస్టీ', 'ఆదాయపు పన్ను', 'ఓటరు', 'రేషన్', 'డిజిటల్ అరెస్ట్', 'వారెంట్',
            'సీబీఐ', 'ఈడీ', 'కేసు', 'న్యాయమూర్తి'
        ],
        'weight': 40,
        'description': 'ప్రభుత్వ అధికారిగా మోసం',
        'helpline': 'పోలీస్ హెల్ప్‌లైన్: 100'
    },
    'job_fraud': {
        'keywords': [
            'ఉద్యోగం', 'జాబ్', 'రుసుము', 'డబ్బు చెల్లించండి', 'రిజిస్ట్రేషన్', 'శిక్షణ',
            'ఇంటి నుండి', 'పార్ట్ టైమ్', 'డేటా ఎంట్రీ', 'కమీషన్', 'వర్క్ ఫ్రమ్ హోమ్',
            'యూట్యూబ్', 'లైక్', 'రివ్యూ', 'రేటింగ్', 'టాస్క్', 'జాయినింగ్ బోనస్'
        ],
        'weight': 35,
        'description': 'నకిలీ ఉద్యోగ ఆఫర్',
        'helpline': 'కార్మిక మంత్రిత్వ శాఖ: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'క్రిప్టో', 'బిట్కాయిన్', 'ఇథీరియం', 'పెట్టుబడి', 'రెట్టింపు',
            'గ్యారంటీ', 'గ్యారంటీడ్', 'క్లౌడ్ మైనింగ్', 'ట్రేడింగ్', 'ఆర్బిట్రేజ్',
            'విత్డ్రావల్', 'ఏఎంఎల్', 'టాక్స్', 'రిస్క్ కంట్రోల్'
        ],
        'weight': 35,
        'description': 'క్రిప్టో ఇన్వెస్ట్మెంట్ మోసం',
        'helpline': 'సైబర్ సెల్: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'అత్యవసరం', 'ఇప్పుడే', 'ఈరోజు', 'రేపు', 'చివరి', 'మూసివేత',
            'గడువు', 'వెంటనే', '24 గంటలు', 'వెంటనే'
        ],
        'weight': 25,
        'description': 'అత్యవసర చర్య ఒత్తిడి',
        'helpline': 'సహాయం: 181'
    },
    'social_scam': {
        'keywords': [
            'ఫేస్బుక్', 'ఇన్స్టాగ్రామ్', 'వాట్సాప్', 'టెలిగ్రామ్', 'స్నేహం', 'రొమాన్స్',
            'ప్రేమ', 'కలయిక', 'గిఫ్ట్', 'వీడియో కాల్', 'అశ్లీల', 'బ్లాక్మెయిల్'
        ],
        'weight': 30,
        'description': 'సోషల్ మీడియా మోసం',
        'helpline': 'మహిళా హెల్ప్లైన్: 1091'
    }
}

# ---- KANNADA (ಕನ್ನಡ) ----
KANNADA_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'ಬ್ಯಾಂಕ್', 'ಖಾತೆ', 'ಎಟಿಎಂ', 'ಪಿನ್', 'ಒಟಿಪಿ', 'ಕೆವೈಸಿ', 'ಮುಚ್ಚುವಿಕೆ', 'ಅಪ್ಡೇಟ್',
            'ಡೆಬಿಟ್', 'ಕ್ರೆಡಿಟ್', 'ಕಾರ್ಡ್', 'ಬ್ಯಾಲೆನ್ಸ್', 'ಮೊತ್ತ', 'ಬಡ್ಡಿ', 'ಸಾಲ',
            'ಎಸ್ಬಿಐ', 'ಎಚ್ಡಿಎಫ್ಸಿ', 'ಐಸಿಐಸಿಐ', 'ವಂಚನೆ', 'ಬ್ಲಾಕ್'
        ],
        'weight': 25,
        'description': 'ಬ್ಯಾಂಕ್ ವಂಚನೆ',
        'helpline': 'ಬ್ಯಾಂಕ್ ಹೆಲ್ಪ್‌ಲೈನ್: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'ಬಹುಮಾನ', 'ಲಾಟರಿ', 'ಗೆಲುವು', 'ಹಣ', 'ಮೊತ್ತ', 'ಕೂಪನ್', 'ಆಫರ್',
            'ಯೋಜನೆ', 'ಉಚಿತ', 'ರಿಯಾಯಿತಿ', 'ಐಫೋನ್', 'ಕಾರು', 'ಅದೃಷ್ಟ',
            'ವಿಜೇತ', 'ಆಯ್ಕೆ', 'ಕ್ಲೈಮ್'
        ],
        'weight': 35,
        'description': 'ಬಹುಮಾನ/ಲಾಟರಿ ವಂಚನೆ',
        'helpline': 'ಸೈಬರ್ ಸೆಲ್: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'ಸರ್ಕಾರ', 'ಪೋಲೀಸ್', 'ಕೋರ್ಟ್', 'ಸೂಚನೆ', 'ದಂಡ', 'ಆಧಾರ್', 'ಪಾನ್',
            'ಜಿಎಸ್ಟಿ', 'ಆದಾಯ ತೆರಿಗೆ', 'ಮತದಾರ', 'ರೇಷನ್', 'ಡಿಜಿಟಲ್ ಅರೆಸ್ಟ್', 'ವಾರಂಟ್',
            'ಸಿಬಿಐ', 'ಇಡಿ', 'ಪ್ರಕರಣ', 'ನ್ಯಾಯಾಧೀಶ'
        ],
        'weight': 40,
        'description': 'ಸರ್ಕಾರಿ ಅಧಿಕಾರಿಯಂತೆ ವಂಚನೆ',
        'helpline': 'ಪೋಲೀಸ್ ಸಹಾಯ: 100'
    },
    'job_fraud': {
        'keywords': [
            'ಉದ್ಯೋಗ', 'ಕೆಲಸ', 'ಶುಲ್ಕ', 'ಹಣ ಪಾವತಿಸಿ', 'ನೋಂದಣಿ', 'ತರಬೇತಿ',
            'ಮನೆಯಿಂದ', 'ಪಾರ್ಟ್ ಟೈಮ್', 'ಡೇಟಾ ಎಂಟ್ರಿ', 'ಕಮಿಷನ್', 'ವರ್ಕ್ ಫ್ರಮ್ ಹೋಮ್',
            'ಯೂಟ್ಯೂಬ್', 'ಲೈಕ್', 'ರಿವ್ಯೂ', 'ರೇಟಿಂಗ್', 'ಟಾಸ್ಕ್', 'ಜಾಯಿನಿಂಗ್ ಬೋನಸ್'
        ],
        'weight': 35,
        'description': 'ನಕಲಿ ಉದ್ಯೋಗ ಆಫರ್',
        'helpline': 'ಕಾರ್ಮಿಕ ಸಚಿವಾಲಯ: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'ಕ್ರಿಪ್ಟೋ', 'ಬಿಟ್ಕಾಯಿನ್', 'ಎಥೇರಿಯಮ್', 'ಹೂಡಿಕೆ', 'ಡಬಲ್', 'ದುಪ್ಪಟ್ಟು',
            'ಗ್ಯಾರಂಟಿ', 'ಗ್ಯಾರಂಟೀಡ್', 'ಕ್ಲೌಡ್ ಮೈನಿಂಗ್', 'ಟ್ರೇಡಿಂಗ್', 'ಆರ್ಬಿಟ್ರೇಜ್',
            'ವಿಥ್ಡ್ರಾವಲ್', 'ಎಎಂಎಲ್', 'ಟ್ಯಾಕ್ಸ್', 'ರಿಸ್ಕ್ ಕಂಟ್ರೋಲ್'
        ],
        'weight': 35,
        'description': 'ಕ್ರಿಪ್ಟೋ ಹೂಡಿಕೆ ವಂಚನೆ',
        'helpline': 'ಸೈಬರ್ ಸೆಲ್: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'ತುರ್ತು', 'ಈಗ', 'ಇಂದು', 'ನಾಳೆ', 'ಕೊನೆಯ', 'ಮುಚ್ಚುವಿಕೆ',
            'ಮುಕ್ತಾಯ', 'ತಕ್ಷಣ', '24 ಗಂಟೆ', 'ಈಗಲೇ'
        ],
        'weight': 25,
        'description': 'ತುರ್ತು ಕ್ರಮ ಒತ್ತಡ',
        'helpline': 'ಸಹಾಯ: 181'
    },
    'social_scam': {
        'keywords': [
            'ಫೇಸ್ಬುಕ್', 'ಇನ್ಸ್ಟಾಗ್ರಾಮ್', 'ವಾಟ್ಸಾಪ್', 'ಟೆಲಿಗ್ರಾಮ್', 'ಸ್ನೇಹ', 'ರೊಮ್ಯಾನ್ಸ್',
            'ಪ್ರೀತಿ', 'ಭೇಟಿ', 'ಉಡುಗೊರೆ', 'ವಿಡಿಯೋ ಕಾಲ್', 'ಅಶ್ಲೀಲ', 'ಬ್ಲ್ಯಾಕ್ಮೇಲ್'
        ],
        'weight': 30,
        'description': 'ಸಾಮಾಜಿಕ ಮಾಧ್ಯಮ ವಂಚನೆ',
        'helpline': 'ಮಹಿಳಾ ಹೆಲ್ಪ್ಲೈನ್: 1091'
    }
}

# ---- MALAYALAM (മലയാളം) ----
MALAYALAM_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'ബാങ്ക്', 'അക്കൗണ്ട്', 'എടിഎം', 'പിൻ', 'ഒടിപി', 'കെവൈസി', 'അടയ്ക്കൽ', 'അപ്ഡേറ്റ്',
            'ഡെബിറ്റ്', 'ക്രെഡിറ്റ്', 'കാർഡ്', 'ബാലൻസ്', 'തുക', 'പലിശ', 'വായ്പ',
            'എസ്ബിഐ', 'എച്ച്ഡിഎഫ്സി', 'ഐസിഐസിഐ', 'തട്ടിപ്പ്', 'ബ്ലോക്ക്'
        ],
        'weight': 25,
        'description': 'ബാങ്ക് തട്ടിപ്പ്',
        'helpline': 'ബാങ്ക് ഹെൽപ്പ്‌ലൈൻ: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'സമ്മാനം', 'ലോട്ടറി', 'വിജയം', 'പണം', 'തുക', 'കൂപ്പൺ', 'ഓഫർ',
            'പദ്ധതി', 'സൗജന്യം', 'കിഴിവ്', 'ഐഫോൺ', 'കാർ', 'ഭാഗ്യം',
            'വിജയി', 'തിരഞ്ഞെടുത്തു', 'ക്ലെയിം'
        ],
        'weight': 35,
        'description': 'സമ്മാനം/ലോട്ടറി തട്ടിപ്പ്',
        'helpline': 'സൈബർ സെൽ: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'സർക്കാർ', 'പോലീസ്', 'കോടതി', 'അറിയിപ്പ്', 'പിഴ', 'ആധാർ', 'പാൻ',
            'ജിഎസ്ടി', 'ആദായ നികുതി', 'വോട്ടർ', 'റേഷൻ', 'ഡിജിറ്റൽ അറസ്റ്റ്', 'വാറന്റ്',
            'സിബിഐ', 'ഇഡി', 'കേസ്', 'ജഡ്ജി'
        ],
        'weight': 40,
        'description': 'സർക്കാർ ഉദ്യോഗസ്ഥനെന്ന വ്യാജേന തട്ടിപ്പ്',
        'helpline': 'പോലീസ് സഹായം: 100'
    },
    'job_fraud': {
        'keywords': [
            'ജോലി', 'തൊഴിൽ', 'ഫീസ്', 'പണം നൽകുക', 'രജിസ്ട്രേഷൻ', 'പരിശീലനം',
            'വീട്ടിൽ നിന്ന്', 'പാർട്ട് ടൈം', 'ഡാറ്റ എൻട്രി', 'കമ്മീഷൻ', 'വർക്ക് ഫ്രം ഹോം',
            'യൂട്യൂബ്', 'ലൈക്ക്', 'റിവ്യൂ', 'റേറ്റിംഗ്', 'ടാസ്ക്', 'ജോയിനിംഗ് ബോണസ്'
        ],
        'weight': 35,
        'description': 'വ്യാജ ജോലി ഓഫർ',
        'helpline': 'തൊഴിൽ മന്ത്രാലയം: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'ക്രിപ്റ്റോ', 'ബിറ്റ്കോയിൻ', 'എതീരിയം', 'നിക്ഷേപം', 'ഡബിൾ', 'ഇരട്ടി',
            'ഗ്യാരണ്ടി', 'ഗ്യാരണ്ടീഡ്', 'ക്ലൗഡ് മൈനിംഗ്', 'ട്രേഡിംഗ്', 'ആർബിട്രേജ്',
            'വിത്ഡ്രാവൽ', 'എഎംഎൽ', 'ടാക്സ്', 'റിസ്ക് കൺട്രോൾ'
        ],
        'weight': 35,
        'description': 'ക്രിപ്റ്റോ നിക്ഷേപ തട്ടിപ്പ്',
        'helpline': 'സൈബർ സെൽ: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'അടിയന്തര', 'ഇപ്പോൾ', 'ഇന്ന്', 'നാളെ', 'അവസാന', 'അടയ്ക്കൽ',
            'കാലഹരണപ്പെടൽ', 'ഉടൻ', '24 മണിക്കൂർ', 'ഉടനെ'
        ],
        'weight': 25,
        'description': 'അടിയന്തര നടപടി സമ്മർദ്ദം',
        'helpline': 'സഹായം: 181'
    },
    'social_scam': {
        'keywords': [
            'ഫേസ്ബുക്ക്', 'ഇൻസ്റ്റാഗ്രാം', 'വാട്സ്ആപ്പ്', 'ടെലിഗ്രാം', 'സൗഹൃദം', 'റൊമാൻസ്',
            'പ്രണയം', 'കൂടിക്കാഴ്ച', 'സമ്മാനം', 'വീഡിയോ കോൾ', 'അശ്ലീല', 'ബ്ലാക്ക്മെയിൽ'
        ],
        'weight': 30,
        'description': 'സോഷ്യൽ മീഡിയ തട്ടിപ്പ്',
        'helpline': 'വനിതാ ഹെൽപ്പ്‌ലൈൻ: 1091'
    }
}

# ---- GUJARATI (ગુજરાતી) ----
GUJARATI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'બેંક', 'ખાતું', 'એટીએમ', 'પિન', 'ઓટીપી', 'કેવાયસી', 'બંધ', 'અપડેટ',
            'ડેબિટ', 'ક્રેડિટ', 'કાર્ડ', 'બેલેન્સ', 'રકમ', 'વ્યાજ', 'લોન',
            'એસબીઆઈ', 'એચડીએફસી', 'આઈસીઆઈસીઆઈ', 'છેતરપિંડી', 'બ્લોક'
        ],
        'weight': 25,
        'description': 'બેંક છેતરપિંડી',
        'helpline': 'બેંક હેલ્પલાઇન: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'ઇનામ', 'લોટરી', 'જીત', 'પૈસા', 'રકમ', 'કૂપન', 'ઓફર',
            'યોજના', 'મફત', 'ડિસ્કાઉન્ટ', 'આઇફોન', 'ગાડી', 'નસીબ',
            'વિજેતા', 'પસંદગી', 'દાવો'
        ],
        'weight': 35,
        'description': 'ઇનામ/લોટરી છેતરપિંડી',
        'helpline': 'સાયબર સેલ: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'સરકાર', 'પોલીસ', 'કોર્ટ', 'નોટિસ', 'દંડ', 'આધાર', 'પાન',
            'જીએસટી', 'આવકવેરો', 'મતદાર', 'રેશન', 'ડિજિટલ અટક', 'વોરંટ',
            'સીબીઆઈ', 'ઈડી', 'કેસ', 'જજ'
        ],
        'weight': 40,
        'description': 'સરકારી અધિકારી બની છેતરપિંડી',
        'helpline': 'પોલીસ હેલ્પલાઇન: 100'
    },
    'job_fraud': {
        'keywords': [
            'નોકરી', 'જોબ', 'ફી', 'પૈસા ભરો', 'રજિસ્ટ્રેશન', 'તાલીમ',
            'ઘરેથી', 'પાર્ટ ટાઇમ', 'ડેટા એન્ટ્રી', 'કમિશન', 'વર્ક ફ્રોમ હોમ',
            'યુટ્યુબ', 'લાઇક', 'રિવ્યુ', 'રેટિંગ', 'ટાસ્ક', 'જોઇનિંગ બોનસ'
        ],
        'weight': 35,
        'description': 'નકલી નોકરી ઓફર',
        'helpline': 'શ્રમ મંત્રાલય: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'ક્રિપ્ટો', 'બિટકોઇન', 'ઇથેરિયમ', 'રોકાણ', 'ડબલ', 'બમણું',
            'ગેરંટી', 'ગેરંટીડ', 'ક્લાઉડ માઇનિંગ', 'ટ્રેડિંગ', 'આર્બિટ્રેજ',
            'વિથડ્રોઅલ', 'એએમએલ', 'ટેક્સ', 'રિસ્ક કંટ્રોલ'
        ],
        'weight': 35,
        'description': 'ક્રિપ્ટો રોકાણ છેતરપિંડી',
        'helpline': 'સાયબર સેલ: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'તાત્કાલિક', 'હમણાં', 'આજે', 'કાલે', 'છેલ્લી', 'બંધ',
            'સમાપ્તિ', 'તરત', '૨૪ કલાક', 'તરત જ'
        ],
        'weight': 25,
        'description': 'તાત્કાલિક કાર્યવાહી દબાણ',
        'helpline': 'મદદ: 181'
    },
    'social_scam': {
        'keywords': [
            'ફેસબુક', 'ઇન્સ્ટાગ્રામ', 'વોટ્સએપ', 'ટેલિગ્રામ', 'મિત્રતા', 'રોમાન્સ',
            'પ્રેમ', 'મુલાકાત', 'ગિફ્ટ', 'વિડિયો કોલ', 'અશ્લીલ', 'બ્લેકમેઇલ'
        ],
        'weight': 30,
        'description': 'સોશિયલ મીડિયા છેતરપિંડી',
        'helpline': 'મહિલા હેલ્પલાઇન: 1091'
    }
}

# ---- BENGALI (বাংলা) ----
BENGALI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'ব্যাঙ্ক', 'অ্যাকাউন্ট', 'এটিএম', 'পিন', 'ওটিপি', 'কেওয়াইসি', 'বন্ধ', 'আপডেট',
            'ডেবিট', 'ক্রেডিট', 'কার্ড', 'ব্যালেন্স', 'টাকা', 'সুদ', 'ঋণ',
            'এসবিআই', 'এইচডিএফসি', 'আইসিআইসিআই', 'জালিয়াতি', 'ব্লক'
        ],
        'weight': 25,
        'description': 'ব্যাঙ্ক জালিয়াতি',
        'helpline': 'ব্যাঙ্ক হেল্পলাইন: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'পুরস্কার', 'লটারি', 'জয়', 'টাকা', 'পরিমাণ', 'কুপন', 'অফার',
            'স্কিম', 'বিনামূল্যে', 'ডিসকাউন্ট', 'আইফোন', 'গাড়ি', 'ভাগ্য',
            'বিজয়ী', 'নির্বাচিত', 'দাবি'
        ],
        'weight': 35,
        'description': 'পুরস্কার/লটারি জালিয়াতি',
        'helpline': 'সাইবার সেল: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'সরকার', 'পুলিশ', 'কোর্ট', 'নোটিশ', 'জরিমানা', 'আধার', 'প্যান',
            'জিএসটি', 'আয়কর', 'ভোটার', 'রেশন', 'ডিজিটাল গ্রেপ্তার', 'ওয়ারেন্ট',
            'সিবিআই', 'ইডি', 'মামলা', 'বিচারক'
        ],
        'weight': 40,
        'description': 'সরকারি কর্মকর্তা সেজে জালিয়াতি',
        'helpline': 'পুলিশ হেল্পলাইন: 100'
    },
    'job_fraud': {
        'keywords': [
            'চাকরি', 'জব', 'ফি', 'টাকা জমা দিন', 'নিবন্ধন', 'প্রশিক্ষণ',
            'বাড়ি থেকে', 'পার্ট টাইম', 'ডাটা এন্ট্রি', 'কমিশন', 'ওয়ার্ক ফ্রম হোম',
            'ইউটিউব', 'লাইক', 'রিভিউ', 'রেটিং', 'টাস্ক', 'জয়েনিং বোনাস'
        ],
        'weight': 35,
        'description': 'নকল চাকরির অফার',
        'helpline': 'শ্রম মন্ত্রক: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'ক্রিপ্টো', 'বিটকয়েন', 'ইথেরিয়াম', 'বিনিয়োগ', 'ডাবল', 'দ্বিগুণ',
            'গ্যারান্টি', 'গ্যারান্টিড', 'ক্লাউড মাইনিং', 'ট্রেডিং', 'আরবিট্রেজ',
            'উইথড্রয়াল', 'এএমএল', 'ট্যাক্স', 'রিস্ক কন্ট্রোল'
        ],
        'weight': 35,
        'description': 'ক্রিপ্টো বিনিয়োগ জালিয়াতি',
        'helpline': 'সাইবার সেল: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'জরুরি', 'এখনই', 'আজ', 'কাল', 'শেষ', 'বন্ধ',
            'মেয়াদোত্তীর্ণ', 'অবিলম্বে', '২৪ ঘন্টা', 'এখন'
        ],
        'weight': 25,
        'description': 'জরুরি পদক্ষেপ চাপ',
        'helpline': 'সাহায্য: 181'
    },
    'social_scam': {
        'keywords': [
            'ফেসবুক', 'ইনস্টাগ্রাম', 'হোয়াটসঅ্যাপ', 'টেলিগ্রাম', 'বন্ধুত্ব', 'রোমান্স',
            'প্রেম', 'সাক্ষাৎ', 'উপহার', 'ভিডিও কল', 'অশ্লীল', 'ব্ল্যাকমেইল'
        ],
        'weight': 30,
        'description': 'সোশ্যাল মিডিয়া জালিয়াতি',
        'helpline': 'মহিলা হেল্পলাইন: 1091'
    }
}

# ---- PUNJABI (ਪੰਜਾਬੀ) ----
PUNJABI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'ਬੈਂਕ', 'ਖਾਤਾ', 'ਏਟੀਐਮ', 'ਪਿੰਨ', 'ਓਟੀਪੀ', 'ਕੇਵਾਈਸੀ', 'ਬੰਦ', 'ਅਪਡੇਟ',
            'ਡੈਬਿਟ', 'ਕ੍ਰੈਡਿਟ', 'ਕਾਰਡ', 'ਬੈਲੰਸ', 'ਰਕਮ', 'ਵਿਆਜ', 'ਕਰਜ਼',
            'ਐਸਬੀਆਈ', 'ਐਚਡੀਐਫਸੀ', 'ਆਈਸੀਆਈਸੀਆਈ', 'ਧੋਖਾਧੜੀ', 'ਬਲਾਕ'
        ],
        'weight': 25,
        'description': 'ਬੈਂਕ ਧੋਖਾਧੜੀ',
        'helpline': 'ਬੈਂਕ ਹੈਲਪਲਾਈਨ: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'ਇਨਾਮ', 'ਲਾਟਰੀ', 'ਜਿੱਤ', 'ਪੈਸੇ', 'ਰਕਮ', 'ਕੂਪਨ', 'ਆਫਰ',
            'ਸਕੀਮ', 'ਮੁਫਤ', 'ਛੂਟ', 'ਆਈਫੋਨ', 'ਗੱਡੀ', 'ਕਿਸਮਤ',
            'ਜੇਤੂ', 'ਚੁਣਿਆ', 'ਦਾਅਵਾ'
        ],
        'weight': 35,
        'description': 'ਇਨਾਮ/ਲਾਟਰੀ ਧੋਖਾਧੜੀ',
        'helpline': 'ਸਾਈਬਰ ਸੈੱਲ: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'ਸਰਕਾਰ', 'ਪੁਲਿਸ', 'ਕੋਰਟ', 'ਨੋਟਿਸ', 'ਜੁਰਮਾਨਾ', 'ਆਧਾਰ', 'ਪੈਨ',
            'ਜੀਐਸਟੀ', 'ਆਮਦਨ ਟੈਕਸ', 'ਵੋਟਰ', 'ਰਾਸ਼ਨ', 'ਡਿਜੀਟਲ ਗ੍ਰਿਫਤਾਰੀ', 'ਵਾਰੰਟ',
            'ਸੀਬੀਆਈ', 'ਈਡੀ', 'ਕੇਸ', 'ਜੱਜ'
        ],
        'weight': 40,
        'description': 'ਸਰਕਾਰੀ ਅਧਿਕਾਰੀ ਬਣ ਕੇ ਧੋਖਾਧੜੀ',
        'helpline': 'ਪੁਲਿਸ ਹੈਲਪਲਾਈਨ: 100'
    },
    'job_fraud': {
        'keywords': [
            'ਨੌਕਰੀ', 'ਜੌਬ', 'ਫੀ', 'ਪੈਸੇ ਜਮ੍ਹਾ ਕਰੋ', 'ਰਜਿਸਟ੍ਰੇਸ਼ਨ', 'ਸਿਖਲਾਈ',
            'ਘਰ ਬੈਠੇ', 'ਪਾਰਟ ਟਾਈਮ', 'ਡਾਟਾ ਐਂਟਰੀ', 'ਕਮਿਸ਼ਨ', 'ਵਰਕ ਫਰੌਮ ਹੋਮ',
            'ਯੂਟਿਊਬ', 'ਲਾਈਕ', 'ਰਿਵਿਊ', 'ਰੇਟਿੰਗ', 'ਟਾਸਕ', 'ਜੁਆਇਨਿੰਗ ਬੋਨਸ'
        ],
        'weight': 35,
        'description': 'ਨਕਲੀ ਨੌਕਰੀ ਆਫਰ',
        'helpline': 'ਸ਼੍ਰਮ ਮੰਤਰਾਲਾ: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'ਕ੍ਰਿਪਟੋ', 'ਬਿਟਕੋਇਨ', 'ਈਥੇਰੀਅਮ', 'ਨਿਵੇਸ਼', 'ਡਬਲ', 'ਦੁੱਗਣਾ',
            'ਗਾਰੰਟੀ', 'ਗਾਰੰਟੀ', 'ਕਲਾਉਡ ਮਾਈਨਿੰਗ', 'ਟ੍ਰੇਡਿੰਗ', 'ਆਰਬਿਟ੍ਰੇਜ',
            'ਵਿਥਡਰਾਵਲ', 'ਏਏਐਮਐਲ', 'ਟੈਕਸ', 'ਰਿਸਕ ਕੰਟਰੋਲ'
        ],
        'weight': 35,
        'description': 'ਕ੍ਰਿਪਟੋ ਨਿਵੇਸ਼ ਧੋਖਾਧੜੀ',
        'helpline': 'ਸਾਈਬਰ ਸੈੱਲ: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'ਜ਼ਰੂਰੀ', 'ਹੁਣੇ', 'ਅੱਜ', 'ਕੱਲ੍ਹ', 'ਆਖਰੀ', 'ਬੰਦ',
            'ਮਿਆਦ ਪੁੱਗਣ', 'ਤੁਰੰਤ', '24 ਘੰਟੇ', 'ਹੁਣੇ ਕਰੋ'
        ],
        'weight': 25,
        'description': 'ਜ਼ਰੂਰੀ ਕਾਰਵਾਈ ਦਬਾਅ',
        'helpline': 'ਮਦਦ: 181'
    },
    'social_scam': {
        'keywords': [
            'ਫੇਸਬੁੱਕ', 'ਇੰਸਟਾਗ੍ਰਾਮ', 'ਵਟਸਐਪ', 'ਟੈਲੀਗ੍ਰਾਮ', 'ਦੋਸਤੀ', 'ਰੋਮਾਂਸ',
            'ਪਿਆਰ', 'ਮੁਲਾਕਾਤ', 'ਤੋਹਫ਼ਾ', 'ਵੀਡੀਓ ਕਾਲ', 'ਅਸ਼ਲੀਲ', 'ਬਲੈਕਮੇਲ'
        ],
        'weight': 30,
        'description': 'ਸੋਸ਼ਲ ਮੀਡੀਆ ਧੋਖਾਧੜੀ',
        'helpline': 'ਮਹਿਲਾ ਹੈਲਪਲਾਈਨ: 1091'
    }
}

# ---- ENGLISH & HINGLISH ----
ENGLISH_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'bank', 'account', 'atm', 'pin', 'otp', 'kyc', 'blocked', 'update', 'verify',
            'debit', 'credit', 'card', 'balance', 'amount', 'interest', 'loan',
            'sbi', 'hdfc', 'icici', 'fraud', 'security', 'unauthorized', 'suspicious'
        ],
        'weight': 25,
        'description': 'Banking fraud',
        'helpline': 'Bank Helpline: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'prize', 'lottery', 'won', 'winner', 'selected', 'claim', 'cash', 'reward',
            'gift', 'free', 'discount', 'iphone', 'car', 'lucky', 'jackpot',
            'congratulations', 'you have won', 'claim now', 'limited time'
        ],
        'weight': 35,
        'description': 'Prize/Lottery fraud',
        'helpline': 'Cyber Cell: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'government', 'police', 'court', 'notice', 'fine', 'penalty', 'aadhaar', 'pan',
            'gst', 'income tax', 'voter', 'ration', 'digital arrest', 'warrant',
            'cbi', 'ed', 'case', 'judge', 'summons', 'nclt', 'cyber crime'
        ],
        'weight': 40,
        'description': 'Government impersonation fraud',
        'helpline': 'Police: 100'
    },
    'job_fraud': {
        'keywords': [
            'job', 'work from home', 'part time', 'data entry', 'commission', 'registration fee',
            'training fee', 'youtube', 'like', 'review', 'rating', 'task', 'joining bonus',
            'daily payment', 'no experience', 'easy money', 'remote work', 'freelance',
            'task scam', 'telegram job', 'whatsapp job', 'interview link', 'trojanned'
        ],
        'weight': 35,
        'description': 'Fake job offer scam',
        'helpline': 'Labour Ministry: 1800-XXX-XXXX'
    },
    'crypto_fraud': {
        'keywords': [
            'crypto', 'bitcoin', 'ethereum', 'investment', 'double', 'double your money',
            'guaranteed returns', 'cloud mining', 'trading', 'arbitrage', 'pig butchering',
            'withdrawal', 'aml', 'tax', 'risk control', 'pay to withdraw', 'fake exchange',
            'mining contract', 'fees to unlock', 'bonus unlock', 'trading mentor',
            'whatsapp group', 'telegram group', 'signal group', 'crypto scam'
        ],
        'weight': 35,
        'description': 'Crypto investment fraud',
        'helpline': 'Cyber Cell: 1930'
    },
    'urgent_actions': {
        'keywords': [
            'urgent', 'immediate', 'today', 'now', 'last', 'closing', 'expire',
            'within 24 hours', 'limited time', 'act now', 'verify immediately',
            'blocked', 'suspended', 'deactivated', 'final warning'
        ],
        'weight': 25,
        'description': 'Urgency pressure',
        'helpline': 'Help: 181'
    },
    'social_scam': {
        'keywords': [
            'facebook', 'instagram', 'whatsapp', 'telegram', 'friend', 'romance', 'love',
            'meet', 'gift', 'video call', 'explicit', 'blackmail', 'sextortion',
            'dating', 'relationship', 'send money', 'girlfriend', 'boyfriend'
        ],
        'weight': 30,
        'description': 'Social media scam',
        'helpline': 'Women Helpline: 1091'
    },
    'phishing': {
        'keywords': [
            'verify your account', 'confirm your identity', 'login to verify', 
            'click here to update', 'account compromised', 'unusual activity',
            'security alert', 'suspicious login', 'reset password', 'verify now'
        ],
        'weight': 30,
        'description': 'Phishing attempt',
        'helpline': 'Cyber Cell: 1930'
    }
}

# Code-mixed Hinglish patterns (Hindi+English)
HINGLISH_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'bank account band', 'kyc update karo', 'otp share', 'pin maang rahe',
            'atm card block', 'balance check', 'paise nikal liye', 'fraud transaction',
            'sbi alert', 'hdfc bank', 'icici bank', 'card se paise'
        ],
        'weight': 25,
        'description': 'Bank fraud in Hinglish',
        'helpline': 'Bank Helpline: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'inaam jeeto', 'lottery lagi', 'free gift', 'iphone jeeto', 'car jeeto',
            'lucky draw', 'selected ho gaye', 'claim karo', 'coupon code', 'discount milega',
            'prize claim', 'winner ban gaye'
        ],
        'weight': 35,
        'description': 'Prize fraud in Hinglish',
        'helpline': 'Cyber Cell: 1930'
    },
    'job_fraud': {
        'keywords': [
            'work from home', 'ghar baithe', 'part time job', 'daily payment', 'data entry',
            'youtube video like', 'task complete', 'joining bonus', 'registration fee',
            'training fee', 'commission milega', 'easy paise', 'no investment'
        ],
        'weight': 35,
        'description': 'Job fraud in Hinglish',
        'helpline': 'Cyber Cell: 1930'
    },
    'crypto_fraud': {
        'keywords': [
            'crypto investment', 'double money', 'guaranteed profit', 'cloud mining',
            'bitcoin double', 'withdrawal problem', 'tax pay karo', 'aml verify',
            'funds freeze', 'pay to withdraw', 'trading group', 'signal group',
            'telegram group join', 'whatsapp group join', 'mentor ne bataya'
        ],
        'weight': 35,
        'description': 'Crypto fraud in Hinglish',
        'helpline': 'Cyber Cell: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'digital arrest', 'police case', 'court notice', 'income tax raid', 'aadhaar block',
            'pan card suspend', 'cyber crime complaint', 'warrant issued', 'cbi investigation',
            'ed summon', 'judge sahab', 'case registered'
        ],
        'weight': 40,
        'description': 'Government impersonation in Hinglish',
        'helpline': 'Police: 100'
    },
    'urgent_actions': {
        'keywords': [
            'turant karo', 'abhi karo', 'aaj hi', 'kal last', 'band ho raha',
            'expire ho raha', 'jaldi karo', '24 hours', 'immediate action'
        ],
        'weight': 25,
        'description': 'Urgency in Hinglish',
        'helpline': 'Help: 181'
    }
}

# ============================================
# 2. FRAUD TYPE SPECIFIC PATTERNS
# ============================================

# SMS/Email patterns
SMS_PATTERNS = {
    'short_urls': [
        'bit.ly', 'tinyurl', 'goo.gl', 't.co', 'rb.gy', 'ow.ly', 'is.gd',
        'shorturl', 'shortlink', 'short.url', 'tiny.cc', 'cutt.ly', 'shorte.st'
    ],
    'free_keywords_english': ['free', 'win', 'won', 'claim', 'prize', 'lottery', 'congratulations'],
    'urgency_indicators': ['urgent', 'immediate', 'today', 'now', 'expire', 'last chance', 'within']
}

# Call patterns
CALL_PATTERNS = {
    'digital_arrest': {
        'hindi': ['गिरफ्तारी', 'पुलिस', 'केस', 'वारंट', 'सीबीआई', 'ईडी', 'जांच'],
        'marathi': ['अटक', 'पोलीस', 'केस', 'वॉरंट', 'सीबीआय', 'ईडी', 'तपास'],
        'tamil': ['கைது', 'போலீஸ்', 'வழக்கு', 'வாரண்ட்', 'சிபிஐ', 'ஈடி'],
        'telugu': ['అరెస్టు', 'పోలీస్', 'కేసు', 'వారెంట్', 'సీబీఐ', 'ఈడీ'],
        'kannada': ['ಬಂಧನ', 'ಪೋಲೀಸ್', 'ಕೇಸ್', 'ವಾರಂಟ್', 'ಸಿಬಿಐ', 'ಇಡಿ'],
        'malayalam': ['അറസ്റ്റ്', 'പോലീസ്', 'കേസ്', 'വാറന്റ്', 'സിബിഐ', 'ഇഡി'],
        'gujarati': ['અટક', 'પોલીસ', 'કેસ', 'વોરંટ', 'સીબીઆઈ', 'ઈડી'],
        'bengali': ['গ্রেপ্তার', 'পুলিশ', 'মামলা', 'ওয়ারেন্ট', 'সিবিআই', 'ইডি'],
        'punjabi': ['ਗ੍ਰਿਫਤਾਰੀ', 'ਪੁਲਿਸ', 'ਕੇਸ', 'ਵਾਰੰਟ', 'ਸੀਬੀਆਈ', 'ਈਡੀ'],
        'english': ['arrest', 'police', 'case', 'warrant', 'cbi', 'ed', 'investigation']
    },
    'kyc_expiry': {
        'hindi': ['केवाईसी', 'बैंक', 'खाता', 'बंद', 'अपडेट'],
        'marathi': ['केवाईसी', 'बँक', 'खाते', 'बंद', 'अपडेट'],
        'tamil': ['கேஒய்சி', 'வங்கி', 'கணக்கு', 'மூடல்', 'புதுப்பிப்பு'],
        'telugu': ['కేవైసీ', 'బ్యాంక్', 'ఖాతా', 'మూసివేత', 'అప్డేట్'],
        'kannada': ['ಕೆವೈಸಿ', 'ಬ್ಯಾಂಕ್', 'ಖಾತೆ', 'ಮುಚ್ಚುವಿಕೆ', 'ಅಪ್ಡೇಟ್'],
        'malayalam': ['കെവൈസി', 'ബാങ്ക്', 'അക്കൗണ്ട്', 'അടയ്ക്കൽ', 'അപ്ഡേറ്റ്'],
        'gujarati': ['કેવાયસી', 'બેંક', 'ખાતું', 'બંધ', 'અપડેટ'],
        'bengali': ['কেওয়াইসি', 'ব্যাঙ্ক', 'অ্যাকাউন্ট', 'বন্ধ', 'আপডেট'],
        'punjabi': ['ਕੇਵਾਈਸੀ', 'ਬੈਂਕ', 'ਖਾਤਾ', 'ਬੰਦ', 'ਅਪਡੇਟ'],
        'english': ['kyc', 'bank', 'account', 'close', 'update']
    },
    'fake_police': {
        'english': ['police officer', 'cyber cell', 'narcotics', 'money laundering', 'drug case'],
        'hindi': ['पुलिस अधिकारी', 'साइबर सेल', 'ड्रग्स', 'मनी लॉन्ड्रिंग']
    }
}

# Crypto-specific patterns
CRYPTO_PATTERNS = {
    'double_money': {
        'english': ['double', 'double money', 'double your money', '2x', '100% return'],
        'hindi': ['पैसे दोगुने', 'डबल मनी', 'दोगुना'],
        'marathi': ['पैसे दुप्पट', 'डबल'],
        'tamil': ['பணம் இரட்டிப்பு', 'டபுள்'],
        'telugu': ['డబ్బు రెట్టింపు', 'డబుల్']
    },
    'guaranteed_returns': {
        'english': ['guaranteed', 'assured', 'fixed returns', 'risk free', 'no loss'],
        'hindi': ['गारंटीड', 'पक्का मुनाफा', 'नो रिस्क'],
        'marathi': ['हमी', 'गॅरंटीड', 'नो रिस्क']
    },
    'fake_platform': {
        'english': [
            'cloud mining', 'arbitrage', 'trading bot', 'signal group', 'mining contract',
            'fake exchange', 'withdrawal fee', 'tax to unlock', 'aml verification',
            'pay to withdraw', 'bonus unlock', 'risk control', 'fees to release funds'
        ],
        'hindi': [
            'क्लाउड माइनिंग', 'आर्बिट्राज', 'सिग्नल ग्रुप', 'ट्रेडिंग बॉट',
            'विथड्रॉवल फीस', 'टैक्स भरो', 'एएमएल वेरिफिकेशन'
        ]
    },
    'pig_butchering': {
        'english': [
            'pig butchering', 'crypto romance scam', 'investment group', 'trading mentor',
            'whatsapp crypto', 'telegram crypto', 'tik tok crypto', 'dating site crypto'
        ]
    }
}

# Job fraud patterns
JOB_FRAUD_PATTERNS = {
    'task_scam': {
        'english': [
            'task scam', 'product listing', 'review task', 'like task', 'commission task',
            'daily tasks', 'earn per task', 'telegram job', 'whatsapp job'
        ]
    },
    'advance_fee': {
        'english': [
            'registration fee', 'training fee', 'security deposit', 'processing fee',
            'background check fee', 'equipment fee', 'joining fee'
        ]
    }
}

# Social media scam patterns
SOCIAL_MEDIA_PATTERNS = {
    'romance_scam': {
        'english': [
            'love', 'girlfriend', 'boyfriend', 'marriage', 'send money', 'gift card',
            'emergency money', 'sick relative', 'travel to meet'
        ]
    },
    'account_hijack': {
        'english': [
            'verify your account', 'account compromised', 'login link', 'reset password',
            'suspicious login', 'click to secure'
        ]
    },
    'giveaway_scam': {
        'english': [
            'giveaway', 'comment to win', 'share to win', 'free followers', 'free likes',
            'free bitcoin', 'free crypto'
        ]
    }
}

# Website scam patterns
WEBSITE_PATTERNS = {
    'suspicious_tlds': [
        '.xyz', '.top', '.club', '.online', '.site', '.work', '.date',
        '.loan', '.win', '.bid', '.trade', '.webcam', '.men', '.review',
        '.click', '.download', '.stream', '.gdn', '.mom', '.lol'
    ],
    'brand_impersonation': {
        'amazon': ['amazon', 'amzn', 'amazonpay'],
        'flipkart': ['flipkart', 'fk'],
        'google': ['google', 'gmail', 'youtube'],
        'paytm': ['paytm', 'paytm mall'],
        'sbi': ['sbi', 'state bank'],
        'hdfc': ['hdfc', 'hdfc bank'],
        'icici': ['icici', 'icici bank']
    },
    'ssl_missing': {
        'indicators': ['http://', 'no https', 'without ssl']
    }
}

# ============================================
# 3. TRUSTED SENDER PATTERNS
# ============================================

TRUSTED_SENDER_PATTERNS = {
    'banks': r'^(SBI|HDFC|ICICI|AXIS|YES|PNB|BOB|CANARA|UNION|IDBI|KOTAK|INDUSIND|SBIN|HDFCBANK|ICICIBANK)',
    'payment_apps': r'^(PAYTM|PHONPE|GOOGLE|AMAZON|FLIPKART|BHIM|UPI|GOOGLEPAY|AMAZONPAY)',
    'govt': r'^(GOV|GOVT|MODI|PMO|CMO|DIGITAL|CYBER|POLICE|NCPI|NPCI|GST|INCOMETAX)',
    'services': r'^(JIO|AIRTEL|VODA|IDEA|BSNL|TATASKY|HATHWAY|RELIANCE|VI|VODAFONE)'
}

# ============================================
# 4. SUSPICIOUS PATTERNS
# ============================================

SUSPICIOUS_PATTERNS = {
    'free_email_domains': [
        '@gmail.com', '@yahoo.com', '@hotmail.com', '@rediffmail.com',
        '@outlook.com', '@aol.com', '@protonmail.com', '@yandex.com',
        '@mail.com', '@inbox.com', '@gmx.com', '@icloud.com'
    ],
    'suspicious_tlds': WEBSITE_PATTERNS['suspicious_tlds'],
    'shortened_url_services': SMS_PATTERNS['short_urls']
}

# ============================================
# 5. RULE WEIGHTS
# ============================================

RULE_WEIGHTS = {
    'keyword_match': 10,
    'multiple_keywords': 15,
    'urgent_action': 25,
    'suspicious_link': 30,
    'unknown_sender': 20,
    'code_mixed_high_risk': 30,
    'native_script_scam': 25,
    'govt_impersonation': 40,
    'banking_threat': 30,
    'prize_claim': 35,
    'job_offer_scam': 35,
    'crypto_promise': 35,
    'phishing_attempt': 30,
    'pay_to_withdraw': 40,
    'fake_platform': 35,
    'task_scam': 35,
    'romance_scam': 35,
    'account_hijack': 30,
    'ssl_missing': 25,
    'brand_impersonation': 30
}

# ============================================
# 6. HELPLINE NUMBERS
# ============================================

HELPLINE_NUMBERS = {
    'national': {
        'cyber_crime': '1930',
        'women_helpline': '1091',
        'child_helpline': '1098',
        'police': '100',
        'ambulance': '102',
        'disaster': '108',
        'national_cyber': '155260'
    },
    'maharashtra': {
        'mumbai_cyber': '022-22620111',
        'pune_cyber': '020-26124220'
    },
    'tamil_nadu': {
        'chennai_cyber': '044-23456789'
    },
    'karnataka': {
        'bangalore_cyber': '080-23456789'
    },
    'telangana': {
        'hyderabad_cyber': '040-23456789'
    },
    'gujarat': {
        'ahmedabad_cyber': '079-23456789'
    },
    'west_bengal': {
        'kolkata_cyber': '033-23456789'
    },
    'punjab': {
        'chandigarh_cyber': '0172-2345678'
    },
    'delhi': {
        'delhi_cyber': '011-23456789'
    }
}

# ============================================
# 7. RESPONSE TEMPLATES (10 Languages)
# ============================================

RESPONSE_TEMPLATES = {
    'marathi': {
        'high_risk': '🚨 उच्च धोका! ही फसवणूक असण्याची शक्यता ९०% पेक्षा जास्त आहे. कृपया त्वरित खबरदारी घ्या.',
        'medium_risk': '⚡ मध्यम धोका. हा संदेश संशयास्पद आहे. तपासून घ्या.',
        'low_risk': '✅ कमी धोका. हा संदेश सुरक्षित वाटतो.',
        'action_steps': [
            '१. कोणतीही लिंक क्लिक करू नका',
            '२. ओटीपी शेअर करू नका',
            '३. त्वरित बँकेशी संपर्क साधा',
            '४. १९३० वर कॉल करून तक्रार नोंदवा'
        ]
    },
    'hindi': {
        'high_risk': '🚨 उच्च जोखिम! ९०% से अधिक संभावना है कि यह धोखाधड़ी है। कृपया तुरंत सावधानी बरतें।',
        'medium_risk': '⚡ मध्यम जोखिम। यह संदेश संदिग्ध है। जांच कर लें।',
        'low_risk': '✅ कम जोखिम। यह संदेश सुरक्षित लग रहा है।',
        'action_steps': [
            '१. किसी भी लिंक पर क्लिक न करें',
            '२. ओटीपी शेयर न करें',
            '३. तुरंत बैंक से संपर्क करें',
            '४. १९३० पर कॉल कर शिकायत दर्ज कराएं'
        ]
    },
    'tamil': {
        'high_risk': '🚨 அதிக ஆபத்து! 90% வாய்ப்பு இது மோசடி. உடனடியாக எச்சரிக்கையாக இருங்கள்.',
        'medium_risk': '⚡ நடுத்தர ஆபத்து. இந்த செய்தி சந்தேகத்திற்குரியது. சரிபார்க்கவும்.',
        'low_risk': '✅ குறைந்த ஆபத்து. இந்த செய்தி பாதுகாப்பானது.',
        'action_steps': [
            '1. எந்த இணைப்பையும் கிளிக் செய்ய வேண்டாம்',
            '2. OTP-ஐ யாருடனும் பகிர வேண்டாம்',
            '3. உடனே வங்கியை தொடர்பு கொள்ளுங்கள்',
            '4. 1930-க்கு அழைத்து புகார் செய்யுங்கள்'
        ]
    },
    'telugu': {
        'high_risk': '🚨 అధిక ప్రమాదం! 90% అవకాశం ఇది మోసం. వెంటనే జాగ్రత్తగా ఉండండి.',
        'medium_risk': '⚡ మధ్యస్థ ప్రమాదం. ఈ సందేశం అనుమానాస్పదంగా ఉంది. తనిఖీ చేయండి.',
        'low_risk': '✅ తక్కువ ప్రమాదం. ఈ సందేశం సురక్షితంగా ఉంది.',
        'action_steps': [
            '1. ఏ లింక్‌ని క్లిక్ చేయవద్దు',
            '2. OTP ఎవరితోనూ షేర్ చేయవద్దు',
            '3. వెంటనే బ్యాంక్‌ను సంప్రదించండి',
            '4. 1930కు కాల్ చేసి ఫిర్యాదు చేయండి'
        ]
    },
    'kannada': {
        'high_risk': '🚨 ಹೆಚ್ಚಿನ ಅಪಾಯ! 90%+ ಸಂಭವನೀಯತೆ ಇದು ವಂಚನೆ. ತಕ್ಷಣ ಎಚ್ಚರಿಕೆ ವಹಿಸಿ.',
        'medium_risk': '⚡ ಮಧ್ಯಮ ಅಪಾಯ. ಈ ಸಂದೇಶ ಅನುಮಾನಾಸ್ಪದವಾಗಿದೆ. ಪರಿಶೀಲಿಸಿ.',
        'low_risk': '✅ ಕಡಿಮೆ ಅಪಾಯ. ಈ ಸಂದೇಶ ಸುರಕ್ಷಿತವಾಗಿದೆ.',
        'action_steps': [
            '1. ಯಾವುದೇ ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ',
            '2. OTP ಯಾರೊಂದಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ',
            '3. ತಕ್ಷಣ ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಅನ್ನು ಸಂಪರ್ಕಿಸಿ',
            '4. 1930 ಗೆ ಕರೆ ಮಾಡಿ ದೂರು ದಾಖಲಿಸಿ'
        ]
    },
    'malayalam': {
        'high_risk': '🚨 ഉയർന്ന അപകടസാധ്യത! 90%+ സാധ്യത ഇത് തട്ടിപ്പാണ്. ഉടൻ ജാഗ്രത പാലിക്കുക.',
        'medium_risk': '⚡ ഇടത്തരം അപകടസാധ്യത. ഈ സന്ദേശം സംശയാസ്പദമാണ്. പരിശോധിക്കുക.',
        'low_risk': '✅ കുറഞ്ഞ അപകടസാധ്യത. ഈ സന്ദേശം സുരക്ഷിതമാണ്.',
        'action_steps': [
            '1. ഒരു ലിങ്കിലും ക്ലിക്ക് ചെയ്യരുത്',
            '2. OTP ആരുമായും പങ്കിടരുത്',
            '3. ഉടൻ നിങ്ങളുടെ ബാങ്കിനെ ബന്ധപ്പെടുക',
            '4. 1930 എന്ന നമ്പറിൽ വിളിച്ച് പരാതി നൽകുക'
        ]
    },
    'gujarati': {
        'high_risk': '🚨 ઉચ્ચ જોખમ! 90%+ સંભાવના છે કે આ છેતરપિંડી છે. કૃપા કરીને તાત્કાલિક સાવચેતી રાખો.',
        'medium_risk': '⚡ મધ્યમ જોખમ. આ સંદેશ શંકાસ્પદ છે. ચકાસી લો.',
        'low_risk': '✅ ઓછું જોખમ. આ સંદેશ સલામત લાગે છે.',
        'action_steps': [
            '૧. કોઈપણ લિંક પર ક્લિક કરશો નહીં',
            '૨. ઓટીપી શેર કરશો નહીં',
            '૩. તાત્કાલિક બેંકનો સંપર્ક કરો',
            '૪. ૧૯૩૦ પર કૉલ કરી ફરિયાદ નોંધાવો'
        ]
    },
    'bengali': {
        'high_risk': '🚨 উচ্চ ঝুঁকি! 90%+ সম্ভাবনা এটি জালিয়াতি। অনুগ্রহ করে অবিলম্বে সতর্কতা অবলম্বন করুন।',
        'medium_risk': '⚡ মাঝারি ঝুঁকি। এই বার্তাটি সন্দেহজনক। যাচাই করুন।',
        'low_risk': '✅ কম ঝুঁকি। এই বার্তাটি নিরাপদ বলে মনে হচ্ছে।',
        'action_steps': [
            '১. কোনো লিংকে ক্লিক করবেন না',
            '২. ওটিপি শেয়ার করবেন না',
            '৩. অবিলম্বে আপনার ব্যাঙ্কের সাথে যোগাযোগ করুন',
            '৪. ১৯৩০-এ কল করে অভিযোগ নিবন্ধন করুন'
        ]
    },
    'punjabi': {
        'high_risk': '🚨 ਉੱਚ ਜੋਖਮ! 90%+ ਸੰਭਾਵਨਾ ਹੈ ਕਿ ਇਹ ਧੋਖਾਧੜੀ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਤੁਰੰਤ ਸਾਵਧਾਨੀ ਵਰਤੋ।',
        'medium_risk': '⚡ ਦਰਮਿਆਨਾ ਜੋਖਮ। ਇਹ ਸੁਨੇਹਾ ਸ਼ੱਕੀ ਹੈ। ਜਾਂਚ ਕਰੋ।',
        'low_risk': '✅ ਘੱਟ ਜੋਖਮ। ਇਹ ਸੁਨੇਹਾ ਸੁਰੱਖਿਅਤ ਜਾਪਦਾ ਹੈ।',
        'action_steps': [
            '੧. ਕਿਸੇ ਵੀ ਲਿੰਕ ਤੇ ਕਲਿੱਕ ਨਾ ਕਰੋ',
            '੨. ਓਟੀਪੀ ਸਾਂਝੀ ਨਾ ਕਰੋ',
            '੩. ਤੁਰੰਤ ਆਪਣੇ ਬੈਂਕ ਨਾਲ ਸੰਪਰਕ ਕਰੋ',
            '੪. ੧੯੩੦ ਤੇ ਕਾਲ ਕਰਕੇ ਸ਼ਿਕਾਇਤ ਦਰਜ ਕਰਵਾਓ'
        ]
    },
    'english': {
        'high_risk': '🚨 HIGH RISK! 90%+ probability this is fraud. Take immediate action.',
        'medium_risk': '⚡ MEDIUM RISK. This message is suspicious. Verify before acting.',
        'low_risk': '✅ LOW RISK. This message appears safe.',
        'action_steps': [
            '1. DO NOT click any links',
            '2. DO NOT share OTP/PIN',
            '3. Contact your bank immediately',
            '4. Report to Cyber Cell: 1930'
        ]
    }
}

# ============================================
# 8. ADDITIONAL REQUIRED DICTIONARIES
# ============================================

LANGUAGE_WEIGHTS = {
    'detected': 1.2,
    'code_mixed': 1.5,
    'native_script': 1.3,
    'transliterated': 0.8
}

REGION_PATTERNS = {
    'maharashtra': {
        'cities': ['मुंबई', 'पुणे', 'नागपूर', 'नाशिक', 'औरंगाबाद', 'ठाणे', 'पिंपरी', 'कल्याण'],
        'state_code': 'MH',
        'language': 'marathi'
    },
    'tamil_nadu': {
        'cities': ['சென்னை', 'கோயம்புத்தூர்', 'மதுரை', 'திருச்சி', 'சேலம்', 'திருநெல்வேலி'],
        'state_code': 'TN',
        'language': 'tamil'
    },
    'karnataka': {
        'cities': ['ಬೆಂಗಳೂರು', 'ಮೈಸೂರು', 'ಹುಬ್ಬಳ್ಳಿ', 'ಮಂಗಳೂರು', 'ಬೆಳಗಾವಿ'],
        'state_code': 'KA',
        'language': 'kannada'
    },
    'telangana': {
        'cities': ['హైదరాబాద్', 'వరంగల్', 'నిజామాబాద్', 'ఖమ్మం'],
        'state_code': 'TS',
        'language': 'telugu'
    },
    'gujarat': {
        'cities': ['અમદાવાદ', 'સુરત', 'વડોદરા', 'રાજકોટ', 'ભાવનગર'],
        'state_code': 'GJ',
        'language': 'gujarati'
    },
    'west_bengal': {
        'cities': ['কলকাতা', 'হাওড়া', 'দুর্গাপুর', 'শিলিগুড়ি'],
        'state_code': 'WB',
        'language': 'bengali'
    },
    'punjab': {
        'cities': ['ਚੰਡੀਗੜ੍ਹ', 'ਲੁਧਿਆਣਾ', 'ਅੰਮ੍ਰਿਤਸਰ', 'ਜਲੰਧਰ'],
        'state_code': 'PB',
        'language': 'punjabi'
    },
    'delhi': {
        'cities': ['दिल्ली', 'नई दिल्ली', 'द्वारका', 'रोहिणी'],
        'state_code': 'DL',
        'language': 'hindi'
    }
}

INDIAN_CONTEXT = {
    'id_proofs': [
        'aadhaar', 'आधार', 'ஆதார்', 'ఆధార్', 'ಆಧಾರ್', 'ആധാർ', 'આધાર', 'আধার', 'ਆਧਾਰ',
        'pan', 'पैन', 'பான்', 'పాన్', 'ಪಾನ್', 'പാൻ', 'પાન', 'প্যান', 'ਪੈਨ',
        'voter', 'वोटर', 'வாக்காளர்', 'ఓటర్', 'ಮತದಾರ', 'വോട്ടർ', 'मतदार'
    ],
    'payment_methods': [
        'upi', 'भीम', 'பீம்', 'భీమ్', 'ಭೀಮ್', 'ഭീം', 'ભીમ', 'ভীম', 'ਭੀਮ',
        'paytm', 'phonepe', 'googlepay', 'amazonpay',
        'netbanking', 'डेबिट', 'क्रेडिट'
    ],
    'bank_names': [
        'sbi', 'hdfc', 'icici', 'axis', 'pnb', 'bob', 'canara',
        'एसबीआई', 'एचडीएफसी', 'आईसीआईसीआई'
    ]
}
