import streamlit as st
import sqlite3
from rapidfuzz import fuzz
import textwrap
import hashlib

# Utility functions for hashing passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize database
def init_db():
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS users
              (id INTEGER PRIMARY KEY, 
              username TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL)
              ''')
    c.execute('''
              CREATE TABLE IF NOT EXISTS cards
              (id INTEGER PRIMARY KEY, 
              user_id INTEGER NOT NULL,
              content TEXT NOT NULL,
              FOREIGN KEY (user_id) REFERENCES users (id))
              ''')
    conn.commit()
    conn.close()

# Function to register a new user
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

# Function to login a user
def login_user(username, password):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

# Function to add a card to the database
def add_card(user_id, content):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('INSERT INTO cards (user_id, content) VALUES (?, ?)', (user_id, content))
    conn.commit()
    conn.close()

# Function to get all cards from the database for a specific user
def get_all_cards(user_id, limit=100):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    if limit is None:
        c.execute('SELECT id, user_id, content FROM cards WHERE user_id = ? ORDER BY id DESC', (user_id,))
    else:
        c.execute('SELECT id, user_id, content FROM cards WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
    cards = c.fetchall()
    conn.close()
    return cards

# Function to delete a card from the database
def delete_card(card_id, user_id):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('DELETE FROM cards WHERE id = ? AND user_id = ?', (card_id, user_id))
    conn.commit()
    conn.close()

# Function to search cards based on content (case-insensitive) for a specific user
def search_cards(user_id, query, threshold=70):
    all_cards = get_all_cards(user_id, limit=None)  # Get all cards for searching
    matched_cards = []
    query = query.lower()
    for card in all_cards:
        card_content = card[2].lower()
        score = fuzz.partial_ratio(query, card_content)
        if score >= threshold:
            matched_cards.append((card[0], card[2], score))
    return matched_cards

# Function to update a card in the database
def update_card(card_id, user_id, content):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('UPDATE cards SET content = ? WHERE id = ? AND user_id = ?', (content, card_id, user_id))
    conn.commit()
    conn.close()

# Function to get a single card from the database
def get_card(card_id, user_id):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('SELECT * FROM cards WHERE id = ? AND user_id = ?', (card_id, user_id))
    card = c.fetchone()
    conn.close()
    return card

# Function to truncate content for thumbnail display
def truncate_content(content, max_length=100):
    if isinstance(content, str):
        return textwrap.shorten(content, width=max_length, placeholder="...")
    return str(content)[:max_length] + '...'

# Function to display a card thumbnail
def display_card_thumbnail(card_id, content):
    truncated_content = truncate_content(content)
    st.markdown(f"### Card {card_id}")
    st.markdown(truncated_content)
    if st.button("View/Edit", key=f"view_{card_id}"):
        st.session_state.current_screen = "card_viewer"
        st.session_state.current_card_id = card_id
        st.experimental_rerun()

# Function to display cards in a grid
def display_cards_grid(cards, cols=3):
    for i in range(0, len(cards), cols):
        columns = st.columns(cols)
        for j in range(cols):
            if i + j < len(cards):
                with columns[j]:
                    with st.container():
                        card_id = cards[i+j][0]
                        card_content = cards[i+j][2]  # Ensure this gets the correct content
                        display_card_thumbnail(card_id, card_content)
                        st.markdown("---")

# Function to display the home screen
def home_screen():
    st.title('SecondBrain')

    # Button to navigate to Add Card screen
    if st.button("Add Card"):
        st.session_state.current_screen = "add_card"
        st.experimental_rerun()

    # Main screen for searching and displaying cards
    search_query = st.text_input('Search Cards', '')

    if search_query:
        results = search_cards(st.session_state.user_id, search_query, st.session_state.threshold)
        if results:
            display_cards_grid(results, cols=st.session_state.num_columns)
        else:
            st.warning('No matching cards found')
    else:
        # Display the first 100 cards when not searching
        cards = get_all_cards(st.session_state.user_id, limit=100)
        if not cards:
            st.info("No cards found. Add some cards to get started!")
        else:
            display_cards_grid(cards, cols=st.session_state.num_columns)

# Function to display the add card screen
def add_card_screen():
    st.title('Add New Card')

    new_card_content = st.text_area('Card Content (Markdown supported)', height=150)
    if st.button('Add Card'):
        if new_card_content:
            add_card(st.session_state.user_id, new_card_content)
            st.success('Card added successfully!')
            st.session_state.current_screen = "home"
            st.experimental_rerun()
        else:
            st.error('Content cannot be empty')

    if st.button("Back to Home"):
        st.session_state.current_screen = "home"
        st.experimental_rerun()

# Function to display the card viewer screen
def card_viewer_screen():
    card = get_card(st.session_state.current_card_id, st.session_state.user_id)
    if not card:
        st.error("Card not found!")
        return

    st.title(f"Card Viewer - Card {st.session_state.current_card_id}")

    if st.button("Back to Home"):
        st.session_state.current_screen = "home"
        st.experimental_rerun()

    # Initialize edit mode in session state if not present
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

    # Toggle edit mode
    if st.button("Edit" if not st.session_state.edit_mode else "View"):
        st.session_state.edit_mode = not st.session_state.edit_mode
        st.experimental_rerun()

    if st.session_state.edit_mode:
        # Edit mode
        edited_content = st.text_area("Edit Card Content", value=card[2], height=300)
        if st.button("Save Changes"):
            update_card(st.session_state.current_card_id, st.session_state.user_id, edited_content)
            st.success("Card updated successfully!")
            st.session_state.edit_mode = False
            st.experimental_rerun()
    else:
        # View mode
        st.markdown(card[2])

    # Delete button (available in both modes)
    if st.button("Delete Card"):
        delete_card(st.session_state.current_card_id, st.session_state.user_id)
        st.success("Card deleted successfully!")
        st.session_state.current_screen = "home"
        st.experimental_rerun()

# Function to display the login screen
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

# Function to display the registration screen
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

# Initialize the app
init_db()

# Initialize session state for navigation
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = "login"
if 'threshold' not in st.session_state:
    st.session_state.threshold = 70
if 'num_columns' not in st.session_state:
    st.session_state.num_columns = 3

# Sidebar configuration
st.set_page_config(initial_sidebar_state="collapsed")

# Sidebar content
if 'user_id' in st.session_state:
    st.sidebar.title('Settings')
    st.sidebar.header('Search Settings')
    st.session_state.threshold = st.sidebar.slider('Fuzzy Match Threshold', 0, 100, 70)
    st.session_state.num_columns = st.sidebar.number_input('Number of columns', min_value=1, max_value=4, value=3)
    st.sidebar.markdown("---")
    if st.sidebar.button('Logout'):
        st.session_state.clear()
        st.session_state.current_screen = "login"
        st.experimental_rerun()

# Main app logic
if st.session_state.current_screen == "home":
    home_screen()
elif st.session_state.current_screen == "add_card":
    add_card_screen()
elif st.session_state.current_screen == "card_viewer":
    card_viewer_screen()
elif st.session_state.current_screen == "login":
    login_screen()
elif st.session_state.current_screen == "register":
    register_screen()
