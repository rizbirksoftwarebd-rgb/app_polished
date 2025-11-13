import streamlit as st
from config import APP_TITLE, LOGO_PATH
from auth.auth import Auth
from home.home import HomePage
from about.about import AboutPage
from admin.admin import AdminPage
import ensure_db

def load_css(path):
    try:
        with open(path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

class App:
    def __init__(self):
        ensure_db.init_db()
        st.set_page_config(page_title=APP_TITLE, page_icon=":sparkles:", layout="wide")
        self.auth = Auth()
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
            st.session_state.username = None

    def show_login(self):
        load_css("auth/auth.css")
        st.markdown("<div style='display:flex;align-items:center;justify-content:center;height:78vh'>", unsafe_allow_html=True)
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center'><img src=\"{LOGO_PATH}\" width=220/></div>", unsafe_allow_html=True)
        st.header("Sign in to Multi-Tasker")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Sign in"):
                ok, msg = self.auth.authenticate(username.strip(), password)
                if ok:
                    st.session_state.logged_in = True
                    st.session_state.username = username.strip()
                    st.experimental_rerun()
                else:
                    st.error(msg or "Invalid credentials.")
        with col2:
            st.write(" ")
        st.markdown("</div></div>", unsafe_allow_html=True)

    def show_app(self):
        load_css("home/home.css")
        with st.sidebar:
            st.markdown(f"<img src='{LOGO_PATH}' width='140'/>", unsafe_allow_html=True)
            st.markdown("### Navigation")
            role = self.auth.get_role(st.session_state.username)
            if role == 'admin':
                page = st.radio("Go to", ["Home","About","Admin"])
            else:
                page = st.radio("Go to", ["Home","About"])
            st.markdown("---")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.experimental_rerun()

        if page == "Home":
            HomePage(self).run()
        elif page == "About":
            AboutPage(self).run()
        else:
            AdminPage(self).run()

def main():
    app = App()
    if not st.session_state.logged_in:
        app.show_login()
    else:
        app.show_app()

if __name__ == "__main__":
    main()
