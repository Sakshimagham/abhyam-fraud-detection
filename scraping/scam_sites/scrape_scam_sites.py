import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

print("\n🚀 FULL COMPANY PROFILE SCRAPER STARTED\n")

BASE = "https://en.wikipedia.org"
START = "https://en.wikipedia.org/wiki/List_of_companies_of_India"

headers = {"User-Agent": "Mozilla/5.0"}

dataset = []

# ----------------------------------------------------
# STEP 1 — GET COMPANY LIST
# ----------------------------------------------------
page = requests.get(START, headers=headers)
soup = BeautifulSoup(page.text, "lxml")

tables = soup.select("table.wikitable")

company_links = []

for table in tables:
    for row in table.find_all("tr")[1:]:
        link = row.find("a")
        if link and link.get("href"):
            company_links.append(urljoin(BASE, link["href"]))

print(f"📊 Companies Found: {len(company_links)}")

# ----------------------------------------------------
# STEP 2 — SCRAPE EACH COMPANY PAGE
# ----------------------------------------------------
for url in company_links[:400]:

    try:
        print(f"🌐 Scraping {url}")

        res = requests.get(url, headers=headers)
        comp_soup = BeautifulSoup(res.text, "lxml")

        name = comp_soup.find("h1").text.strip()

        infobox = comp_soup.select_one("table.infobox")

        industry = ""
        founded = ""
        headquarters = ""
        company_type = ""
        revenue = ""
        website = ""
        key_people = ""

        if infobox:
            rows = infobox.find_all("tr")

            for row in rows:
                header = row.find("th")
                value = row.find("td")

                if not header or not value:
                    continue

                text = value.text.strip()

                if "Industry" in header.text:
                    industry = text

                elif "Founded" in header.text:
                    founded = text

                elif "Headquarters" in header.text:
                    headquarters = text

                elif "Type" in header.text:
                    company_type = text

                elif "Revenue" in header.text:
                    revenue = text

                elif "Key people" in header.text:
                    key_people = text

                elif "Website" in header.text:
                    link = value.find("a")
                    if link:
                        website = link.get("href")

        # ------------------------------------------------
        # PAGE DESCRIPTION
        # ------------------------------------------------
        description = ""

        paragraphs = comp_soup.select("p")

        for p in paragraphs:
            if len(p.text) > 50:
                description = p.text.strip()
                break

        if website:
            dataset.append({
                "company": name,
                "industry": industry,
                "founded": founded,
                "headquarters": headquarters,
                "type": company_type,
                "revenue": revenue,
                "key_people": key_people,
                "description": description,
                "website": website,
                "label": 0
            })

        time.sleep(1)

    except Exception as e:
        print("❌ Error:", e)

# ----------------------------------------------------
# SAVE DATASET
# ----------------------------------------------------
df = pd.DataFrame(dataset)

output = "../1_data/raw/scam_websites/real_company_profiles.csv"
df.to_csv(output, index=False)

print("\n✅ REAL COMPANY PROFILE DATASET CREATED")
print(f"📊 Records: {len(df)}")
print(f"📁 Saved: {output}")