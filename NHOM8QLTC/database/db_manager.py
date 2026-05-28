"""
Tang database: ket noi va khoi tao SQLite.
"""
import hashlib
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "pet_shop.db")


def hash_password(password: str) -> str:
    """Hash mat khau truoc khi luu vao database."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection():
    """Lay ket noi database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Khoi tao toan bo bang database."""
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
            duration    INTEGER DEFAULT 30,
            species_category TEXT DEFAULT 'Tat ca'
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
            appointment_id INTEGER,
            customer_id     INTEGER,
            total_amount   REAL NOT NULL DEFAULT 0,
            payment_method TEXT DEFAULT 'Tiền mặt',
            created_at     TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (appointment_id) REFERENCES appointments(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT,
            price       REAL NOT NULL DEFAULT 0,
            category    TEXT DEFAULT 'Khác',
            stock       INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS invoice_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id  INTEGER NOT NULL,
            item_type   TEXT NOT NULL CHECK(item_type IN ('service', 'product')),
            item_id     INTEGER NOT NULL,
            item_name   TEXT NOT NULL,
            quantity    INTEGER NOT NULL DEFAULT 1,
            unit_price  REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id)
        );

        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL UNIQUE,
            password    TEXT NOT NULL,
            full_name   TEXT NOT NULL,
            role        TEXT NOT NULL DEFAULT 'nhanvien'
                        CHECK(role IN ('admin', 'nhanvien')),
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        );
    """)

    _migrate_invoices_table(cursor)
    _migrate_services_table(cursor)

    admin_exists = cursor.execute(
        "SELECT 1 FROM users WHERE role = 'admin' LIMIT 1"
    ).fetchone()
    if not admin_exists:
        cursor.execute(
            """
            INSERT INTO users (username, password, full_name, role)
            VALUES (?, ?, ?, ?)
            """,
            ("admin", hash_password("admin123"), "Quan tri vien", "admin"),
        )

    conn.commit()
    conn.close()
    print("Database khởi tạo thành công rồi hehe!")


def _migrate_invoices_table(cursor):
    """Cho phep hoa don truc tiep khong can lich hen."""
    columns = cursor.execute("PRAGMA table_info(invoices)").fetchall()
    if not columns:
        return

    has_customer_id = any(col["name"] == "customer_id" for col in columns)
    appointment_col = next((col for col in columns if col["name"] == "appointment_id"), None)
    appointment_not_null = bool(appointment_col and appointment_col["notnull"])
    if has_customer_id and not appointment_not_null:
        return

    cursor.executescript("""
        CREATE TABLE invoices_new (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER,
            customer_id     INTEGER,
            total_amount   REAL NOT NULL DEFAULT 0,
            payment_method TEXT DEFAULT 'Tien mat',
            created_at     TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (appointment_id) REFERENCES appointments(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        INSERT INTO invoices_new (id, appointment_id, customer_id, total_amount, payment_method, created_at)
        SELECT i.id,
               i.appointment_id,
               a.customer_id,
               i.total_amount,
               i.payment_method,
               i.created_at
        FROM invoices i
        LEFT JOIN appointments a ON i.appointment_id = a.id;

        DROP TABLE invoices;
        ALTER TABLE invoices_new RENAME TO invoices;
    """)


def _migrate_services_table(cursor):
    """Them danh muc loai thu cung cho dich vu neu database da co san."""
    columns = cursor.execute("PRAGMA table_info(services)").fetchall()
    if not columns:
        return

    has_species_category = any(col["name"] == "species_category" for col in columns)
    if not has_species_category:
        cursor.execute(
            "ALTER TABLE services ADD COLUMN species_category TEXT DEFAULT 'Tat ca'"
        )
