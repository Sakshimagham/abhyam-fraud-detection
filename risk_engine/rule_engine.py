# risk_engine/rule_engine.py
"""
Enhanced Rule Engine with Multilingual Support for ALL Indian Languages
Language-aware rules with regional context and code-mixed text handling
Includes detection for:
- SMS/Email (banking, prize, govt, job, crypto, urgency)
- Call (digital arrest, KYC, police impersonation)
- Crypto (double money, guaranteed returns, fake platforms, pig butchering, pay-to-withdraw)
- Fake Job (task scams, advance fee, work-from-home)
- Social Media (romance scams, giveaways, account hijack)
- Website (suspicious TLDs, brand impersonation, SSL)
"""

import re
from .rule_config import (
    MARATHI_PATTERNS, HINDI_PATTERNS, TAMIL_PATTERNS, TELUGU_PATTERNS,
    KANNADA_PATTERNS, MALAYALAM_PATTERNS, GUJARATI_PATTERNS, BENGALI_PATTERNS,
    PUNJABI_PATTERNS, ENGLISH_PATTERNS, HINGLISH_PATTERNS,
    TRUSTED_SENDER_PATTERNS, SUSPICIOUS_PATTERNS, LANGUAGE_WEIGHTS,
    RULE_WEIGHTS, HELPLINE_NUMBERS, RESPONSE_TEMPLATES, REGION_PATTERNS,
    SMS_PATTERNS, CALL_PATTERNS, CRYPTO_PATTERNS, JOB_FRAUD_PATTERNS,
    SOCIAL_MEDIA_PATTERNS, WEBSITE_PATTERNS, INDIAN_CONTEXT
)

