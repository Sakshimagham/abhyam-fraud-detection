import pandas as pd
import numpy as np
import re
from datetime import datetime

# === 1. Load dataset ===
raw_data_path = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system\1_data\raw\crypto_fraud\Bitcoin_Scam_Detection_Dataset_2025.csv"
df = pd.read_csv(raw_data_path)

# Quick look
print("Initial shape:", df.shape)
print(df.head())

# === 2. Clean text data ===
def clean_text(text):
    if pd.isnull(text):
        return ""
    text = text.lower()  # lowercase
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # remove URLs
    text = re.sub(r"[^a-z0-9\s]", "", text)  # remove punctuation/special chars
    text = re.sub(r"\s+", " ", text).strip()  # remove extra spaces
    return text

df['message_text_clean'] = df['message_text'].apply(clean_text)

# === 3. Handle missing values ===
# For numerical columns, fill NaNs with median
num_cols = ['promised_return_pct', 'sentiment_score', 'message_length']
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # ensure numeric
    df[col] = df[col].fillna(df[col].median())

# For categorical columns, fill NaNs with 'unknown'
cat_cols = ['label', 'scam_type', 'platform', 'contains_link', 'btc_address_present', 'urgency_level']
for col in cat_cols:
    df[col] = df[col].fillna('unknown')

# === 4. Encode categorical variables ===
# Simple mapping for binary columns
binary_map = {'Yes': 1, 'No': 0, 'unknown': 0}
df['contains_link'] = df['contains_link'].map(binary_map)
df['btc_address_present'] = df['btc_address_present'].map(binary_map)

# One-hot encoding for multi-class categorical columns
multi_class_cols = ['label', 'scam_type', 'platform', 'urgency_level']
df = pd.get_dummies(df, columns=multi_class_cols, drop_first=True)

# === 5. Convert timestamp ===
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
df['message_hour'] = df['created_at'].dt.hour
df['message_day'] = df['created_at'].dt.day
df['message_month'] = df['created_at'].dt.month
df['message_weekday'] = df['created_at'].dt.weekday

# === 6. Feature Engineering ===
# Example: message length normalized
df['message_length_norm'] = df['message_length'] / df['message_length'].max()

# Example: BTC address flag
df['btc_address_flag'] = df['btc_address_present']

# === 7. Remove unnecessary columns ===
drop_cols = ['message_id', 'message_text', 'created_at']
df = df.drop(columns=drop_cols)

# === 8. Save preprocessed data ===
processed_path = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system\1_data\processed\crypto_fraud_preprocessed.csv"
df.to_csv(processed_path, index=False)
print("Preprocessing completed. Saved to:", processed_path)
print("Processed shape:", df.shape)