# risk_engine/rule_config.py
"""
Enhanced Rule Configuration with Multilingual Support for ALL Indian Languages
Contains patterns, keywords, and weights for all fraud types in 9+ Indian languages
"""

# ============================================
# 1. LANGUAGE-SPECIFIC SCAM PATTERNS
# ============================================

# Marathi (मराठी) Patterns
MARATHI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'बँक', 'खाते', 'एटीएम', 'पिन', 'ओटीपी', 'केवाईसी', 'बंद', 'अपडेट',
            'डेबिट', 'क्रेडिट', 'कार्ड', 'बॅलन्स', 'रक्कम', 'व्याज', 'कर्ज'
        ],
        'weight': 25,
        'description': 'बँक संबंधित फसवणूक',
        'helpline': 'बँक हेल्पलाइन: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'बक्षीस', 'लॉटरी', 'जिंकलात', 'पैसे', 'रक्कम', 'कूपन', 'ऑफर',
            'स्कीम', 'योजना', 'भेट', 'फ्री', 'मोफत', 'डिस्काउंट', 'सूट'
        ],
        'weight': 30,
        'description': 'बक्षीस/लॉटरी फसवणूक',
        'helpline': 'सायबर सेल: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'सरकार', 'पोलीस', 'कोर्ट', 'नोटीस', 'दंड', 'आधार', 'पॅन',
            'जीएसटी', 'आयकर', 'व्होटर', 'राशन', 'डिजिटल अटक'
        ],
        'weight': 35,
        'description': 'सरकारी अधिकारी बनून फसवणूक',
        'helpline': 'पोलीस हेल्पलाइन: 100'
    },
    'job_fraud': {
        'keywords': [
            'नोकरी', 'जॉब', 'फी', 'पैसे भरा', 'रजिस्ट्रेशन', 'ट्रेनिंग',
            'घरबसल्या', 'पार्ट टाइम', 'डेटा एंट्री', 'कमिशन'
        ],
        'weight': 30,
        'description': 'बनावट नोकरी ऑफर',
        'helpline': 'श्रम मंत्रालय: 1800-XXX-XXXX'
    },
    'urgent_actions': {
        'keywords': [
            'तातडीचे', 'लगेच', 'आज', 'उद्या', 'शेवटची', 'बंद होणार',
            'एक्सपायर', 'थांबा', 'ताबडतोब', 'आत्ताच'
        ],
        'weight': 20,
        'description': 'तातडीची कारवाईचा दबाव',
        'helpline': 'मदत हेल्पलाइन: 181'
    }
}

# Hindi (हिंदी) Patterns
HINDI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'बैंक', 'खाता', 'एटीएम', 'पिन', 'ओटीपी', 'केवाईसी', 'बंद', 'अपडेट',
            'डेबिट', 'क्रेडिट', 'कार्ड', 'बैलेंस', 'रकम', 'ब्याज', 'कर्ज'
        ],
        'weight': 25,
        'description': 'बैंक संबंधित धोखाधड़ी',
        'helpline': 'बैंक हेल्पलाइन: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'इनाम', 'लॉटरी', 'जीत', 'पैसे', 'रकम', 'कूपन', 'ऑफर',
            'स्कीम', 'योजना', 'गिफ्ट', 'फ्री', 'मुफ्त', 'डिस्काउंट', 'छूट'
        ],
        'weight': 30,
        'description': 'इनाम/लॉटरी धोखाधड़ी',
        'helpline': 'साइबर सेल: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'सरकार', 'पुलिस', 'कोर्ट', 'नोटिस', 'जुर्माना', 'आधार', 'पैन',
            'जीएसटी', 'इनकम टैक्स', 'वोटर', 'राशन', 'डिजिटल अरेस्ट'
        ],
        'weight': 35,
        'description': 'सरकारी अधिकारी बनकर धोखाधड़ी',
        'helpline': 'पुलिस हेल्पलाइन: 100'
    },
    'urgent_actions': {
        'keywords': [
            'तुरंत', 'अभी', 'आज', 'कल', 'आखिरी', 'बंद हो रहा',
            'एक्सपायर', 'जल्दी', 'तत्काल'
        ],
        'weight': 20,
        'description': 'तत्काल कार्रवाई का दबाव',
        'helpline': 'मदद हेल्पलाइन: 181'
    }
}

