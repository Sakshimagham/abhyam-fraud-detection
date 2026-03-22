import pandas as pd
import re
import os
from urllib.parse import urlparse
from datetime import datetime

def extract_url_features(url):
    url = str(url)
    parsed = urlparse(url)
    
    return pd.Series({
        "url_length": len(url),
        "num_dots": url.count("."),
        "has_https": 1 if parsed.scheme == "https" else 0,
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": len(re.findall(r"[@\-_%?=]", url)),
        "has_ip": 1 if re.match(r"\d+\.\d+\.\d+\.\d+", parsed.netloc) else 0
    })

def preprocess_websites(base_path):
    # 1. Load all files from the scam_websites folder
    print("Loading datasets from scam_websites...")
    df_fake = pd.read_csv(os.path.join(base_path, "fake_sites.csv"))
    df_real = pd.read_csv(os.path.join(base_path, "real_sites.csv"))
    df_profiles = pd.read_csv(os.path.join(base_path, "real_company_profiles.csv"))

    # 2. Assign labels (1 = Fraudulent/Fake, 0 = Legitimate/Real)
    df_fake["label"] = 1
    df_real["label"] = 0
    df_profiles["label"] = 0

    # 3. Combine them into one DataFrame
    df = pd.concat([df_fake, df_real, df_profiles], ignore_index=True)
    
    # Handle website vs url naming inconsistency
    if "website" in df.columns and "url" not in df.columns:
        df["url"] = df["website"]
    elif "website" in df.columns and "url" in df.columns:
        df["url"] = df["url"].fillna(df["website"])

    # 4. Extract URL features
    if "url" in df.columns:
        print("Extracting URL features...")
        url_features = df["url"].apply(extract_url_features)
        df = pd.concat([df, url_features], axis=1)
    
    # 5. Feature Engineering for Company Data
    if "description" in df.columns:
        print("Processing company descriptions...")
        df["text"] = (
            df["description"].fillna("") + " " +
            df.get("industry", pd.Series([""]*len(df))).fillna("") + " " +
            df.get("key_people", pd.Series([""]*len(df))).fillna("")
        )
        
        current_year = datetime.now().year
        df["company_age"] = current_year - pd.to_numeric(df.get("founded"), errors="coerce")
        df["company_age"] = df["company_age"].fillna(0)
        
        df["revenue_available"] = df.get("revenue").notnull().astype(int)
        df["has_headquarters"] = df.get("headquarters").notnull().astype(int)

    # Keep only the features useful for machine learning
    cols_to_keep = ["label", "url_length", "num_dots", "has_https", "num_digits", 
                    "num_special_chars", "has_ip", "company_age", "revenue_available", 
                    "has_headquarters", "text"]
    
    existing_cols = [c for c in cols_to_keep if c in df.columns]
    return df[existing_cols]

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    # Path updated to point to the subfolder seen in your screenshot
    INPUT_DIR = "../1_data/raw/scam_websites/" 
    OUTPUT_PATH = "../1_data/processed/websites_preprocessed.csv"

    if os.path.exists(INPUT_DIR):
        try:
            processed_df = preprocess_websites(INPUT_DIR)
            
            os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
            processed_df.to_csv(OUTPUT_PATH, index=False)
            
            print(f"✅ Success! Combined {len(processed_df)} rows.")
            print(f"📁 File saved to: {OUTPUT_PATH}")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
    else:
        print(f"❌ Folder not found: {INPUT_DIR}")