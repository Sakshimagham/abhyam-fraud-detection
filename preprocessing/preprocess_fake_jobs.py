import pandas as pd
import re
import nltk
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure resources are available
nltk.download("stopwords")
nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    
    words = text.split()
    words = [w for w in words if w not in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]
    
    return " ".join(words)

def preprocess_fake_jobs(input_file):
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    
    # 1. Handle Labels
    df = df.dropna(subset=["fraudulent"])
    df["label"] = df["fraudulent"].astype(int)
    
    # 2. Combine all text features into one
    columns_to_combine = ["title", "company_profile", "description", "requirements", "benefits"]
    df["text"] = df[columns_to_combine].fillna("").agg(" ".join, axis=1)
    
    # 3. Clean the text
    print("Cleaning text (this may take a moment)...")
    df["clean_text"] = df["text"].apply(clean_text)
    
    # 4. Drop original columns to save space
    # We keep 'clean_text' and 'label'
    cols_to_drop = columns_to_combine + ["job_id", "fraudulent", "text", "location", 
                                       "department", "salary_range", "employment_type", 
                                       "required_experience", "required_education", 
                                       "industry", "function", "telecommuting", 
                                       "has_company_logo", "has_questions"]
    
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors="ignore")
    
    return df

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    # Define your paths (relative to the script location in 3_preprocessing)
    INPUT_PATH = "../1_data/raw/job_posts/fake_job_postings.csv" 
    OUTPUT_DIR = "../1_data/processed/"
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, "fake_jobs_preprocessed.csv")

    # Create directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        # Process
        processed_df = preprocess_fake_jobs(INPUT_PATH)
        
        # Save to CSV
        processed_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Successfully saved: {OUTPUT_FILE}")
        print(f"Processed Rows: {len(processed_df)}")
        
    except FileNotFoundError:
        print(f"Error: Could not find the raw file at {INPUT_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")