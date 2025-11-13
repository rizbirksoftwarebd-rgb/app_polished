import streamlit as st

class AboutPage:
    def __init__(self, app):
        self.app = app

    def run(self):
        st.title("About")
        st.markdown("""
        **Multi-Tasker** — polished version.

        - Uses SQLAlchemy and supports `DATABASE_URL` (use Render managed DB).
        - Simple hashed-password auth (PBKDF2).
        - Admin console for user creation.
        - Auto-initializes DB/tables on startup.
        """)
