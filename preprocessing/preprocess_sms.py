import pandas as pd
import re
import nltk
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# --- INITIAL SETUP ---
nltk.download("stopwords")
nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-z\s]", " ", text)       # Remove special chars/numbers
    text = re.sub(r"\s+", " ", text)            # Remove extra whitespace
    words = [lemmatizer.lemmatize(w) for w in text.split() if w not in stop_words]
    return " ".join(words)

def preprocess_sms_files(folder_path):
    all_data = []
    
    # Files identified from your directory
    file_configs = [
        {"name": "spam.csv", "text_col": "Message", "lbl_col": "Category"}, # Based on image_5fe225
        {"name": "spam_ham_india.csv", "text_col": "Msg", "lbl_col": "Label"} # Based on image_5fe1e4
    ]
    
    for config in file_configs:
        path = os.path.join(folder_path, config["name"])
        
        if os.path.exists(path):
            print(f"Reading: {config['name']}...")
            # Use latin-1 to handle special characters seen in your Excel data
            df = pd.read_csv(path, encoding="latin-1")
            
            # Extract and rename columns to a standard format
            temp_df = df[[config["text_col"], config["lbl_col"]]].copy()
            temp_df.columns = ["text", "raw_label"]
            
            # Map labels to numbers (1 for spam, 0 for ham)
            temp_df["label"] = temp_df["raw_label"].astype(str).str.lower().map({
                "spam": 1, "ham": 0
            })
            
            all_data.append(temp_df.dropna(subset=["label"]))
        else:
            print(f"❌ File not found: {config['name']}")

    if not all_data:
        return None
        
    final_df = pd.concat(all_data, ignore_index=True)
    print("Cleaning text data...")
    final_df["clean_text"] = final_df["text"].apply(clean_text)
    
    return final_df[["clean_text", "label"]]

# --- EXECUTION ---
if __name__ == "__main__":
    # Absolute path provided by you
    RAW_DIR = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system\1_data\raw\sms_email"
    OUTPUT_PATH = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system\1_data\processed\sms_preprocessed.csv"

    if os.path.exists(RAW_DIR):
        processed_df = preprocess_sms_files(RAW_DIR)
        
        if processed_df is not None:
            os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
            processed_df.to_csv(OUTPUT_PATH, index=False)
            print(f"✅ Success! Saved {len(processed_df)} rows to: {OUTPUT_PATH}")
    else:
        print(f"❌ Directory not found: {RAW_DIR}")