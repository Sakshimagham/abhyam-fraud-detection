# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)   # fraud_ai_system

ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
FEEDBACK_DIR = os.path.join(PROJECT_ROOT, 'data', 'feedback')