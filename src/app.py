# app.py
import streamlit as st
from database import init_db
from auth import login_screen, register_screen
from ui_components import home_screen, add_card_screen, card_viewer_screen

def main():
    init_db()

    if 'current_screen' not in st.session_state:
        st.session_state.current_screen = "login"
    if 'threshold' not in st.session_state:
        st.session_state.threshold = 70
    if 'num_columns' not in st.session_state:
        st.session_state.num_columns = 3

    st.set_page_config(initial_sidebar_state="collapsed")

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

if __name__ == "__main__":
    main()