# Tamil (தமிழ்) Patterns
TAMIL_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'வங்கி', 'கணக்கு', 'ஏடிஎம்', 'பின்', 'ஓடிபி', 'கேஒய்சி', 'மூடல்', 'புதுப்பிப்பு',
            'டெபிட்', 'கிரெடிட்', 'கார்டு', 'இருப்பு', 'தொகை', 'வட்டி', 'கடன்'
        ],
        'weight': 25,
        'description': 'வங்கி மோசடி',
        'helpline': 'வங்கி உதவி எண்: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'பரிசு', 'லாட்டரி', 'வெற்றி', 'பணம்', 'தொகை', 'கூப்பன்', 'சலுகை',
            'திட்டம்', 'இலவசம்', 'தள்ளுபடி'
        ],
        'weight': 30,
        'description': 'பரிசு/லாட்டரி மோசடி',
        'helpline': 'சைபர் செல்: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'அரசு', 'போலீஸ்', 'நீதிமன்றம்', 'நோட்டீஸ்', 'அபராதம்', 'ஆதார்', 'பான்',
            'ஜிஎஸ்டி', 'வருமான வரி', 'வாக்காளர்', 'ரேஷன்'
        ],
        'weight': 35,
        'description': 'அரசு அதிகாரி போல் மோசடி',
        'helpline': 'போலீஸ் உதவி: 100'
    },
    'urgent_actions': {
        'keywords': [
            'அவசரம்', 'இப்போது', 'இன்று', 'நாளை', 'கடைசி', 'மூடப்படும்',
            'காலாவதி', 'உடனடி'
        ],
        'weight': 20,
        'description': 'அவசர நடவடிக்கை அழுத்தம்',
        'helpline': 'உதவி எண்: 181'
    }
}

# Telugu (తెలుగు) Patterns
TELUGU_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'బ్యాంక్', 'ఖాతా', 'ఏటీఎం', 'పిన్', 'ఓటిపి', 'కేవైసీ', 'మూసివేత', 'అప్డేట్',
            'డెబిట్', 'క్రెడిట్', 'కార్డు', 'బ్యాలెన్స్', 'మొత్తం', 'వడ్డీ', 'రుణం'
        ],
        'weight': 25,
        'description': 'బ్యాంక్ మోసం',
        'helpline': 'బ్యాంక్ హెల్ప్‌లైన్: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'బహుమతి', 'లాటరీ', 'గెలుపు', 'డబ్బు', 'మొత్తం', 'కూపన్', 'ఆఫర్',
            'పథకం', 'ఉచితం', 'తగ్గింపు'
        ],
        'weight': 30,
        'description': 'బహుమతి/లాటరీ మోసం',
        'helpline': 'సైబర్ సెల్: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'ప్రభుత్వం', 'పోలీస్', 'కోర్ట్', 'నోటీసు', 'జరిమానా', 'ఆధార్', 'పాన్'
        ],
        'weight': 35,
        'description': 'ప్రభుత్వ అధికారిగా మోసం',
        'helpline': 'పోలీస్ హెల్ప్‌లైన్: 100'
    },
    'urgent_actions': {
        'keywords': [
            'అత్యవసరం', 'ఇప్పుడే', 'ఈరోజు', 'రేపు', 'చివరి', 'మూసివేత',
            'గడువు', 'వెంటనే'
        ],
        'weight': 20,
        'description': 'అత్యవసర చర్య ఒత్తిడి',
        'helpline': 'సహాయం: 181'
    }
}

