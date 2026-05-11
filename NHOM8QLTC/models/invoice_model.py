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
        """Tạo hóa đơn đơn giản (không có invoice_items) - giữ tương thích cũ"""
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO invoices (appointment_id, total_amount, payment_method) VALUES (?, ?, ?)",
            (appointment_id, total_amount, payment_method)
        )
        invoice_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return invoice_id

    def add_full(self, appointment_id, payment_method, items):
        """
        Tạo hóa đơn kèm danh sách items (dịch vụ + sản phẩm).

        items: list of dict, mỗi dict gồm:
            - item_type  : 'service' hoặc 'product'
            - item_id    : id của dịch vụ / sản phẩm
            - item_name  : tên hiển thị
            - quantity   : số lượng
            - unit_price : đơn giá
        """
        total = sum(it["quantity"] * it["unit_price"] for it in items)
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO invoices (appointment_id, total_amount, payment_method) VALUES (?, ?, ?)",
            (appointment_id, total, payment_method)
        )
        invoice_id = cursor.lastrowid

        for it in items:
            conn.execute(
                """INSERT INTO invoice_items
                       (invoice_id, item_type, item_id, item_name, quantity, unit_price)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (invoice_id, it["item_type"], it["item_id"],
                 it["item_name"], it["quantity"], it["unit_price"])
            )

        conn.commit()
        conn.close()
        return invoice_id

    def get_items(self, invoice_id):
        """Lấy danh sách các dòng trong hóa đơn"""
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM invoice_items WHERE invoice_id = ? ORDER BY item_type, id",
            (invoice_id,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

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