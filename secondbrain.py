import streamlit as st
import sqlite3
from rapidfuzz import fuzz

# Initialize database
def init_db():
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS cards
              (id INTEGER PRIMARY KEY, 
              content TEXT NOT NULL)
              ''')
    conn.commit()
    conn.close()

# Function to add a card to the database
def add_card(content):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('INSERT INTO cards (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()

# Function to get all cards from the database
def get_all_cards():
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('SELECT * FROM cards')
    cards = c.fetchall()
    conn.close()
    return cards

# Function to search cards based on content
def search_cards(query, threshold=70):
    all_cards = get_all_cards()
    matched_cards = []
    for card in all_cards:
        score = fuzz.token_set_ratio(query, card[1])
        if score >= threshold:
            matched_cards.append((card[0], card[1], score))
    return matched_cards

# Initialize the app
init_db()

# Streamlit UI
st.title('Simple Offline MyMind')
st.sidebar.title('Options')
option = st.sidebar.selectbox('Choose an action', ['Add Card', 'View All Cards', 'Search Cards'])

if option == 'Add Card':
    st.header('Add a New Card')
    content = st.text_area('Card Content', height=150)
    if st.button('Add Card'):
        if content:
            add_card(content)
            st.success('Card added successfully!')
        else:
            st.error('Content cannot be empty')

elif option == 'View All Cards':
    st.header('All Cards')
    cards = get_all_cards()
    for card in cards:
        st.text_area(f"Card ID: {card[0]}", value=card[1], height=200)

elif option == 'Search Cards':
    st.header('Search Cards')
    query = st.text_input('Search Query')
    threshold = st.slider('Fuzzy Match Threshold', 0, 100, 70)
    if st.button('Search'):
        results = search_cards(query, threshold)
        if results:
            for result in results:
                st.write(f"Card ID: {result[0]} | Match Score: {result[2]}")
                st.text_area("Card Content", value=result[1], height=200)
        else:
            st.warning('No matching cards found')
