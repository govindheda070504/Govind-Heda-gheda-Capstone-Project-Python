import sqlite3
from typing import List, Dict, Optional, Any

# Database manager class for SQLite CRUD operations
class BookDatabaseManager:

    def __init__(self, db_name: str = "books.db"):
        self.db_name = db_name
        self.create_table()

    # Get connection with dict-like row access
    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    # Create books table if not exists.
    def create_table(self) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    price REAL NOT NULL,
                    in_stock BOOLEAN NOT NULL,
                    rating INTEGER NOT NULL
                )
            """
            )
            conn.commit()

    # Insert a new book record
    def create_book(
        self, title: str, price: float, in_stock: bool, rating: int
    ) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO books (title, price, in_stock, rating)
                VALUES (?, ?, ?, ?)
            """,
                (title, price, int(in_stock), rating),
            )
            conn.commit()
            book_id = cursor.lastrowid
            return self.get_book_by_id(book_id)

    # Retrieve all book records
    def get_all_books(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "title": row["title"],
                    "price": row["price"],
                    "in_stock": bool(row["in_stock"]),
                    "rating": row["rating"],
                }
                for row in rows
            ]

    # Retrieve a single book record by ID
    def get_book_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "title": row["title"],
                    "price": row["price"],
                    "in_stock": bool(row["in_stock"]),
                    "rating": row["rating"],
                }
            return None

    # Update an existing book record
    def update_book(
        self,
        book_id: int,
        title: Optional[str] = None,
        price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        rating: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        current_book = self.get_book_by_id(book_id)
        if not current_book:
            return None

        new_title = title if title is not None else current_book["title"]
        new_price = price if price is not None else current_book["price"]
        new_in_stock = in_stock if in_stock is not None else current_book["in_stock"]
        new_rating = rating if rating is not None else current_book["rating"]

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE books
                SET title = ?, price = ?, in_stock = ?, rating = ?
                WHERE id = ?
            """,
                (new_title, new_price, int(new_in_stock), new_rating, book_id),
            )
            conn.commit()
            return self.get_book_by_id(book_id)

    # Delete a book record by ID
    def delete_book(self, book_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            return cursor.rowcount > 0