# Kannada (ಕನ್ನಡ) Patterns
KANNADA_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'ಬ್ಯಾಂಕ್', 'ಖಾತೆ', 'ಎಟಿಎಂ', 'ಪಿನ್', 'ಒಟಿಪಿ', 'ಕೆವೈಸಿ', 'ಮುಚ್ಚುವಿಕೆ', 'ಅಪ್ಡೇಟ್',
            'ಡೆಬಿಟ್', 'ಕ್ರೆಡಿಟ್', 'ಕಾರ್ಡ್', 'ಬ್ಯಾಲೆನ್ಸ್', 'ಮೊತ್ತ', 'ಬಡ್ಡಿ', 'ಸಾಲ'
        ],
        'weight': 25,
        'description': 'ಬ್ಯಾಂಕ್ ವಂಚನೆ',
        'helpline': 'ಬ್ಯಾಂಕ್ ಹೆಲ್ಪ್‌ಲೈನ್: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'ಬಹುಮಾನ', 'ಲಾಟರಿ', 'ಗೆಲುವು', 'ಹಣ', 'ಮೊತ್ತ', 'ಕೂಪನ್', 'ಆಫರ್'
        ],
        'weight': 30,
        'description': 'ಬಹುಮಾನ/ಲಾಟರಿ ವಂಚನೆ',
        'helpline': 'ಸೈಬರ್ ಸೆಲ್: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'ಸರ್ಕಾರ', 'ಪೋಲೀಸ್', 'ಕೋರ್ಟ್', 'ಸೂಚನೆ', 'ದಂಡ', 'ಆಧಾರ್', 'ಪಾನ್'
        ],
        'weight': 35,
        'description': 'ಸರ್ಕಾರಿ ಅಧಿಕಾರಿಯಂತೆ ವಂಚನೆ',
        'helpline': 'ಪೋಲೀಸ್ ಸಹಾಯ: 100'
    },
    'urgent_actions': {
        'keywords': [
            'ತುರ್ತು', 'ಈಗ', 'ಇಂದು', 'ನಾಳೆ', 'ಕೊನೆಯ', 'ಮುಚ್ಚುವಿಕೆ',
            'ಮುಕ್ತಾಯ', 'ತಕ್ಷಣ'
        ],
        'weight': 20,
        'description': 'ತುರ್ತು ಕ್ರಮ ಒತ್ತಡ',
        'helpline': 'ಸಹಾಯ: 181'
    }
}

# Malayalam (മലയാളം) Patterns
MALAYALAM_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'ബാങ്ക്', 'അക്കൗണ്ട്', 'എടിഎം', 'പിൻ', 'ഒടിപി', 'കെവൈസി', 'അടയ്ക്കൽ', 'അപ്ഡേറ്റ്',
            'ഡെബിറ്റ്', 'ക്രെഡിറ്റ്', 'കാർഡ്', 'ബാലൻസ്', 'തുക', 'പലിശ', 'വായ്പ'
        ],
        'weight': 25,
        'description': 'ബാങ്ക് തട്ടിപ്പ്',
        'helpline': 'ബാങ്ക് ഹെൽപ്പ്‌ലൈൻ: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'സമ്മാനം', 'ലോട്ടറി', 'വിജയം', 'പണം', 'തുക', 'കൂപ്പൺ', 'ഓഫർ'
        ],
        'weight': 30,
        'description': 'സമ്മാനം/ലോട്ടറി തട്ടിപ്പ്',
        'helpline': 'സൈബർ സെൽ: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'സർക്കാർ', 'പോലീസ്', 'കോടതി', 'അറിയിപ്പ്', 'പിഴ', 'ആധാർ', 'പാൻ'
        ],
        'weight': 35,
        'description': 'സർക്കാർ ഉദ്യോഗസ്ഥനെന്ന വ്യാജേന തട്ടിപ്പ്',
        'helpline': 'പോലീസ് സഹായം: 100'
    },
    'urgent_actions': {
        'keywords': [
            'അടിയന്തര', 'ഇപ്പോൾ', 'ഇന്ന്', 'നാളെ', 'അവസാന', 'അടയ്ക്കൽ',
            'കാലഹരണപ്പെടൽ', 'ഉടൻ'
        ],
        'weight': 20,
        'description': 'അടിയന്തര നടപടി സമ്മർദ്ദം',
        'helpline': 'സഹായം: 181'
    }
}

