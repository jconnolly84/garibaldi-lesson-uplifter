
import streamlit as st
from auth_utils import get_google_auth_url, get_microsoft_auth_url

def show_login():
    st.title("Login to Lessonary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("Login with Google", get_google_auth_url())
        
    with col2:
        st.link_button("Login with Microsoft", get_microsoft_auth_url())

def main_dashboard():
    user = st.session_state.get('user', {})
    st.write(f"Welcome, {user.get('name', user.get('email', 'User'))}!")
    # Main Lessonary dashboard here...

if __name__ == "__main__":
    if 'user' in st.session_state:
        main_dashboard()
    else:
        show_login()
