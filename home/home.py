import streamlit as st
from config import LOGO_PATH
from auth.auth import Auth

class HomePage:
    def __init__(self, app):
        self.app = app
        self.auth = Auth()

    def run(self):
        st.markdown(f"<div class='header'><img src='{LOGO_PATH}' width='160'/> <div><h2>Welcome to Multi-Tasker</h2><p style='margin-top:-8px'>A polished demo with role-based access and Render-ready DB support.</p></div></div>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<div class='card'><h3>Quick Task</h3><p>Create and manage your tasks here (demo).</p></div>", unsafe_allow_html=True)
        role = self.auth.get_role(st.session_state.get('username'))
        if role == 'admin':
            st.info("You are an admin — use the Admin Console from the sidebar to manage users.")
