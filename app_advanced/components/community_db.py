import pandas as pd
import os
from datetime import datetime

POSTS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'community', 'posts.csv')

def load_posts():
    os.makedirs(os.path.dirname(POSTS_FILE), exist_ok=True)
    if os.path.exists(POSTS_FILE):
        return pd.read_csv(POSTS_FILE)
    return pd.DataFrame(columns=['timestamp', 'author', 'title', 'content', 'category', 'link'])

def save_post(author, title, content, category, link=''):
    df = load_posts()
    new = pd.DataFrame([{
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'author': author,
        'title': title,
        'content': content,
        'category': category,
        'link': link
    }])
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(POSTS_FILE, index=False)