# Gujarati (ગુજરાતી) Patterns
GUJARATI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'બેંક', 'ખાતું', 'એટીએમ', 'પિન', 'ઓટીપી', 'કેવાયસી', 'બંધ', 'અપડેટ',
            'ડેબિટ', 'ક્રેડિટ', 'કાર્ડ', 'બેલેન્સ', 'રકમ', 'વ્યાજ', 'લોન'
        ],
        'weight': 25,
        'description': 'બેંક છેતરપિંડી',
        'helpline': 'બેંક હેલ્પલાઇન: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'ઇનામ', 'લોટરી', 'જીત', 'પૈસા', 'રકમ', 'કૂપન', 'ઓફર'
        ],
        'weight': 30,
        'description': 'ઇનામ/લોટરી છેતરપિંડી',
        'helpline': 'સાયબર સેલ: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'સરકાર', 'પોલીસ', 'કોર્ટ', 'નોટિસ', 'દંડ', 'આધાર', 'પાન'
        ],
        'weight': 35,
        'description': 'સરકારી અધિકારી બની છેતરપિંડી',
        'helpline': 'પોલીસ હેલ્પલાઇન: 100'
    },
    'urgent_actions': {
        'keywords': [
            'તાત્કાલિક', 'હમણાં', 'આજે', 'કાલે', 'છેલ્લી', 'બંધ',
            'સમાપ્તિ', 'તરત'
        ],
        'weight': 20,
        'description': 'તાત્કાલિક કાર્યવાહી દબાણ',
        'helpline': 'મદદ: 181'
    }
}

# Bengali (বাংলা) Patterns
BENGALI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'ব্যাঙ্ক', 'অ্যাকাউন্ট', 'এটিএম', 'পিন', 'ওটিপি', 'কেওয়াইসি', 'বন্ধ', 'আপডেট',
            'ডেবিট', 'ক্রেডিট', 'কার্ড', 'ব্যালেন্স', 'টাকা', 'সুদ', 'ঋণ'
        ],
        'weight': 25,
        'description': 'ব্যাঙ্ক জালিয়াতি',
        'helpline': 'ব্যাঙ্ক হেল্পলাইন: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'পুরস্কার', 'লটারি', 'জয়', 'টাকা', 'পরিমাণ', 'কুপন', 'অফার'
        ],
        'weight': 30,
        'description': 'পুরস্কার/লটারি জালিয়াতি',
        'helpline': 'সাইবার সেল: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'সরকার', 'পুলিশ', 'কোর্ট', 'নোটিশ', 'জরিমানা', 'আধার', 'প্যান'
        ],
        'weight': 35,
        'description': 'সরকারি কর্মকর্তা সেজে জালিয়াতি',
        'helpline': 'পুলিশ হেল্পলাইন: 100'
    },
    'urgent_actions': {
        'keywords': [
            'জরুরি', 'এখনই', 'আজ', 'কাল', 'শেষ', 'বন্ধ',
            'মেয়াদোত্তীর্ণ', 'অবিলম্বে'
        ],
        'weight': 20,
        'description': 'জরুরি পদক্ষেপ চাপ',
        'helpline': 'সাহায্য: 181'
    }
}

