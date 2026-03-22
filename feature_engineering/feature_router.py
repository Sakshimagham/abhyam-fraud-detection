# feature_engineering/feature_router.py
"""
Unified Feature Router with Multilingual Support
Routes requests to appropriate feature extractors with language awareness
"""

import os
import numpy as np
import joblib
import re
from typing import Dict, Any, Tuple, Optional, Union

# Import language detector
from .language_detector import IndianLanguageDetector

# Import all feature extractors (with error handling)
try:
    from .sms_features import MultilingualSMSFeatureExtractor
except ImportError:
    MultilingualSMSFeatureExtractor = None
    print("⚠️ SMS feature extractor not available")

try:
    from .call_features import MultilingualCallFeatureExtractor
except ImportError:
    MultilingualCallFeatureExtractor = None
    print("⚠️ Call feature extractor not available")

try:
    from .crypto_features import MultilingualCryptoFeatureExtractor
except ImportError:
    MultilingualCryptoFeatureExtractor = None
    print("⚠️ Crypto feature extractor not available")

try:
    from .fake_jobs_features import MultilingualFakeJobsFeatureExtractor
except ImportError:
    MultilingualFakeJobsFeatureExtractor = None
    print("⚠️ Jobs feature extractor not available")

try:
    from .social_media_features import MultilingualSocialMediaFeatureExtractor
except ImportError:
    MultilingualSocialMediaFeatureExtractor = None
    print("⚠️ Social media feature extractor not available")

try:
    from .web_features import MultilingualWebsiteFeatureExtractor
except ImportError:
    MultilingualWebsiteFeatureExtractor = None
    print("⚠️ Website feature extractor not available")

from .multilingual_utils import MultilingualFeatureExtractor

