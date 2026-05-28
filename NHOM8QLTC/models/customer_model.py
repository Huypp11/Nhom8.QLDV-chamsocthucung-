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

    def get_customer_count_by_period(self, period, year):
        formats = {
            "week": "%Y-W%W",
            "month": "%Y-%m",
            "year": "%Y",
        }
        date_format = formats.get(period, "%Y-%m")
        params = []
        where_clause = ""
        if period in ("week", "month"):
            where_clause = "WHERE strftime('%Y', created_at) = ?"
            params.append(str(year))

        conn = get_connection()
        rows = conn.execute(f"""
            SELECT strftime('{date_format}', created_at) as period,
                   COUNT(*) as total
            FROM customers
            {where_clause}
            GROUP BY period
            ORDER BY period
        """, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]
