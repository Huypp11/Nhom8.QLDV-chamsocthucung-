"""
Tầng 2 - MODEL: Xử lý dữ liệu hóa đơn
"""
from database.db_manager import get_connection


class InvoiceModel:

    def get_all(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT i.id, i.appointment_id, c.name as customer_name,
                   i.total_amount, i.payment_method, i.created_at
            FROM invoices i
            JOIN appointments a ON i.appointment_id = a.id
            JOIN customers c    ON a.customer_id = c.id
            ORDER BY i.created_at DESC
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_by_customer(self, customer_id):
        conn = get_connection()
        rows = conn.execute("""
            SELECT i.id, i.appointment_id, c.name as customer_name,
                   i.total_amount, i.payment_method, i.created_at
            FROM invoices i
            JOIN appointments a ON i.appointment_id = a.id
            JOIN customers c    ON a.customer_id = c.id
            WHERE a.customer_id = ?
            ORDER BY i.created_at DESC
        """, (customer_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add(self, appointment_id, total_amount, payment_method):
        conn = get_connection()
        conn.execute(
            "INSERT INTO invoices (appointment_id, total_amount, payment_method) VALUES (?, ?, ?)",
            (appointment_id, total_amount, payment_method)
        )
        conn.commit()
        conn.close()

    def get_monthly_revenue(self, year):
        conn = get_connection()
        rows = conn.execute("""
            SELECT strftime('%m', created_at) as month,
                   SUM(total_amount) as total
            FROM invoices
            WHERE strftime('%Y', created_at) = ?
            GROUP BY month ORDER BY month
        """, (str(year),)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
