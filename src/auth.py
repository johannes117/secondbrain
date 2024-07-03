# auth.py
import streamlit as st
import sqlite3
from utils import hash_password, generate_session_token

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
    c.execute('SELECT id, username FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

def check_session_token(token):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('SELECT id, username FROM users WHERE session_token = ?', (token,))
    user = c.fetchone()
    conn.close()
    return user

def load_session():
    if 'session_token' in st.query_params:
        user = check_session_token(st.query_params['session_token'])
        if user:
            st.session_state.user_id = user[0]
            st.session_state.username = user[1]
            st.session_state.current_screen = "home"

def login_screen():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    remember_me = st.checkbox('Remember Me')
    if st.button('Login'):
        user = login_user(username, password)
        if user:
            st.session_state.user_id = user[0]
            st.session_state.username = user[1]
            if remember_me:
                session_token = generate_session_token()
                conn = sqlite3.connect('cards.db')
                c = conn.cursor()
                c.execute('UPDATE users SET session_token = ? WHERE id = ?', (session_token, user[0]))
                conn.commit()
                conn.close()
                st.query_params['session_token'] = session_token
            st.session_state.current_screen = "home"
            st.rerun()
        else:
            st.error('Invalid username or password')
    if st.button('Register'):
        st.session_state.current_screen = "register"
        st.rerun()

def register_screen():
    st.title('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Register'):
        if register_user(username, password):
            st.success('User registered successfully!')
            st.session_state.current_screen = "login"
            st.rerun()
        else:
            st.error('Username already exists')
    if st.button('Back to Login'):
        st.session_state.current_screen = "login"
        st.rerun()