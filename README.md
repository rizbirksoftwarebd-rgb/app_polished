# Multi-Tasker — Polished Streamlit App (Render-ready DB)

This polished project:
- Uses SQLAlchemy to connect to `DATABASE_URL` (if you attach a managed DB on Render, set DATABASE_URL).
- Falls back to `sqlite:///app.db` when DATABASE_URL isn't provided.
- `ensure_db.py` auto-creates the users table and any missing schema on startup.
- Simple hashed-password auth (PBKDF2); admin console allows creating users from the UI.
- Polished UI with animations and icons-like styles.

## Quick start (local)
1. Create venv and install:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Initialize DB (optional — app will auto-init on start):
   ```bash
   python ensure_db.py
   ```
3. Create admin user:
   ```bash
   python create_user.py
   ```
4. Run locally:
   ```bash
   streamlit run main.py
   ```

## Deploy to Render
- Create a Web Service, connect your GitHub repo, and add a managed database (Postgres).
- Set `DATABASE_URL` in Render's environment variables (Render may provide a `RENDER_DATABASE_URL` environment variable).
- Render will run `streamlit run main.py --server.port $PORT` as in `render.yaml`.

