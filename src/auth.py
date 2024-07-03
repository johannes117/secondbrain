# auth.py
import streamlit as st
import sqlite3
from utils import hash_password

def register_user(username, password):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def login_user(username, password):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

def login_screen():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        user = login_user(username, password)
        if user:
            st.session_state.user_id = user[0]
            st.session_state.username = username
            st.session_state.current_screen = "home"
            st.experimental_rerun()
        else:
            st.error('Invalid username or password')
    if st.button('Register'):
        st.session_state.current_screen = "register"
        st.experimental_rerun()

def register_screen():
    st.title('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Register'):
        if register_user(username, password):
            st.success('User registered successfully!')
            st.session_state.current_screen = "login"
            st.experimental_rerun()
        else:
            st.error('Username already exists')
    if st.button('Back to Login'):
        st.session_state.current_screen = "login"
        st.experimental_rerun()