"""
Tầng 1 - DATABASE: Kết nối và khởi tạo SQLite
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "pet_shop.db")


def get_connection():
    """Lấy kết nối database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Trả về dict thay vì tuple
    return conn


def init_db():
    """Khởi tạo toàn bộ bảng database"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            phone       TEXT,
            email       TEXT,
            address     TEXT,
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS pets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            name        TEXT NOT NULL,
            species     TEXT,
            breed       TEXT,
            age         INTEGER,
            created_at  TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        CREATE TABLE IF NOT EXISTS services (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT,
            price       REAL NOT NULL DEFAULT 0,
            duration    INTEGER DEFAULT 30
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            pet_id      INTEGER NOT NULL,
            service_id  INTEGER NOT NULL,
            datetime    TEXT NOT NULL,
            status      TEXT DEFAULT 'Chờ xử lý',
            note        TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (pet_id)      REFERENCES pets(id),
            FOREIGN KEY (service_id)  REFERENCES services(id)
        );

        CREATE TABLE IF NOT EXISTS invoices (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER NOT NULL,
            total_amount   REAL NOT NULL DEFAULT 0,
            payment_method TEXT DEFAULT 'Tiền mặt',
            created_at     TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (appointment_id) REFERENCES appointments(id)
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Database đã khởi tạo thành công!")
