import os
import re
import pandas as pd

# -----------------------------
# 1️⃣ Define Paths
# -----------------------------
BASE_PATH = r"D:\SKM-IMP\SAKSHI PROJECT\final\fraud_ai_system"
RAW_PATH = os.path.join(BASE_PATH, "1_data", "raw", "call_transcripts")
PROCESSED_PATH = os.path.join(BASE_PATH, "1_data", "processed")
os.makedirs(PROCESSED_PATH, exist_ok=True)

# -----------------------------
# 2️⃣ Text Cleaning Function
# -----------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"\[.*?\]", "", text)  # remove placeholders like [Company]
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # remove special chars
    text = re.sub(r"\s+", " ", text).strip()    # remove extra spaces
    return text

# -----------------------------
# 3️⃣ Load TXT Files Dynamically
# -----------------------------
def load_txt_file(filepath, label_value):
    texts = []
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() != "":
                texts.append({
                    "text": clean_text(line),
                    "label": label_value
                })
    return pd.DataFrame(texts)

# Auto-detect TXT files
txt_files = [f for f in os.listdir(RAW_PATH) if f.lower().endswith(".txt")]

df_list = []

for file in txt_files:
    if "scam" in file.lower():
        df_list.append(load_txt_file(os.path.join(RAW_PATH, file), 1))
    else:
        df_list.append(load_txt_file(os.path.join(RAW_PATH, file), 0))

# -----------------------------
# 4️⃣ Process any CSV files dynamically
# -----------------------------
csv_files = [f for f in os.listdir(RAW_PATH) if f.lower().endswith(".csv")]

for file in csv_files:
    df_csv = pd.read_csv(os.path.join(RAW_PATH, file))
    
    # Keep only TEXT and LABEL columns if they exist
    if set(["TEXT", "LABEL"]).issubset(df_csv.columns):
        df_csv = df_csv[["TEXT", "LABEL"]]
        df_csv.columns = ["text", "label"]
        df_csv["label"] = df_csv["label"].apply(lambda x: 1 if str(x).lower() == "scam" else 0)
        df_csv["text"] = df_csv["text"].apply(clean_text)
        df_list.append(df_csv)

# -----------------------------
# 5️⃣ Merge all data
# -----------------------------
df_final = pd.concat(df_list, ignore_index=True)
df_final.drop_duplicates(inplace=True)
df_final = df_final[df_final["text"] != ""]

# -----------------------------
# 6️⃣ Save processed file
# -----------------------------
output_path = os.path.join(PROCESSED_PATH, "call_data_cleaned.csv")
df_final.to_csv(output_path, index=False)

print("✅ Call transcript preprocessing completed!")
print(f"Saved to: {output_path}")
print(f"Total records: {len(df_final)}")
