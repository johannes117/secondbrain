# ui_components.py
import streamlit as st
from card_operations import add_card, get_all_cards, delete_card, search_cards, update_card, get_card
from utils import truncate_content

def display_card_thumbnail(card_id, content):
    truncated_content = truncate_content(content)
    st.markdown(f"### Card {card_id}")
    st.markdown(truncated_content)
    if st.button("View/Edit", key=f"view_{card_id}"):
        st.session_state.current_screen = "card_viewer"
        st.session_state.current_card_id = card_id
        st.experimental_rerun()

def display_cards_grid(cards, cols=3):
    for i in range(0, len(cards), cols):
        columns = st.columns(cols)
        for j in range(cols):
            if i + j < len(cards):
                with columns[j]:
                    with st.container():
                        card_id, card_content = cards[i+j]
                        display_card_thumbnail(card_id, card_content)
                        st.markdown("---")

def home_screen():
    st.title('SecondBrain')

    if st.button("Add Card"):
        st.session_state.current_screen = "add_card"
        st.experimental_rerun()

    search_query = st.text_input('Search Cards', '')

    if search_query:
        results = search_cards(st.session_state.user_id, search_query, st.session_state.threshold)
        if results:
            display_cards_grid(results, cols=st.session_state.num_columns)
        else:
            st.warning('No matching cards found')
    else:
        cards = get_all_cards(st.session_state.user_id, limit=100)
        if not cards:
            st.info("No cards found. Add some cards to get started!")
        else:
            display_cards_grid(cards, cols=st.session_state.num_columns)

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

def card_viewer_screen():
    card = get_card(st.session_state.current_card_id, st.session_state.user_id)
    if not card:
        st.error("Card not found!")
        return

    st.title(f"Card Viewer - Card {st.session_state.current_card_id}")

    if st.button("Back to Home"):
        st.session_state.current_screen = "home"
        st.experimental_rerun()

    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

    if st.button("Edit" if not st.session_state.edit_mode else "View"):
        st.session_state.edit_mode = not st.session_state.edit_mode
        st.experimental_rerun()

    if st.session_state.edit_mode:
        edited_content = st.text_area("Edit Card Content", value=card[2], height=300)
        if st.button("Save Changes"):
            update_card(st.session_state.current_card_id, st.session_state.user_id, edited_content)
            st.success("Card updated successfully!")
            st.session_state.edit_mode = False
            st.experimental_rerun()
    else:
        st.markdown(card[2])

    if st.button("Delete Card"):
        delete_card(st.session_state.current_card_id, st.session_state.user_id)
        st.success("Card deleted successfully!")
        st.session_state.current_screen = "home"
        st.experimental_rerun()