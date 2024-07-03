# utils.py
import hashlib
import textwrap
import secrets

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def truncate_content(content, max_length=100):
    if isinstance(content, str):
        return textwrap.shorten(content, width=max_length, placeholder="...")
    return str(content)[:max_length] + '...'

def generate_session_token():
    return secrets.token_urlsafe(32)