class MultilingualRuleEngine:
    """
    Enhanced rule engine with support for multiple Indian languages
    and all major fraud types.
    """
    
    def __init__(self):
        self.all_language_patterns = {
            'marathi': MARATHI_PATTERNS,
            'hindi': HINDI_PATTERNS,
            'tamil': TAMIL_PATTERNS,
            'telugu': TELUGU_PATTERNS,
            'kannada': KANNADA_PATTERNS,
            'malayalam': MALAYALAM_PATTERNS,
            'gujarati': GUJARATI_PATTERNS,
            'bengali': BENGALI_PATTERNS,
            'punjabi': PUNJABI_PATTERNS,
            'english': ENGLISH_PATTERNS,
            'hinglish': HINGLISH_PATTERNS
        }
        
        # Language detection patterns (character/word based)
        self.language_indicators = {
            'english': ['the', 'is', 'are', 'was', 'were', 'has', 'have', 'been', 'will', 'would'],
            'marathi': ['आहे', 'होते', 'करा', 'मिळाले', 'तुमचे'],
            'hindi': ['है', 'का', 'की', 'के', 'में'],
            'tamil': ['உங்கள்', 'இது', 'அது', 'இங்கே'],
            'telugu': ['మీ', 'ఈ', 'ఆ', 'ఇక్కడ'],
            'kannada': ['ನಿಮ್ಮ', 'ಈ', 'ಆ', 'ಇಲ್ಲಿ'],
            'malayalam': ['നിങ്ങളുടെ', 'ഈ', 'ആ', 'ഇവിടെ'],
            'gujarati': ['તમારું', 'આ', 'તે', 'અહીં'],
            'bengali': ['আপনার', 'এই', 'সেই', 'এখানে'],
            'punjabi': ['ਤੁਹਾਡਾ', 'ਇਹ', 'ਉਹ', 'ਇੱਥੇ']
        }
        
        # Code-mixed indicators
        self.code_mixed_indicators = {
            'hinglish': ['hai', 'kya', 'ka', 'ki', 'ke', 'ko', 'se', 'mein'],
            'tenglish': ['cheppu', 'vachu', 'untadi', 'ledu'],  # Telugu + English
            'tangling': ['pannu', 'vachu', 'iruku', 'illai']     # Tamil + English
        }
    
    def detect_language_from_text(self, text):
        """
        Detect which language(s) are present in text
        Returns: primary_language, is_code_mixed, confidence
        """
        if not text:
            return 'unknown', False, 0
        
        text_lower = text.lower()
        scores = {}
        
        # Check for language indicators
        for lang, indicators in self.language_indicators.items():
            score = sum(1 for ind in indicators if ind in text)
            if score > 0:
                scores[lang] = score
        
        # Check for code-mixed patterns
        is_code_mixed = False
        code_mixed_langs = []
        
        for mixed_type, patterns in self.code_mixed_indicators.items():
            matches = sum(1 for pat in patterns if pat in text_lower)
            if matches > 2:  # Multiple patterns indicate code-mixing
                is_code_mixed = True
                code_mixed_langs.append(mixed_type)
        
        # Determine primary language
        if scores:
            primary = max(scores, key=scores.get)
            confidence = min(scores[primary] / 10, 0.95)  # Normalize
            return primary, is_code_mixed, confidence
        elif is_code_mixed:
            return code_mixed_langs[0] if code_mixed_langs else 'hinglish', True, 0.7
        else:
            return 'english', False, 0.5
    
    def get_language_patterns(self, language):
        """
        Get scam patterns for detected language
        """
        return self.all_language_patterns.get(language, ENGLISH_PATTERNS)
    
    def detect_region(self, text):
        """
        Detect region from text (city/state mentions)
        """
        detected_regions = []
        
        for region, data in REGION_PATTERNS.items():
            for city in data['cities']:
                if city in text:
                    detected_regions.append({
                        'region': region.replace('_', ' ').title(),
                        'city': city,
                        'language': data['language'],
                        'helpline': HELPLINE_NUMBERS.get(region, {}).get('police', '100')
                    })
                    break
        
        return detected_regions
    
    # ==========================================
    # URL & Link Analysis (Common)
    # ==========================================
    
    def analyze_urls(self, text):
        """
        Extract and analyze URLs in text. Returns (score, reasons)
        """
        urls = re.findall(r'https?://[^\s]+', text)
        score = 0
        reasons = []
        
        for url in urls:
            url_lower = url.lower()
            # Shortened URLs
            for short in SMS_PATTERNS['short_urls']:
                if short in url_lower:
                    score += RULE_WEIGHTS['suspicious_link']
                    reasons.append(f"Suspicious shortened URL: {short}")
                    break
            # Suspicious TLDs
            for tld in SUSPICIOUS_PATTERNS['suspicious_tlds']:
                if url_lower.endswith(tld):
                    score += RULE_WEIGHTS['suspicious_link']
                    reasons.append(f"Suspicious domain TLD: {tld}")
                    break
        return score, reasons, urls
    
    # ==========================================
    # SMS RULES (Multilingual)
    # ==========================================
    
    def sms_rules(self, text, sender_id=None, detected_lang=None):
        """
        Enhanced SMS rules with multilingual support
        """
        score = 0
        reasons = []
        helplines = []
        
        # Auto-detect language if not provided
        if not detected_lang:
            detected_lang, is_code_mixed, lang_conf = self.detect_language_from_text(text)
        else:
            is_code_mixed = False
        
        text_lower = text.lower()
        
        # Apply language-specific patterns
        lang_patterns = self.get_language_patterns(detected_lang)
        
        for fraud_type, pattern_data in lang_patterns.items():
            if not isinstance(pattern_data, dict):
                continue
            keywords = pattern_data.get('keywords', [])
            if not keywords:
                continue
            for keyword in keywords:
                if keyword in text:
                    score += pattern_data.get('weight', 20)
                    reasons.append({
                        'code': f'RULES-SMS-{detected_lang.upper()}-01',
                        'message': pattern_data.get('description', f'{fraud_type} detected'),
                        'language': detected_lang
                    })
                    if 'helpline' in pattern_data:
                        helplines.append(pattern_data['helpline'])
        
        # Check for short URLs (language independent)
        for url_service in SMS_PATTERNS['short_urls']:
            if url_service in text_lower:
                score += RULE_WEIGHTS['suspicious_link']
                reasons.append({
                    'code': 'RULES-SMS-COMMON-01',
                    'message': f'Suspicious shortened URL: {url_service}',
                    'language': 'common'
                })
                helplines.append(HELPLINE_NUMBERS['national']['cyber_crime'])
        
        # Check for urgency indicators across languages
        urgency_indicators = (
            SMS_PATTERNS['urgency_indicators'] +
            ['तातडीचे', 'लगेच', 'तुरंत', 'अभी', 'जल्दी', 'अवसर', 'அவசரம்', 'అత్యవసరం']
        )
        urgent_matches = 0
        for word in urgency_indicators:
            if word.lower() in text_lower:
                urgent_matches += 1
        if urgent_matches > 0:
            score += urgent_matches * RULE_WEIGHTS['urgent_action']
            reasons.append({
                'code': 'RULES-SMS-COMMON-02',
                'message': f'Urgency detected ({urgent_matches} indicators)',
                'language': 'common'
            })
        
        # Code-mixed text gets extra scrutiny
        if is_code_mixed:
            score += RULE_WEIGHTS['code_mixed_high_risk']
            reasons.append({
                'code': 'RULES-SMS-COMMON-03',
                'message': 'Code-mixed text detected - requires extra verification',
                'language': 'common'
            })
        
        # Sender ID rules
        if sender_id:
            trusted = False
            for pattern_name, pattern in TRUSTED_SENDER_PATTERNS.items():
                if re.match(pattern, sender_id):
                    trusted = True
                    break
            if not trusted:
                score += RULE_WEIGHTS['unknown_sender']
                reasons.append({
                    'code': 'RULES-SMS-COMMON-04',
                    'message': f'Unverified sender: {sender_id}',
                    'language': 'common'
                })
        
        # Check for Indian context indicators
        for id_type in INDIAN_CONTEXT['id_proofs']:
            if id_type in text:
                score += 15
                reasons.append({
                    'code': 'RULES-SMS-COMMON-05',
                    'message': f'ID proof mentioned: {id_type}',
                    'language': 'common'
                })
        
        # URL deep analysis
        url_score, url_reasons, _ = self.analyze_urls(text)
        score += url_score
        for r in url_reasons:
            reasons.append({
                'code': 'RULES-SMS-URL-01',
                'message': r,
                'language': 'common'
            })
        
        return score, reasons, list(set(helplines)), detected_lang, is_code_mixed
    
    # ==========================================
    # CALL RULES (Multilingual)
    # ==========================================
    
    def call_rules(self, transcript, caller_id=None, duration=None, detected_lang=None):
        """
        Enhanced call rules with multilingual support
        """
        score = 0
        reasons = []
        helplines = []
        
        if not detected_lang:
            detected_lang, is_code_mixed, _ = self.detect_language_from_text(transcript)
        
        # Check for scam scenarios
        for scenario, lang_patterns in CALL_PATTERNS.items():
            scenario_score = 0
            for lang, keywords in lang_patterns.items():
                for keyword in keywords:
                    if keyword in transcript:
                        scenario_score += 20
                        if scenario == 'digital_arrest':
                            reasons.append({
                                'code': 'RULES-CALL-SCENARIO-01',
                                'message': 'Digital arrest scam pattern detected',
                                'language': lang
                            })
                            helplines.append(HELPLINE_NUMBERS['national']['police'])
                        elif scenario == 'kyc_expiry':
                            reasons.append({
                                'code': 'RULES-CALL-SCENARIO-02',
                                'message': 'KYC expiry scam pattern detected',
                                'language': lang
                            })
                            helplines.append(HELPLINE_NUMBERS['national']['cyber_crime'])
            score += scenario_score
        
        # Call duration analysis
        if duration:
            if duration > 300:  # >5 minutes
                score += 15
                reasons.append({
                    'code': 'RULES-CALL-COMMON-01',
                    'message': 'Unusually long call duration',
                    'language': 'common'
                })
        
        # Caller ID analysis
        if caller_id:
            if caller_id == 'unknown' or caller_id == 'private':
                score += 20
                reasons.append({
                    'code': 'RULES-CALL-COMMON-02',
                    'message': 'Caller ID hidden or unknown',
                    'language': 'common'
                })
            elif re.match(r'^\+[^91]', caller_id):  # International number not starting with +91
                score += 15
                reasons.append({
                    'code': 'RULES-CALL-COMMON-03',
                    'message': 'International caller ID',
                    'language': 'common'
                })
        
        return score, reasons, list(set(helplines))
    
    # ==========================================
    # CRYPTO RULES (Multilingual)
    # ==========================================
    
    def crypto_rules(self, text, url=None, detected_lang=None):
        """
        Enhanced crypto fraud rules with multilingual support
        """
        score = 0
        reasons = []
        helplines = []
        
        if not detected_lang:
            detected_lang, is_code_mixed, _ = self.detect_language_from_text(text)
        
        text_lower = text.lower()
        
        # Check for double money promises
        for lang, keywords in CRYPTO_PATTERNS['double_money'].items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    score += RULE_WEIGHTS['crypto_promise']
                    reasons.append({
                        'code': 'RULES-CRYPTO-01',
                        'message': f'Double money promise detected ({lang})',
                        'language': lang
                    })
                    helplines.append(HELPLINE_NUMBERS['national']['cyber_crime'])
        
        # Check for guaranteed returns
        for lang, keywords in CRYPTO_PATTERNS['guaranteed_returns'].items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    score += 25
                    reasons.append({
                        'code': 'RULES-CRYPTO-02',
                        'message': f'Guaranteed returns claim ({lang})',
                        'language': lang
                    })
        
        # Fake platform indicators (pay-to-withdraw)
        for keyword in CRYPTO_PATTERNS['fake_platform']['english']:
            if keyword.lower() in text_lower:
                score += RULE_WEIGHTS['pay_to_withdraw']
                reasons.append({
                    'code': 'RULES-CRYPTO-03',
                    'message': f'Fake platform indicator: {keyword}',
                    'language': 'common'
                })
                helplines.append(HELPLINE_NUMBERS['national']['cyber_crime'])
        
        # Pig butchering indicators
        for keyword in CRYPTO_PATTERNS['pig_butchering']['english']:
            if keyword.lower() in text_lower:
                score += RULE_WEIGHTS['crypto_promise']
                reasons.append({
                    'code': 'RULES-CRYPTO-04',
                    'message': f'Pig butchering scam pattern: {keyword}',
                    'language': 'common'
                })
        
        # URL analysis
        if url:
            url_score, url_reasons, _ = self.analyze_urls(url)
            score += url_score
            for r in url_reasons:
                reasons.append({
                    'code': 'RULES-CRYPTO-URL',
                    'message': r,
                    'language': 'common'
                })
        
        return score, reasons, list(set(helplines))
    
    # ==========================================
    # JOB RULES (Multilingual)
    # ==========================================
    
    def job_rules(self, job_data, detected_lang=None):
        """
        Enhanced fake job rules with multilingual support
        """
        score = 0
        reasons = []
        helplines = []
        
        title = job_data.get('title', '')
        description = job_data.get('description', '')
        company = job_data.get('company', '')
        email = job_data.get('email', '')
        
        full_text = f"{title} {description}".lower()
        
        if not detected_lang:
            detected_lang, is_code_mixed, _ = self.detect_language_from_text(full_text)
        
        # Get language-specific job patterns
        lang_patterns = self.get_language_patterns(detected_lang)
        if 'job_fraud' in lang_patterns:
            for keyword in lang_patterns['job_fraud']['keywords']:
                if keyword.lower() in full_text:
                    score += 25
                    reasons.append({
                        'code': 'RULES-JOB-01',
                        'message': f'Job scam keyword: {keyword}',
                        'language': detected_lang
                    })
        
        # Task scam patterns
        for keyword in JOB_FRAUD_PATTERNS['task_scam']['english']:
            if keyword.lower() in full_text:
                score += RULE_WEIGHTS['task_scam']
                reasons.append({
                    'code': 'RULES-JOB-02',
                    'message': f'Task scam pattern: {keyword}',
                    'language': 'common'
                })
                helplines.append(HELPLINE_NUMBERS['national']['cyber_crime'])
        
        # Advance fee patterns
        for keyword in JOB_FRAUD_PATTERNS['advance_fee']['english']:
            if keyword.lower() in full_text:
                score += RULE_WEIGHTS['job_offer_scam']
                reasons.append({
                    'code': 'RULES-JOB-03',
                    'message': f'Advance fee request: {keyword}',
                    'language': 'common'
                })
                helplines.append(HELPLINE_NUMBERS['national']['cyber_crime'])
        
        # Check for free email domains
        if email:
            for domain in SUSPICIOUS_PATTERNS['free_email_domains']:
                if domain in email:
                    score += 15
                    reasons.append({
                        'code': 'RULES-JOB-04',
                        'message': f'Free email domain used: {domain}',
                        'language': 'common'
                    })
        
        # Check for missing company name
        if not company or len(company) < 3:
            score += 20
            reasons.append({
                'code': 'RULES-JOB-05',
                'message': 'Company name missing or too short',
                'language': 'common'
            })
        
        return score, reasons, list(set(helplines))
    
    # ==========================================
    # SOCIAL MEDIA RULES (Multilingual)
    # ==========================================
    
    def social_media_rules(self, profile_data, detected_lang=None):
        """
        Enhanced social media fraud rules with multilingual support
        """
        score = 0
        reasons = []
        helplines = []
        
        bio = profile_data.get('bio', '')
        followers = profile_data.get('followers', 0)
        following = profile_data.get('following', 0)
        posts = profile_data.get('posts', 0)
        account_age = profile_data.get('account_age', 0)
        
        if not detected_lang and bio:
            detected_lang, is_code_mixed, _ = self.detect_language_from_text(bio)
        
        # Romance scam patterns
        for keyword in SOCIAL_MEDIA_PATTERNS['romance_scam']['english']:
            if keyword in bio.lower():
                score += RULE_WEIGHTS['romance_scam']
                reasons.append({
                    'code': 'RULES-SOCIAL-01',
                    'message': f'Romance scam indicator: {keyword}',
                    'language': 'common'
                })
                helplines.append(HELPLINE_NUMBERS['national']['women_helpline'])
        
        # Giveaway scam patterns
        for keyword in SOCIAL_MEDIA_PATTERNS['giveaway_scam']['english']:
            if keyword in bio.lower():
                score += 25
                reasons.append({
                    'code': 'RULES-SOCIAL-02',
                    'message': f'Giveaway scam pattern: {keyword}',
                    'language': 'common'
                })
        
        # Account hijack patterns
        for keyword in SOCIAL_MEDIA_PATTERNS['account_hijack']['english']:
            if keyword in bio.lower():
                score += RULE_WEIGHTS['account_hijack']
                reasons.append({
                    'code': 'RULES-SOCIAL-03',
                    'message': f'Account hijack indicator: {keyword}',
                    'language': 'common'
                })
        
        # Follower/Following ratio analysis
        if following > 0:
            ratio = followers / following
            if ratio < 0.1 and followers > 100:
                score += 25
                reasons.append({
                    'code': 'RULES-SOCIAL-04',
                    'message': 'Suspicious follower/following ratio',
                    'language': 'common'
                })
        
        # New account with high activity
        if account_age < 7 and posts > 50:
            score += 20
            reasons.append({
                'code': 'RULES-SOCIAL-05',
                'message': 'New account with unusually high post count',
                'language': 'common'
            })
        
        # Bio with suspicious links
        if bio and any(short in bio for short in SMS_PATTERNS['short_urls']):
            score += 25
            reasons.append({
                'code': 'RULES-SOCIAL-06',
                'message': 'Suspicious link in bio',
                'language': 'common'
            })
            helplines.append(HELPLINE_NUMBERS['national']['cyber_crime'])
        
        return score, reasons, list(set(helplines))
    
    # ==========================================
    # WEBSITE RULES (Multilingual)
    # ==========================================
    
    def website_rules(self, url, content=None, trust_data=None, detected_lang=None):
        """
        Enhanced website fraud rules with multilingual support
        """
        score = 0
        reasons = []
        helplines = []
        
        url_lower = url.lower()
        
        if content and not detected_lang:
            detected_lang, is_code_mixed, _ = self.detect_language_from_text(content)
        
        # Check for suspicious TLDs
        for tld in SUSPICIOUS_PATTERNS['suspicious_tlds']:
            if url_lower.endswith(tld):
                score += 30
                reasons.append({
                    'code': 'RULES-WEB-01',
                    'message': f'Suspicious domain extension: {tld}',
                    'language': 'common'
                })
                helplines.append(HELPLINE_NUMBERS['national']['cyber_crime'])
        
        # Check for brand impersonation
        for brand, patterns in WEBSITE_PATTERNS['brand_impersonation'].items():
            for pattern in patterns:
                if pattern in url_lower and not any(trusted in url_lower for trusted in ['.gov.in', '.org.in', '.ac.in']):
                    score += RULE_WEIGHTS['brand_impersonation']
                    reasons.append({
                        'code': 'RULES-WEB-02',
                        'message': f'Possible brand impersonation: {brand}',
                        'language': 'common'
                    })
        
        # Trust data analysis
        if trust_data:
            if trust_data.get('domain_age', 1000) < 30:  # New domain
                score += 25
                reasons.append({
                    'code': 'RULES-WEB-03',
                    'message': 'Domain registered recently (<30 days)',
                    'language': 'common'
                })
            if not trust_data.get('has_ssl', 0):
                score += 20
                reasons.append({
                    'code': 'RULES-WEB-04',
                    'message': 'No SSL certificate (not HTTPS)',
                    'language': 'common'
                })
            if not trust_data.get('has_contact', 0):
                score += 15
                reasons.append({
                    'code': 'RULES-WEB-05',
                    'message': 'No contact information found',
                    'language': 'common'
                })
        
        return score, reasons, list(set(helplines))
    
    # ==========================================
    # MAIN RULE ENGINE (Combined)
    # ==========================================
    
    def calculate_risk(self, module_type, input_data, detected_lang=None):
        """
        Central rule engine for all fraud types
        """
        rule_score = 0
        all_reasons = []
        all_helplines = []
        
        if module_type == 'sms':
            text = input_data.get('text', '') if isinstance(input_data, dict) else input_data
            sender = input_data.get('sender_id', None) if isinstance(input_data, dict) else None
            rule_score, reasons, helplines, lang, code_mixed = self.sms_rules(
                text, sender, detected_lang
            )
            all_reasons.extend(reasons)
            all_helplines.extend(helplines)
            
        elif module_type == 'call':
            transcript = input_data.get('transcript', '') if isinstance(input_data, dict) else input_data
            caller_id = input_data.get('caller_id', None) if isinstance(input_data, dict) else None
            duration = input_data.get('duration', None) if isinstance(input_data, dict) else None
            rule_score, reasons, helplines = self.call_rules(
                transcript, caller_id, duration, detected_lang
            )
            all_reasons.extend(reasons)
            all_helplines.extend(helplines)
            
        elif module_type == 'crypto':
            text = input_data.get('text', '') if isinstance(input_data, dict) else input_data
            url = input_data.get('url', None) if isinstance(input_data, dict) else None
            rule_score, reasons, helplines = self.crypto_rules(
                text, url, detected_lang
            )
            all_reasons.extend(reasons)
            all_helplines.extend(helplines)
            
        elif module_type == 'job':
            rule_score, reasons, helplines = self.job_rules(
                input_data if isinstance(input_data, dict) else {'description': input_data}, 
                detected_lang
            )
            all_reasons.extend(reasons)
            all_helplines.extend(helplines)
            
        elif module_type == 'social':
            rule_score, reasons, helplines = self.social_media_rules(
                input_data if isinstance(input_data, dict) else {'bio': input_data}, 
                detected_lang
            )
            all_reasons.extend(reasons)
            all_helplines.extend(helplines)
            
        elif module_type == 'website':
            url = input_data.get('url', '') if isinstance(input_data, dict) else input_data
            content = input_data.get('content', None) if isinstance(input_data, dict) else None
            trust_data = input_data.get('trust_data', None) if isinstance(input_data, dict) else None
            rule_score, reasons, helplines = self.website_rules(
                url, content, trust_data, detected_lang
            )
            all_reasons.extend(reasons)
            all_helplines.extend(helplines)
        
        return rule_score, all_reasons, list(set(all_helplines))
    
    # ==========================================
    # RISK COMBINATION AND RESPONSE GENERATION
    # ==========================================
    
    def combine_risk(self, ml_probability, rule_score, detected_lang='english', is_code_mixed=False):
        """
        Combine ML score and rule score with language awareness
        """
        # Convert ML probability to score (0-100)
        ml_score = ml_probability * 100
        
        # Apply language weights
        lang_weight = LANGUAGE_WEIGHTS.get('detected', 1.0)
        if is_code_mixed:
            lang_weight = LANGUAGE_WEIGHTS.get('code_mixed', 1.5)
        
        # Calculate final score
        final_score = (ml_score * 0.6 + rule_score * 0.4) * lang_weight
        
        # Cap at 100
        final_score = min(final_score, 100)
        
        # Determine risk level
        if final_score >= 80:
            level = 'HIGH'
            action = 'BLOCK_AND_ALERT'
        elif final_score >= 50:
            level = 'MEDIUM'
            action = 'REVIEW'
        elif final_score >= 25:
            level = 'LOW'
            action = 'MONITOR'
        else:
            level = 'MINIMAL'
            action = 'ALLOW'
        
        # Get language-specific response
        templates = RESPONSE_TEMPLATES.get(detected_lang, RESPONSE_TEMPLATES['english'])
        
        if level == 'HIGH':
            user_message = templates['high_risk']
            action_steps = templates.get('action_steps', [
                'Do not share any personal information',
                'Do not click any links',
                'Contact the official helpline',
                'Report to cyber crime: 1930'
            ])
        elif level == 'MEDIUM':
            user_message = templates['medium_risk']
            action_steps = ['Verify before proceeding', 'Check with official sources']
        else:
            user_message = templates['low_risk']
            action_steps = ['No immediate action needed']
        
        return {
            'final_score': round(final_score, 1),
            'risk_level': level,
            'action': action,
            'user_message': user_message,
            'action_steps': action_steps,
            'language_used': detected_lang,
            'code_mixed': is_code_mixed
        }
    
    def generate_response(self, result_dict, reasons, helplines):
        """
        Generate complete response with all information
        """
        response = {
            'risk_assessment': result_dict,
            'reasons': reasons,
            'helplines': helplines,
            'timestamp': '2024-01-01 12:00:00'  # Add actual timestamp
        }
        
        # Add helpline suggestions
        if result_dict['risk_level'] in ['HIGH', 'MEDIUM']:
            response['recommended_actions'] = [
                'Do not share any personal information',
                'Do not click any links',
                'Contact the official helpline',
                'Report to cyber crime: 1930'
            ]
        
        return response


