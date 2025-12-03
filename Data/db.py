import os
import sqlite3
import hashlib
from typing import List, Tuple, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db(seed_books: Optional[List[Tuple]] = None):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        year INTEGER,
        category TEXT,
        description TEXT
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS borrows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        returned_at TIMESTAMP,
        due_date TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(book_id) REFERENCES books(id)
    )
    """
    )

    conn.commit()

    cur.execute("PRAGMA table_info(borrows)")
    cols = [r[1] for r in cur.fetchall()]
    if "due_date" not in cols:
        try:
            cur.execute("ALTER TABLE borrows ADD COLUMN due_date TIMESTAMP")
            conn.commit()
        except Exception:
            pass

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, book_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(book_id) REFERENCES books(id)
    )
    """
    )

    conn.commit()

    if seed_books:
        cur.executemany(
            "INSERT INTO books (title, author, year, category, description) VALUES (?, ?, ?, ?, ?)",
            seed_books,
        )
        conn.commit()

    conn.close()


def user_create(username: str, password: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        conn.commit()
        uid = cur.lastrowid
    except sqlite3.IntegrityError:
        uid = 0
    conn.close()
    return uid


def user_get(username: str) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?", (username,)
    )
    row = cur.fetchone()
    conn.close()
    return row


def user_verify(username: str, password: str) -> Optional[int]:
    row = user_get(username)
    if not row:
        return None
    uid, uname, password_hash = row
    if hashlib.sha256(password.encode("utf-8")).hexdigest() == password_hash:
        return uid
    return None


def books_all() -> List[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, author, year, category, description FROM books ORDER BY title"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def add_book(
    title: str, author: str, year: int, category: str, description: str = ""
) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (title, author, year, category, description) VALUES (?, ?, ?, ?, ?)",
        (title, author, year, category, description),
    )
    conn.commit()
    bid = cur.lastrowid
    conn.close()
    return bid


def books_search(query: str) -> List[Tuple]:
    like = f"%{query}%"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, author, year, category, description FROM books WHERE title LIKE ? OR author LIKE ? OR category LIKE ? ORDER BY title",
        (like, like, like),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def borrow_book(user_id: int, book_id: int, days: int = 14) -> int:
    conn = get_conn()
    cur = conn.cursor()
    modifier = f"+{int(days)} days"
    cur.execute(
        "INSERT INTO borrows (user_id, book_id, due_date) VALUES (?, ?, datetime('now', ?))",
        (user_id, book_id, modifier),
    )
    conn.commit()
    bid = cur.lastrowid
    conn.close()
    return bid


def return_book(user_id: int, book_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM borrows WHERE user_id = ? AND book_id = ? AND returned_at IS NULL ORDER BY borrowed_at DESC",
        (user_id, book_id),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    borrow_id = row[0]
    cur.execute(
        "UPDATE borrows SET returned_at = CURRENT_TIMESTAMP WHERE id = ?", (borrow_id,)
    )
    conn.commit()
    conn.close()
    return True


def borrowed_by_user(user_id: int) -> List[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT b.id, b.title, b.author, b.year, b.category, br.borrowed_at, br.due_date, br.returned_at FROM borrows br JOIN books b ON br.book_id = b.id WHERE br.user_id = ? ORDER BY br.borrowed_at DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def favorites_add(user_id: int, book_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT OR IGNORE INTO favorites (user_id, book_id) VALUES (?, ?)",
            (user_id, book_id),
        )
        conn.commit()
        ok = cur.rowcount > 0
    except Exception:
        ok = False
    conn.close()
    return ok


def favorites_remove(user_id: int, book_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM favorites WHERE user_id = ? AND book_id = ?", (user_id, book_id)
    )
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed > 0


def favorites_by_user(user_id: int) -> List[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT b.id, b.title, b.author, b.year, b.category, f.added_at FROM favorites f JOIN books b ON f.book_id = b.id WHERE f.user_id = ? ORDER BY f.added_at DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def book_delete(book_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed > 0


def db_exists() -> bool:
    return os.path.exists(DB_PATH)