# Punjabi (ਪੰਜਾਬੀ) Patterns
PUNJABI_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'ਬੈਂਕ', 'ਖਾਤਾ', 'ਏਟੀਐਮ', 'ਪਿੰਨ', 'ਓਟੀਪੀ', 'ਕੇਵਾਈਸੀ', 'ਬੰਦ', 'ਅਪਡੇਟ',
            'ਡੈਬਿਟ', 'ਕ੍ਰੈਡਿਟ', 'ਕਾਰਡ', 'ਬੈਲੰਸ', 'ਰਕਮ', 'ਵਿਆਜ', 'ਕਰਜ਼'
        ],
        'weight': 25,
        'description': 'ਬੈਂਕ ਧੋਖਾਧੜੀ',
        'helpline': 'ਬੈਂਕ ਹੈਲਪਲਾਈਨ: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'ਇਨਾਮ', 'ਲਾਟਰੀ', 'ਜਿੱਤ', 'ਪੈਸੇ', 'ਰਕਮ', 'ਕੂਪਨ', 'ਆਫਰ'
        ],
        'weight': 30,
        'description': 'ਇਨਾਮ/ਲਾਟਰੀ ਧੋਖਾਧੜੀ',
        'helpline': 'ਸਾਈਬਰ ਸੈੱਲ: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'ਸਰਕਾਰ', 'ਪੁਲਿਸ', 'ਕੋਰਟ', 'ਨੋਟਿਸ', 'ਜੁਰਮਾਨਾ', 'ਆਧਾਰ', 'ਪੈਨ'
        ],
        'weight': 35,
        'description': 'ਸਰਕਾਰੀ ਅਧਿਕਾਰੀ ਬਣ ਕੇ ਧੋਖਾਧੜੀ',
        'helpline': 'ਪੁਲਿਸ ਹੈਲਪਲਾਈਨ: 100'
    },
    'urgent_actions': {
        'keywords': [
            'ਜ਼ਰੂਰੀ', 'ਹੁਣੇ', 'ਅੱਜ', 'ਕੱਲ੍ਹ', 'ਆਖਰੀ', 'ਬੰਦ',
            'ਮਿਆਦ ਪੁੱਗਣ', 'ਤੁਰੰਤ'
        ],
        'weight': 20,
        'description': 'ਜ਼ਰੂਰੀ ਕਾਰਵਾਈ ਦਬਾਅ',
        'helpline': 'ਮਦਦ: 181'
    }
}

# Odia (ଓଡ଼ିଆ) Patterns
ODIA_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'ବ୍ୟାଙ୍କ', 'ଖାତା', 'ଏଟିଏମ୍', 'ପିନ୍', 'ଓଟିପି', 'କେୱାଇସି', 'ବନ୍ଦ', 'ଅପଡେଟ୍',
            'ଡେବିଟ୍', 'କ୍ରେଡିଟ୍', 'କାର୍ଡ', 'ବ୍ୟାଲାନ୍ସ', 'ଟଙ୍କା', 'ସୁଧ', 'ଋଣ'
        ],
        'weight': 25,
        'description': 'ବ୍ୟାଙ୍କ ଠକେଇ',
        'helpline': 'ବ୍ୟାଙ୍କ ହେଲ୍ପଲାଇନ୍: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'ପୁରସ୍କାର', 'ଲଟେରୀ', 'ଜିତ', 'ଟଙ୍କା', 'ରାଶି', 'କୁପନ୍', 'ଅଫର୍'
        ],
        'weight': 30,
        'description': 'ପୁରସ୍କାର/ଲଟେରୀ ଠକେଇ',
        'helpline': 'ସାଇବର ସେଲ୍: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'ସରକାର', 'ପୋଲିସ୍', 'କୋର୍ଟ', 'ନୋଟିସ୍', 'ଜୋରିମାନା', 'ଆଧାର', 'ପ୍ୟାନ୍'
        ],
        'weight': 35,
        'description': 'ସରକାରୀ ଅଧିକାରୀ ଭାବେ ଠକେଇ',
        'helpline': 'ପୋଲିସ୍ ସହାୟତା: 100'
    },
    'urgent_actions': {
        'keywords': [
            'ଜରୁରୀ', 'ଏବେ', 'ଆଜି', 'କାଲି', 'ଶେଷ', 'ବନ୍ଦ',
            'ସମାପ୍ତ', 'ତୁରନ୍ତ'
        ],
        'weight': 20,
        'description': 'ଜରୁରୀ କାର୍ଯ୍ୟାନୁଷ୍ଠାନ ଚାପ',
        'helpline': 'ସହାୟତା: 181'
    }
}

