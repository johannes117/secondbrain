# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS users
              (id INTEGER PRIMARY KEY, 
              username TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL,
              session_token TEXT)
              ''')
    c.execute('''
              CREATE TABLE IF NOT EXISTS cards
              (id INTEGER PRIMARY KEY, 
              user_id INTEGER NOT NULL,
              content TEXT NOT NULL,
              FOREIGN KEY (user_id) REFERENCES users (id))
              ''')
    conn.commit()
    conn.close()
