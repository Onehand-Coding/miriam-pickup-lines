import sqlite3
import json
import random
from datetime import datetime
from pathlib import Path

from .config import PROJECT_ROOT

QUOTES_JSON = PROJECT_ROOT / "data" / "punch_line.json"


class MiriamDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            # Create database in user's home directory
            home_dir = PROJECT_ROOT
            db_dir = home_dir / "data"
            db_dir.mkdir(exist_ok=True)
            self.db_path = db_dir / "miriam_quotes.db"
        else:
            self.db_path = Path(db_path)

        self.init_database()
        self.populate_initial_data()

    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY,
                    category TEXT NOT NULL,
                    type TEXT NOT NULL,
                    setup TEXT,
                    punchline TEXT NOT NULL,
                    source TEXT,
                    difficulty_level INTEGER,
                    tags TEXT,
                    used_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def populate_initial_data(self):
        """Populate database with initial quotes if empty"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM quotes")
            count = cursor.fetchone()[0]

            if count == 0:
                # Insert the JSON data
                quotes_data = self.get_initial_quotes(QUOTES_JSON)
                for quote in quotes_data:
                    cursor.execute(
                        """
                        INSERT INTO quotes
                        (id, category, type, setup, punchline, source, difficulty_level, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            quote["id"],
                            quote["category"],
                            quote["type"],
                            quote.get("setup", ""),
                            quote["punchline"],
                            quote.get("source", ""),
                            quote.get("difficulty_level", 5),
                            ",".join(quote.get("tags", [])),
                        ),
                    )
                conn.commit()

    def get_unused_quote(self, category=None, max_difficulty=10):
        """Get a random unused quote, optionally filtered by category and difficulty"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = "SELECT * FROM quotes WHERE used_count = 0"
            params = []

            if category:
                query += " AND category = ?"
                params.append(category)

            query += " AND difficulty_level <= ?"
            params.append(max_difficulty)

            cursor.execute(query, params)
            quotes = cursor.fetchall()

            if not quotes:
                # If no unused quotes, reset all and try again
                self.reset_usage()
                cursor.execute(query, params)
                quotes = cursor.fetchall()

            return dict(random.choice(quotes)) if quotes else None

    def mark_as_used(self, quote_id):
        """Mark a quote as used"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE quotes
                SET used_count = used_count + 1, last_used = ?
                WHERE id = ?
            """,
                (datetime.now(), quote_id),
            )
            conn.commit()

    def reset_usage(self):
        """Reset usage count for all quotes"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE quotes SET used_count = 0, last_used = NULL")
            conn.commit()

    def get_stats(self):
        """Get usage statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM quotes")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM quotes WHERE used_count > 0")
            used = cursor.fetchone()[0]

            cursor.execute("SELECT category, COUNT(*) FROM quotes GROUP BY category")
            by_category = dict(cursor.fetchall())

            return {
                "total": total,
                "used": used,
                "unused": total - used,
                "by_category": by_category,
            }

    def get_initial_quotes(self, quotes_json, key="miriam_quotes"):
        """Return the complete initial quotes data from Miriam's book or any json source."""
        with open(quotes_json, "r") as f:
            return json.load(f).get(key, [])
