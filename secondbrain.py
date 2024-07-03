import streamlit as st
import sqlite3
from rapidfuzz import fuzz, process
import textwrap

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

# Function to update a card in the database
def update_card(card_id, content):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('UPDATE cards SET content = ? WHERE id = ?', (content, card_id))
    conn.commit()
    conn.close()

# Function to get a single card from the database
def get_card(card_id):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
    card = c.fetchone()
    conn.close()
    return card

# Function to truncate content for thumbnail display
def truncate_content(content, max_length=100):
    return textwrap.shorten(content, width=max_length, placeholder="...")

# Function to display a card thumbnail
def display_card_thumbnail(card_id, content):
    truncated_content = truncate_content(content)
    st.markdown(f"### Card {card_id}")
    st.markdown(truncated_content)
    if st.button("View/Edit", key=f"view_{card_id}"):
        st.session_state.current_screen = "card_viewer"
        st.session_state.current_card_id = card_id
        st.rerun()

# Function to display cards in a grid
def display_cards_grid(cards, cols=3):
    for i in range(0, len(cards), cols):
        columns = st.columns(cols)
        for j in range(cols):
            if i + j < len(cards):
                with columns[j]:
                    with st.container():
                        display_card_thumbnail(cards[i+j][0], cards[i+j][1])
                        st.markdown("---")

# Function to display the home screen
def home_screen():
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

# Function to display the card viewer screen
def card_viewer_screen():
    card = get_card(st.session_state.current_card_id)
    if not card:
        st.error("Card not found!")
        return

    st.title(f"Card Viewer - Card {st.session_state.current_card_id}")

    if st.button("Back to Home"):
        st.session_state.current_screen = "home"
        st.rerun()

    # Initialize edit mode in session state if not present
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

    # Toggle edit mode
    if st.button("Edit" if not st.session_state.edit_mode else "View"):
        st.session_state.edit_mode = not st.session_state.edit_mode
        st.rerun()

    if st.session_state.edit_mode:
        # Edit mode
        edited_content = st.text_area("Edit Card Content", value=card[1], height=300)
        if st.button("Save Changes"):
            update_card(st.session_state.current_card_id, edited_content)
            st.success("Card updated successfully!")
            st.session_state.edit_mode = False
            st.rerun()
    else:
        # View mode
        st.markdown(card[1])

    # Delete button (available in both modes)
    if st.button("Delete Card"):
        delete_card(st.session_state.current_card_id)
        st.success("Card deleted successfully!")
        st.session_state.current_screen = "home"
        st.rerun()

# Initialize the app
init_db()

# Initialize session state for navigation
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = "home"

# Main app logic
if st.session_state.current_screen == "home":
    home_screen()
elif st.session_state.current_screen == "card_viewer":
    card_viewer_screen()