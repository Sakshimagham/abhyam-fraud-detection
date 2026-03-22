import requests
import pandas as pd
import os
from pathlib import Path

def scrape_fake_sites():
    print("\n🚨 Scraping Fake Websites...")

    # --- PATH LOGIC ---
    # This gets the directory where fake_sites.py is located
    current_dir = Path(__file__).resolve().parent 
    # This goes up two levels to FRAUD_AI_SYSTEM and then into the data folder
    output_dir = current_dir.parent.parent / "1_data" / "raw" / "scam_websites"
    
    # Ensure the directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "fake_sites.csv"
    # ------------------

    fake_urls = []
    sources = [
        "https://openphish.com/feed.txt",
        "https://urlhaus.abuse.ch/downloads/text/"
    ]

    for src in sources:
        try:
            print(f"🌐 Fetching from {src}")
            # Added a User-Agent header; some sites block scripts that don't have one
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(src, headers=headers, timeout=20)

            if response.status_code == 200:
                lines = response.text.split("\n")
                # Filter out comments (lines starting with #) and empty lines
                valid_urls = [url.strip() for url in lines if url.startswith("http")]
                fake_urls.extend(valid_urls)

        except Exception as e:
            print(f"❌ Failed source {src}: {e}")

    if not fake_urls:
        print("⚠️ No URLs were collected. Check your internet connection or sources.")
        return

    df = pd.DataFrame(fake_urls, columns=["url"])
    df["label"] = 1

    # Save using the absolute path
    df.to_csv(output_file, index=False)

    print(f"✅ Fake Sites Saved to: {output_file}")
    print(f"📊 Total records: {len(df)}")


if __name__ == "__main__":
    scrape_fake_sites()