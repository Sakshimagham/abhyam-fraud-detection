# components/company_verifier.py
import pandas as pd
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'trusted_companies.csv')

def load_companies():
    """Load trusted companies from CSV."""
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame(columns=['name', 'domain', 'logo_url'])

def extract_company_mentions(text):
    """Return list of companies mentioned in text (case‑insensitive)."""
    companies = load_companies()
    found = []
    text_lower = text.lower()
    for _, row in companies.iterrows():
        if row['name'].lower() in text_lower:
            found.append(row.to_dict())
    return found

def verify_sender(company_domain, sender_email):
    """Check if sender email domain matches company domain."""
    if not sender_email or '@' not in sender_email:
        return False
    sender_domain = sender_email.split('@')[-1].lower()
    return sender_domain == company_domain.lower() or sender_domain.endswith('.' + company_domain.lower())