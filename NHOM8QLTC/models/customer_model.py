"""
Tầng 2 - MODEL: Xử lý dữ liệu khách hàng (truy vấn SQL)
"""
from database.db_manager import get_connection


class CustomerModel:

    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM customers ORDER BY name").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def search(self, keyword):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add(self, name, phone, email, address):
        conn = get_connection()
        conn.execute(
            "INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)",
            (name, phone, email, address)
        )
        conn.commit()
        conn.close()

    def update(self, customer_id, name, phone, email, address):
        conn = get_connection()
        conn.execute(
            "UPDATE customers SET name=?, phone=?, email=?, address=? WHERE id=?",
            (name, phone, email, address, customer_id)
        )
        conn.commit()
        conn.close()

    def delete(self, customer_id):
        conn = get_connection()
        conn.execute("DELETE FROM customers WHERE id=?", (customer_id,))
        conn.commit()
        conn.close()

    def get_by_id(self, customer_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM customers WHERE id=?", (customer_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def count(self):
        conn = get_connection()
        count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        conn.close()
        return count