# ==========================================
# Test the rule engine
# ==========================================
if __name__ == "__main__":
    engine = MultilingualRuleEngine()
    
    # Test cases for all fraud types
    test_cases = [
        {
            'type': 'sms',
            'data': {
                'text': '🎬 CONGRATULATIONS! You have won ₹5,00,000 + iPhone 16! Click here to claim: https://short.link/xyz123',
                'sender_id': 'WINNER'
            }
        },
        {
            'type': 'call',
            'data': {
                'transcript': 'मी पोलीस अधिकारी बोलतोय. तुमच्यावर केस आहे. पैसे भरा नाहीतर अटक',
                'caller_id': '+1234567890',
                'duration': 360
            }
        },
        {
            'type': 'crypto',
            'data': {
                'text': 'Double your Bitcoin in 24 hours! Guaranteed returns! Pay only 0.01 BTC to unlock withdrawal.',
                'url': 'https://crypto-scam.xyz'
            }
        },
        {
            'type': 'job',
            'data': {
                'title': 'Work from home data entry',
                'description': 'Earn ₹15,000/day by liking YouTube videos. Join Telegram group. Registration fee ₹500.',
                'company': '',
                'email': 'job@scam.com'
            }
        },
        {
            'type': 'social',
            'data': {
                'bio': 'Looking for love! Send me gift cards and I will visit you. DM for more.',
                'followers': 50,
                'following': 5000,
                'posts': 10,
                'account_age': 2
            }
        },
        {
            'type': 'website',
            'data': {
                'url': 'https://sbi-update.xyz',
                'content': 'Update your KYC immediately or your account will be blocked.',
                'trust_data': {'domain_age': 5, 'has_ssl': False, 'has_contact': False}
            }
        }
    ]
    
    print("=" * 100)
    print("MULTILINGUAL RULE ENGINE TEST - ALL FRAUD TYPES")
    print("=" * 100)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📌 TEST CASE {i}: {test['type'].upper()}")
        print("-" * 80)
        
        # Detect language
        if 'text' in test['data']:
            text = test['data']['text']
        elif 'transcript' in test['data']:
            text = test['data']['transcript']
        elif 'bio' in test['data']:
            text = test['data']['bio']
        else:
            text = test['data'].get('url', '')
        
        detected_lang, is_code_mixed, conf = engine.detect_language_from_text(text)
        print(f"📝 Text: {text[:100]}...")
        print(f"🌐 Detected Language: {detected_lang} (confidence: {conf:.2f})")
        print(f"🔄 Code-mixed: {is_code_mixed}")
        
        # Apply rules
        rule_score, reasons, helplines = engine.calculate_risk(
            test['type'], test['data'], detected_lang
        )
        
        print(f"\n⚖️ Rule Score: {rule_score}")
        print(f"📋 Reasons ({len(reasons)}):")
        for r in reasons[:5]:  # Show first 5 reasons
            if isinstance(r, dict):
                print(f"  • {r.get('message', str(r))}")
            else:
                print(f"  • {r}")
        
        if helplines:
            print(f"📞 Helplines: {', '.join(helplines[:3])}")
        
        # Combine with a dummy ML probability (0.5) – just for demo
        result = engine.combine_risk(0.5, rule_score, detected_lang, is_code_mixed)
        print(f"\n🎯 Final Risk Assessment:")
        print(f"  Score: {result['final_score']}%")
        print(f"  Level: {result['risk_level']}")
        print(f"  Message: {result['user_message']}")
        print(f"  Action: {result['action']}")
        
        print("=" * 100)
