import pandas as pd
import numpy as np
import os
from datetime import datetime

def preprocess_social_media(fake_path, real_path):
    print(f"Reading social media files...")
    #
    df_fake = pd.read_csv(fake_path)
    df_real = pd.read_csv(real_path)
    
    df_fake["label"] = 1
    df_real["label"] = 0
    
    df = pd.concat([df_fake, df_real], ignore_index=True)
    
    # Clean numeric columns
    numeric_cols = ["statuses_count", "followers_count", "friends_count", 
                    "favourites_count", "listed_count"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    
    if "followers_count" in df.columns and "friends_count" in df.columns:
        df["follower_friend_ratio"] = df["followers_count"] / (df["friends_count"] + 1)
    
    # --- FIXED TIMEZONE LOGIC ---
    if "created_at" in df.columns:
        # 1. Convert to datetime
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        
        # 2. Strip timezone info to make it 'tz-naive'
        df["created_at"] = df["created_at"].dt.tz_localize(None)
        
        # 3. Use a naive current date
        current_date = datetime(2026, 2, 16)
        df["account_age_days"] = (current_date - df["created_at"]).dt.days.fillna(0)
    
    if "description" in df.columns:
        df["description_len"] = df["description"].fillna("").apply(len)
        df["has_description"] = df["description"].notnull().astype(int)
    
    features = [
        "label", "statuses_count", "followers_count", "friends_count", 
        "favourites_count", "listed_count", "follower_friend_ratio", 
        "account_age_days", "description_len", "has_description"
    ]
    
    # Only return columns that actually exist in the dataframe
    existing_features = [f for f in features if f in df.columns]
    return df[existing_features]

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    # Ensure these paths match your actual D: drive structure
    RAW_DIR = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system\1_data\raw\social_media"
    FAKE_PATH = os.path.join(RAW_DIR, "fake_users.csv")
    REAL_PATH = os.path.join(RAW_DIR, "real_users.csv")
    OUTPUT_PATH = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system\1_data\processed\social_media_preprocessed.csv"

    if os.path.exists(FAKE_PATH) and os.path.exists(REAL_PATH):
        processed_df = preprocess_social_media(FAKE_PATH, REAL_PATH)
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        processed_df.to_csv(OUTPUT_PATH, index=False)
        print(f"✅ Success! Saved {len(processed_df)} rows to: {OUTPUT_PATH}")
    else:
        print(f"❌ Error: Could not find raw files in {RAW_DIR}")