# components/link_analyzer.py
import re
import requests
from urllib.parse import urlparse

def extract_links(text):
    return re.findall(r'https?://[^\s]+', text)

def get_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return ""

def fetch_page_title(url, timeout=5):
    try:
        resp = requests.get(url, timeout=timeout)
        match = re.search(r'<title>(.*?)</title>', resp.text, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else "No title found"
    except Exception as e:
        return f"Unreachable ({str(e)})"