class MultilingualFeatureRouter:
    """
    Unified router for multilingual feature extraction across all fraud types
    """
    
    def __init__(self):
        """Initialize all feature extractors and utilities"""
        print("🚀 Initializing Multilingual Feature Router...")
        
        # Initialize language detector
        self.language_detector = IndianLanguageDetector()
        
        # Initialize multilingual utilities
        self.multilingual_utils = MultilingualFeatureExtractor()
        
        # Initialize feature extractors (lazy loading - only when needed)
        self._extractors = {}
        
        # Path to saved models and vectorizers
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.feature_path = os.path.join(self.base_path, "feature_engineering")
        
        print("✅ Feature Router initialized")
    
    def _get_extractor(self, module_type: str):
        """
        Lazy load feature extractor for specific module
        """
        if module_type not in self._extractors:
            if module_type == 'sms' and MultilingualSMSFeatureExtractor:
                self._extractors['sms'] = MultilingualSMSFeatureExtractor()
            elif module_type == 'call' and MultilingualCallFeatureExtractor:
                self._extractors['call'] = MultilingualCallFeatureExtractor()
            elif module_type == 'crypto' and MultilingualCryptoFeatureExtractor:
                self._extractors['crypto'] = MultilingualCryptoFeatureExtractor()
            elif module_type == 'job' and MultilingualFakeJobsFeatureExtractor:
                self._extractors['job'] = MultilingualFakeJobsFeatureExtractor()
            elif module_type == 'social' and MultilingualSocialMediaFeatureExtractor:
                self._extractors['social'] = MultilingualSocialMediaFeatureExtractor()
            elif module_type == 'website' and MultilingualWebsiteFeatureExtractor:
                self._extractors['website'] = MultilingualWebsiteFeatureExtractor()
            else:
                # Return a dummy extractor that returns empty features
                return DummyExtractor(module_type)
        
        return self._extractors.get(module_type, DummyExtractor(module_type))
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language of input text
        Returns language code, confidence, and script details
        """
        if not text:
            return {
                'language': 'unknown',
                'confidence': 0,
                'is_code_mixed': False,
                'scripts': {}
            }
        
        try:
            result = self.language_detector.detect_language(text)
            
            # Handle different return types
            if isinstance(result, tuple) and len(result) >= 2:
                lang = result[0]
                conf = result[1]
                scripts = result[2] if len(result) > 2 else {}
                
                # Check if code-mixed
                is_code_mixed = False
                if isinstance(scripts, dict):
                    is_code_mixed = scripts.get('code_mixed', False)
                
                return {
                    'language': lang,
                    'confidence': conf,
                    'is_code_mixed': is_code_mixed,
                    'scripts': scripts
                }
            elif isinstance(result, dict):
                return result
            else:
                return {
                    'language': 'unknown',
                    'confidence': 0,
                    'is_code_mixed': False,
                    'scripts': {}
                }
        except Exception as e:
            print(f"Language detection error: {e}")
            return {
                'language': 'unknown',
                'confidence': 0,
                'is_code_mixed': False,
                'scripts': {}
            }
    
    def extract_features(self, module_type: str, input_data: Union[str, Dict], 
                        detect_language: bool = True) -> Dict[str, Any]:
        """
        Unified feature extraction function
        
        Args:
            module_type: Type of fraud (sms, call, crypto, job, social, website)
            input_data: Input data (string or dictionary based on module)
            detect_language: Whether to auto-detect language
        
        Returns:
            Dictionary containing features and metadata
        """
        # Initialize features dictionary
        features = {}
        
        # Detect language if requested
        lang_info = {'language': 'unknown', 'confidence': 0, 'is_code_mixed': False}
        
        if detect_language:
            # Extract text for language detection
            text_to_analyze = ""
            if isinstance(input_data, str):
                text_to_analyze = input_data
            elif isinstance(input_data, dict):
                # Try common text fields
                for field in ['text', 'transcript', 'description', 'content', 
                             'message', 'title', 'bio']:
                    if field in input_data and input_data[field]:
                        text_to_analyze = input_data[field]
                        break
            
            if text_to_analyze:
                lang_info = self.detect_language(text_to_analyze)
        
        # Get appropriate extractor
        extractor = self._get_extractor(module_type)
        
        # Extract features based on module type
        try:
            if hasattr(extractor, 'extract_all_features'):
                if module_type == 'sms':
                    if isinstance(input_data, str):
                        features = extractor.extract_all_features(input_data)
                    else:
                        text = input_data.get('text', '')
                        features = extractor.extract_all_features(text)
                
                elif module_type == 'call':
                    if isinstance(input_data, str):
                        features = extractor.extract_all_features(input_data)
                    else:
                        transcript = input_data.get('transcript', '')
                        duration = input_data.get('duration', None)
                        caller_id = input_data.get('caller_id', None)
                        features = extractor.extract_all_features(transcript, duration, caller_id)
                
                elif module_type == 'crypto':
                    if isinstance(input_data, str):
                        features = extractor.extract_all_features(text=input_data)
                    else:
                        url = input_data.get('url', None)
                        text = input_data.get('text', '')
                        transaction_data = input_data.get('transaction_data', None)
                        features = extractor.extract_all_features(url, text, transaction_data)
                
                elif module_type == 'job':
                    if isinstance(input_data, str):
                        features = extractor.extract_all_features({'description': input_data})
                    else:
                        features = extractor.extract_all_features(input_data)
                
                elif module_type == 'social':
                    if isinstance(input_data, str):
                        features = extractor.extract_all_features({'bio': input_data})
                    else:
                        profile_data = input_data.get('profile', input_data)
                        posts = input_data.get('posts', None)
                        features = extractor.extract_all_features(profile_data, posts)
                
                elif module_type == 'website':
                    if isinstance(input_data, str):
                        features = extractor.extract_all_features(url=input_data)
                    else:
                        url = input_data.get('url', '')
                        content = input_data.get('content', None)
                        title = input_data.get('title', None)
                        meta = input_data.get('meta_description', None)
                        trust_data = input_data.get('trust_data', None)
                        features = extractor.extract_all_features(url, content, title, meta, trust_data)
            else:
                # Dummy extractor or extractor without extract_all_features
                features = {
                    'text_length': len(str(input_data)),
                    'has_digits': any(c.isdigit() for c in str(input_data))
                }
        except Exception as e:
            print(f"⚠️ Error extracting features for {module_type}: {e}")
            features = {'error': str(e), 'text_preview': str(input_data)[:100]}
        
        # Add language info to features
        features['detected_language'] = lang_info['language']
        features['language_confidence'] = lang_info['confidence']
        features['is_code_mixed'] = lang_info['is_code_mixed']
        
        return features
    
    def get_feature_vector(self, module_type: str, input_data: Union[str, Dict],
                          model_type: str = 'ml') -> np.ndarray:
        """
        Get feature vector ready for model input
        """
        features = self.extract_features(module_type, input_data)
        
        # Convert features to vector
        vector = []
        
        # Add numerical features
        for key, value in features.items():
            if isinstance(value, (int, float)) and not key.startswith('_'):
                vector.append(value)
        
        # Ensure we have at least some features
        if not vector:
            vector = [0] * 10  # Return zeros if no features
        
        return np.array(vector)
    
    def get_supported_languages(self) -> list:
        """
        Return list of supported language codes
        """
        return [
            'english', 'hindi', 'marathi', 'tamil', 'telugu', 'kannada',
            'malayalam', 'gujarati', 'bengali', 'punjabi', 'odia',
            'hinglish', 'tenglish', 'tangling'
        ]


class DummyExtractor:
    """Dummy extractor for when real extractor is not available"""
    
    def __init__(self, module_type):
        self.module_type = module_type
    
    def extract_all_features(self, *args, **kwargs):
        return {
            'module': self.module_type,
            'text_length': 0,
            'has_digits': 0,
            'dummy': True
        }


# Create singleton instance
_feature_router_instance = None

def get_feature_router():
    """
    Get singleton instance of feature router
    """
    global _feature_router_instance
    if _feature_router_instance is None:
        _feature_router_instance = MultilingualFeatureRouter()
    return _feature_router_instance


# ============================================
# CONVENIENCE FUNCTIONS
# ============================================

def extract_features(module_type: str, input_data: Union[str, Dict], 
                    detect_language: bool = True) -> Dict:
    """
    Convenience function to extract features
    """
    router = get_feature_router()
    return router.extract_features(module_type, input_data, detect_language)


def detect_language(text: str) -> Dict:
    """
    Convenience function to detect language
    """
    router = get_feature_router()
    return router.detect_language(text)


def get_feature_vector(module_type: str, input_data: Union[str, Dict],
                      model_type: str = 'ml') -> np.ndarray:
    """
    Convenience function to get feature vector
    """
    router = get_feature_router()
    return router.get_feature_vector(module_type, input_data, model_type)