import streamlit as st
from db import list_users, add_or_update_user
import re, binascii, secrets, hashlib
from ensure_db import init_db

def hash_password(password: str, salt: bytes=None, iterations: int=100_000):
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    return {
        "algorithm": "pbkdf2_sha256",
        "iterations": iterations,
        "salt": binascii.hexlify(salt).decode(),
        "hash": binascii.hexlify(dk).decode()
    }

def valid_password(p):
    if len(p) < 8: return False, "Minimum 8 characters required"
    if not re.search(r"[A-Z]", p): return False, "At least one uppercase letter required"
    if not re.search(r"[a-z]", p): return False, "At least one lowercase letter required"
    if not re.search(r"[0-9]", p): return False, "At least one digit required"
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]", p): return False, "At least one special character required"
    return True, ""

class AdminPage:
    def __init__(self, app):
        self.app = app
        init_db()

    def run(self):
        st.title("Admin Console")
        st.write("Create users and manage roles.")
        with st.expander("Existing users"):
            users = list_users()
            for u in users:
                st.write(f"- **{u['username']}** — role: {u['role']}")
        st.markdown('---')
        st.subheader("Create / Update user")
        with st.form("create_user"):
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            role = st.selectbox("Role", ["user","admin"])
            submitted = st.form_submit_button("Create / Update")
            if submitted:
                ok, msg = valid_password(password)
                if not ok:
                    st.error(msg)
                else:
                    h = hash_password(password)
                    add_or_update_user(username, h['algorithm'], h['iterations'], h['salt'], h['hash'], role)
                    st.success(f"User {username} created/updated with role {role}.")