# Hinglish (हिंग्लिश) Patterns
HINGLISH_PATTERNS = {
    'banking_fraud': {
        'keywords': [
            'bank', 'account', 'atm', 'pin', 'otp', 'kyc', 'band', 'update',
            'debit', 'credit', 'card', 'balance', 'paise', 'byaaj', 'karz'
        ],
        'weight': 25,
        'description': 'Bank fraud in Hinglish',
        'helpline': 'Bank Helpline: 1800-XXX-XXXX'
    },
    'prize_fraud': {
        'keywords': [
            'inaam', 'lottery', 'jeet', 'paise', 'coupon', 'offer', 'free',
            'muft', 'discount', 'gift', 'scheme', 'yojana'
        ],
        'weight': 30,
        'description': 'Prize/Lottery fraud in Hinglish',
        'helpline': 'Cyber Cell: 1930'
    },
    'govt_fraud': {
        'keywords': [
            'sarkar', 'police', 'court', 'notice', 'jurmana', 'aadhaar', 'pan'
        ],
        'weight': 35,
        'description': 'Government official impersonation in Hinglish',
        'helpline': 'Police: 100'
    },
    'urgent_actions': {
        'keywords': [
            'urgent', 'immediate', 'today', 'kal', 'aaj', 'last', 'close',
            'expire', 'jaldi', 'turant'
        ],
        'weight': 20,
        'description': 'Urgency pressure in Hinglish',
        'helpline': 'Help: 181'
    }
}

# ============================================
# 2. FRAUD TYPE SPECIFIC PATTERNS
# ============================================

# SMS-specific patterns across languages
SMS_PATTERNS = {
    'short_urls': [
        'bit.ly', 'tinyurl', 'goo.gl', 't.co', 'rb.gy', 'ow.ly', 'is.gd',
        'shorturl', 'shortlink'
    ],
    'free_keywords_english': ['free', 'win', 'won', 'claim', 'prize', 'lottery'],
    'urgency_indicators': ['urgent', 'immediate', 'today', 'now', 'expire']
}

# Call-specific patterns
CALL_PATTERNS = {
    'digital_arrest': {
        'hindi': ['गिरफ्तारी', 'पुलिस', 'केस', 'वारंट'],
        'marathi': ['अटक', 'पोलीस', 'केस', 'वॉरंट'],
        'tamil': ['கைது', 'போலீஸ்', 'வழக்கு', 'வாரண்ட்'],
        'telugu': ['అరెస్టు', 'పోలీస్', 'కేసు', 'వారెంట్'],
        'kannada': ['ಬಂಧನ', 'ಪೋಲೀಸ್', 'ಕೇಸ್', 'ವಾರಂಟ್'],
        'english': ['arrest', 'police', 'case', 'warrant']
    },
    'kyc_expiry': {
        'hindi': ['केवाईसी', 'बैंक', 'खाता', 'बंद'],
        'marathi': ['केवाईसी', 'बँक', 'खाते', 'बंद'],
        'tamil': ['கேஒய்சி', 'வங்கி', 'கணக்கு', 'மூடல்'],
        'telugu': ['కేవైసీ', 'బ్యాంక్', 'ఖాతా', 'మూసివేత'],
        'english': ['kyc', 'bank', 'account', 'close']
    }
}

# Crypto-specific patterns
CRYPTO_PATTERNS = {
    'double_money': {
        'english': ['double', 'double money', 'double your money'],
        'hindi': ['पैसे दोगुने', 'डबल मनी'],
        'marathi': ['पैसे दुप्पट'],
        'tamil': ['பணம் இரட்டிப்பு'],
        'telugu': ['డబ్బు రెట్టింపు']
    },
    'guaranteed_returns': {
        'english': ['guaranteed', 'assured', 'fixed returns'],
        'hindi': ['गारंटीड', 'पक्का मुनाफा'],
        'marathi': ['हमी', 'गॅरंटीड'],
        'tamil': ['உத்தரவாதம்', 'நிச்சயமான வருமானம்']
    }
}

