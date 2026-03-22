# components/feedback_db.py
import pandas as pd
import os
from datetime import datetime

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'feedback', 'feedback.csv')

def save_feedback(input_text, ml_prob, rule_score, final_risk, user_correct, comment, proof_link):
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
    df_new = pd.DataFrame([{
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'input_text': input_text,
        'ml_prob': ml_prob,
        'rule_score': rule_score,
        'final_risk': final_risk,
        'user_correct': user_correct,
        'comment': comment,
        'proof_link': proof_link
    }])
    if os.path.exists(FEEDBACK_FILE):
        existing = pd.read_csv(FEEDBACK_FILE)
        df_new = pd.concat([existing, df_new], ignore_index=True)
    df_new.to_csv(FEEDBACK_FILE, index=False)