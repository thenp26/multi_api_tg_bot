# database.py

import sqlite3
import logging

DATABASE_NAME = 'users.db'

def initialize_db():
    # (This function is correct and does not need changes)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            default_provider TEXT DEFAULT 'google',
            gemini_key TEXT,
            gpt_key TEXT,
            claude_key TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Database initialized successfully.")

def get_user(user_id):
    # (This function is correct and does not need changes)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        keys = ["user_id", "default_provider", "gemini_key", "gpt_key", "claude_key"]
        return dict(zip(keys, user_data))
    return None

def add_or_update_user(user_id, default_provider=None, gemini_key=None, gpt_key=None, claude_key=None):
    """Adds a new user or updates an existing one."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        # User exists, build the UPDATE query
        query = "UPDATE users SET "
        params = []
        if default_provider:
            query += "default_provider = ?, "
            params.append(default_provider)
        if gemini_key:
            query += "gemini_key = ?, "
            params.append(gemini_key)
        if gpt_key:
            query += "gpt_key = ?, "
            params.append(gpt_key)
        if claude_key:
            query += "claude_key = ?, "
            params.append(claude_key)
        
        # ✨ FIX: Only run the UPDATE command if there is something to update.
        if params:
            query = query.rstrip(', ') + " WHERE user_id = ?"
            params.append(user_id)
            cursor.execute(query, tuple(params))

    else:
        # User does not exist, INSERT them.
        cursor.execute(
            "INSERT INTO users (user_id, default_provider, gemini_key, gpt_key, claude_key) VALUES (?, ?, ?, ?, ?)",
            (user_id, 'google', gemini_key, gpt_key, claude_key)
        )
    
    conn.commit()
    conn.close()