# ============================================
# 3. TRUSTED SENDER PATTERNS
# ============================================

TRUSTED_SENDER_PATTERNS = {
    'banks': r'^(SBI|HDFC|ICICI|AXIS|YES|PNB|BOB|CANARA|UNION|IDBI|KOTAK|INDUSIND)',
    'payment_apps': r'^(PAYTM|PHONPE|GOOGLE|AMAZON|FLIPKART|BHIM|UPI)',
    'govt': r'^(GOV|MODI|PMO|CMO|DIGITAL|CYBER|POLICE)',
    'services': r'^(JIO|AIRTEL|VODA|IDEA|BSNL|TATASKY|HATHWAY)'
}

# ============================================
# 4. SUSPICIOUS PATTERNS
# ============================================

SUSPICIOUS_PATTERNS = {
    'free_email_domains': [
        '@gmail.com', '@yahoo.com', '@hotmail.com', '@rediffmail.com',
        '@outlook.com', '@aol.com', '@protonmail.com', '@yandex.com',
        '@mail.com', '@inbox.com', '@gmx.com'
    ],
    'suspicious_tlds': [
        '.xyz', '.top', '.club', '.online', '.site', '.work', '.date',
        '.loan', '.win', '.bid', '.trade', '.webcam', '.men', '.review'
    ],
    'shortened_url_services': [
        'bit.ly', 'tinyurl', 'goo.gl', 't.co', 'rb.gy', 'ow.ly', 'is.gd',
        'buff.ly', 'short.link', 'shorturl.at'
    ]
}

# ============================================
# 5. LANGUAGE WEIGHTS AND PRIORITIES
# ============================================

LANGUAGE_WEIGHTS = {
    'detected': 1.2,      # If language explicitly detected in text
    'code_mixed': 1.5,    # Code-mixed texts need higher scrutiny
    'native_script': 1.3,  # Native script detection
    'transliterated': 0.8  # Roman script for Indian languages
}

# ============================================
# 6. INDIAN CONTEXT PATTERNS
# ============================================

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

# ============================================
# 7. SCORE WEIGHTS FOR RULE ENGINE
# ============================================

RULE_WEIGHTS = {
    'keyword_match': 10,
    'multiple_keywords': 15,
    'urgent_action': 20,
    'suspicious_link': 25,
    'unknown_sender': 15,
    'code_mixed_high_risk': 30,
    'native_script_scam': 25,
    'govt_impersonation': 35,
    'banking_threat': 30,
    'prize_claim': 25,
    'job_offer_scam': 25,
    'crypto_promise': 30
}

# ============================================
# 8. HELPLINE NUMBERS (State-wise)
# ============================================

HELPLINE_NUMBERS = {
    'national': {
        'cyber_crime': '1930',
        'women_helpline': '1091',
        'child_helpline': '1098',
        'police': '100',
        'ambulance': '102',
        'disaster': '108'
    },
    'maharashtra': {
        'mumbai_cyber': '022-22620111',
        'pune_cyber': '020-26124220',
        'nagpur_cyber': '0712-2562111',
        'thane_cyber': '022-25341234',
        'women_helpline': '1091',
        'police': '100'
    },
    'tamil_nadu': {
        'chennai_cyber': '044-23456789',
        'coimbatore_cyber': '0422-1234567',
        'madurai_cyber': '0452-2345678',
        'women_helpline': '1091'
    },
    'karnataka': {
        'bangalore_cyber': '080-23456789',
        'mysore_cyber': '0821-1234567',
        'women_helpline': '1091'
    },
    'telangana': {
        'hyderabad_cyber': '040-23456789',
        'warangal_cyber': '0870-1234567'
    },
    'gujarat': {
        'ahmedabad_cyber': '079-23456789',
        'surat_cyber': '0261-1234567'
    },
    'west_bengal': {
        'kolkata_cyber': '033-23456789',
        'howrah_cyber': '033-1234567'
    },
    'punjab': {
        'chandigarh_cyber': '0172-2345678',
        'ludhiana_cyber': '0161-1234567'
    },
    'delhi': {
        'delhi_cyber': '011-23456789',
        'women_helpline': '1091'
    },
    'uttar_pradesh': {
        'lucknow_cyber': '0522-2345678',
        'kanpur_cyber': '0512-2345678'
    },
    'bihar': {
        'patna_cyber': '0612-2345678',
        'police': '100'
    },
    'odisha': {
        'bhubaneswar_cyber': '0674-2345678',
        'cuttack_cyber': '0671-2345678'
    }
}

