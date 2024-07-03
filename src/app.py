# app.py
import streamlit as st
from database import init_db
from auth import login_screen, register_screen, check_session_token
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

    # Check for existing session token using st.query_params
    if 'session_token' in st.query_params:
        user = check_session_token(st.query_params['session_token'])
        if user:
            st.session_state.user_id = user[0]
            st.session_state.username = user[1]
            st.session_state.current_screen = "home"

    if 'user_id' in st.session_state:
        st.sidebar.title('Settings')
        st.sidebar.header('Search Settings')
        st.session_state.threshold = st.sidebar.slider('Fuzzy Match Threshold', 0, 100, 70)
        st.session_state.num_columns = st.sidebar.number_input('Number of columns', min_value=1, max_value=4, value=3)
        st.sidebar.markdown("---")
        if st.sidebar.button('Logout'):
            st.session_state.clear()
            st.query_params.clear()  # Clear the session token from URL
            st.rerun()

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

    # Add JavaScript to set session token in local storage
    st.markdown("""
        <script>
        const params = new URLSearchParams(window.location.search);
        const session_token = params.get('session_token');
        if (session_token) {
            localStorage.setItem('session_token', session_token);
        }
        const stored_token = localStorage.getItem('session_token');
        if (stored_token && !session_token) {
            window.location.search = `session_token=${stored_token}`;
        }
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()