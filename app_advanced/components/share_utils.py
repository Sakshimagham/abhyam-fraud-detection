# components/share_utils.py
import urllib.parse

def get_whatsapp_link(text):
    return f"https://wa.me/?text={urllib.parse.quote(text)}"

def get_email_link(subject, body):
    return f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

def get_twitter_link(text):
    return f"https://twitter.com/intent/tweet?text={urllib.parse.quote(text)}"