# ============================================
# 9. REGION DETECTION PATTERNS
# ============================================

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
    'andhra_pradesh': {
        'cities': ['విశాఖపట్నం', 'విజయవాడ', 'గుంటూరు', 'తిరుపతి'],
        'state_code': 'AP',
        'language': 'telugu'
    },
    'kerala': {
        'cities': ['തിരുവനന്തപുരം', 'കൊച്ചി', 'കോഴിക്കോട്', 'തൃശ്ശൂർ'],
        'state_code': 'KL',
        'language': 'malayalam'
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
    'haryana': {
        'cities': ['गुरुग्राम', 'फरीदाबाद', 'पानीपत', 'अंबाला'],
        'state_code': 'HR',
        'language': 'hindi'
    },
    'delhi': {
        'cities': ['दिल्ली', 'नई दिल्ली', 'द्वारका', 'रोहिणी'],
        'state_code': 'DL',
        'language': 'hindi'
    },
    'uttar_pradesh': {
        'cities': ['लखनऊ', 'कानपुर', 'वाराणसी', 'आगरा', 'प्रयागराज'],
        'state_code': 'UP',
        'language': 'hindi'
    },
    'bihar': {
        'cities': ['पटना', 'गया', 'भागलपुर', 'मुजफ्फरपुर'],
        'state_code': 'BR',
        'language': 'hindi'
    },
    'odisha': {
        'cities': ['ଭୁବନେଶ୍ୱର', 'କଟକ', 'ରାଉରକେଲା', 'ବ୍ରହ୍ମପୁର'],
        'state_code': 'OD',
        'language': 'odia'
    },
    'jharkhand': {
        'cities': ['रांची', 'जमशेदपुर', 'धनबाद'],
        'state_code': 'JH',
        'language': 'hindi'
    },
    'chhattisgarh': {
        'cities': ['रायपुर', 'बिलासपुर', 'दुर्ग'],
        'state_code': 'CG',
        'language': 'hindi'
    },
    'madhya_pradesh': {
        'cities': ['भोपाल', 'इंदौर', 'ग्वालियर', 'जबलपुर'],
        'state_code': 'MP',
        'language': 'hindi'
    },
    'rajasthan': {
        'cities': ['जयपुर', 'जोधपुर', 'उदयपुर', 'कोटा'],
        'state_code': 'RJ',
        'language': 'hindi'
    },
    'assam': {
        'cities': ['গুৱাহাটী', 'দিছপুৰ', 'যোৰহাট'],
        'state_code': 'AS',
        'language': 'assamese'
    }
}

# ============================================
# 10. MULTILINGUAL RESPONSE TEMPLATES
# ============================================

RESPONSE_TEMPLATES = {
    'marathi': {
        'high_risk': '🚨 उच्च धोका! ही फसवणूक असण्याची शक्यता ९०% पेक्षा जास्त आहे. कृपया त्वरित खबरदारी घ्या.',
        'medium_risk': '⚡ मध्यम धोका. हा संदेश संशयास्पद आहे. तपासून घ्या.',
        'low_risk': '✅ कमी धोका. हा संदेश सुरक्षित वाटतो.',
        'banking_alert': 'बँक कधीही ओटीपी, पिन किंवा पासवर्ड विचारत नाही. कोणाशीही शेअर करू नका.',
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