# card_operations.py
import sqlite3
from rapidfuzz import fuzz

def add_card(user_id, content):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('INSERT INTO cards (user_id, content) VALUES (?, ?)', (user_id, content))
    conn.commit()
    conn.close()

def get_all_cards(user_id, limit=100):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    if limit is None:
        c.execute('SELECT id, content FROM cards WHERE user_id = ? ORDER BY id DESC', (user_id,))
    else:
        c.execute('SELECT id, content FROM cards WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
    cards = c.fetchall()
    conn.close()
    return cards

def delete_card(card_id, user_id):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('DELETE FROM cards WHERE id = ? AND user_id = ?', (card_id, user_id))
    conn.commit()
    conn.close()

def search_cards(user_id, query, threshold=70):
    all_cards = get_all_cards(user_id, limit=None)
    matched_cards = []
    query = query.lower()
    for card in all_cards:
        card_content = card[1].lower()
        score = fuzz.partial_ratio(query, card_content)
        if score >= threshold:
            matched_cards.append((card[0], card[1]))
    return matched_cards

def update_card(card_id, user_id, content):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('UPDATE cards SET content = ? WHERE id = ? AND user_id = ?', (content, card_id, user_id))
    conn.commit()
    conn.close()

def get_card(card_id, user_id):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('SELECT * FROM cards WHERE id = ? AND user_id = ?', (card_id, user_id))
    card = c.fetchone()
    conn.close()
    return card
