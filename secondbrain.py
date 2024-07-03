import streamlit as st
import sqlite3
from rapidfuzz import fuzz, process

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
def get_all_cards(limit=100):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    if limit is None:
        c.execute('SELECT * FROM cards ORDER BY id DESC')
    else:
        c.execute('SELECT * FROM cards ORDER BY id DESC LIMIT ?', (limit,))
    cards = c.fetchall()
    conn.close()
    return cards

# Function to delete a card from the database
def delete_card(card_id):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('DELETE FROM cards WHERE id = ?', (card_id,))
    conn.commit()
    conn.close()

# Function to search cards based on content (case-insensitive)
def search_cards(query, threshold=70):
    all_cards = get_all_cards(limit=None)  # Get all cards for searching
    matched_cards = []
    query = query.lower()
    for card in all_cards:
        card_content = card[1].lower()
        score = fuzz.partial_ratio(query, card_content)
        if score >= threshold:
            matched_cards.append((card[0], card[1], score))
    return matched_cards

# Function to display a card with Markdown formatting
def display_card(card_id, content):
    st.markdown(f"### Card ID: {card_id}")
    st.markdown(content)
    if st.button(f"Delete Card {card_id}", key=f"delete_{card_id}"):
        delete_card(card_id)
        st.success(f"Card {card_id} deleted successfully!")
        st.rerun()

# Function to display cards in a grid
def display_cards_grid(cards, cols=3):
    for i in range(0, len(cards), cols):
        columns = st.columns(cols)
        for j in range(cols):
            if i + j < len(cards):
                with columns[j]:
                    with st.container():
                        display_card(cards[i+j][0], cards[i+j][1])
                        st.markdown("---")

# Initialize the app
init_db()

# Streamlit UI
st.title('SecondBrain')

# Sidebar for adding new cards
st.sidebar.title('Add New Card')
new_card_content = st.sidebar.text_area('Card Content (Markdown supported)', height=150)
if st.sidebar.button('Add Card'):
    if new_card_content:
        add_card(new_card_content)
        st.sidebar.success('Card added successfully!')
        st.rerun()
    else:
        st.sidebar.error('Content cannot be empty')

# Main screen for searching and displaying cards
search_query = st.text_input('Search Cards', '')
threshold = st.slider('Fuzzy Match Threshold', 0, 100, 70)

# Number of columns in the grid
num_columns = st.sidebar.number_input('Number of columns', min_value=1, max_value=4, value=3)

if search_query:
    results = search_cards(search_query, threshold)
    if results:
        display_cards_grid(results, cols=num_columns)
    else:
        st.warning('No matching cards found')
else:
    # Display the first 100 cards when not searching
    cards = get_all_cards(limit=100)
    if not cards:
        st.info("No cards found. Add some cards to get started!")
    else:
        display_cards_grid(cards, cols=num_columns)