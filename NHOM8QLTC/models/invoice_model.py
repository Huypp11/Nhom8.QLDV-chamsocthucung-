"""
Tầng 2 - MODEL: Xử lý dữ liệu hóa đơn
"""
from database.db_manager import get_connection


class InvoiceModel:

    def get_all(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT i.id, i.appointment_id,
                   COALESCE(ca.name, cd.name, 'Khach le') as customer_name,
                   i.total_amount, i.payment_method, i.created_at
            FROM invoices i
            LEFT JOIN appointments a ON i.appointment_id = a.id
            LEFT JOIN customers ca   ON a.customer_id = ca.id
            LEFT JOIN customers cd   ON i.customer_id = cd.id
            ORDER BY i.created_at DESC
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_by_customer(self, customer_id):
        conn = get_connection()
        rows = conn.execute("""
            SELECT i.id, i.appointment_id,
                   COALESCE(ca.name, cd.name, 'Khach le') as customer_name,
                   i.total_amount, i.payment_method, i.created_at
            FROM invoices i
            LEFT JOIN appointments a ON i.appointment_id = a.id
            LEFT JOIN customers ca   ON a.customer_id = ca.id
            LEFT JOIN customers cd   ON i.customer_id = cd.id
            WHERE COALESCE(a.customer_id, i.customer_id) = ?
            ORDER BY i.created_at DESC
        """, (customer_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def search_by_customer(self, keyword):
        conn = get_connection()
        rows = conn.execute("""
            SELECT i.id, i.appointment_id,
                   COALESCE(ca.name, cd.name, 'Khach le') as customer_name,
                   i.total_amount, i.payment_method, i.created_at
            FROM invoices i
            LEFT JOIN appointments a ON i.appointment_id = a.id
            LEFT JOIN customers ca   ON a.customer_id = ca.id
            LEFT JOIN customers cd   ON i.customer_id = cd.id
            WHERE ca.name LIKE ? OR ca.phone LIKE ?
               OR cd.name LIKE ? OR cd.phone LIKE ?
            ORDER BY i.created_at DESC
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")).fetchall()
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

    def add_full(self, appointment_id, payment_method, items, customer_id=None):
        """
        Tạo hóa đơn kèm danh sách items (dịch vụ + sản phẩm).

        items: list of dict, mỗi dict gồm:
            - item_type  : 'service' hoặc 'product'
            - item_id    : id của dịch vụ / sản phẩm
            - item_name  : tên hiển thị
            - quantity   : số lượng
            - unit_price : đơn giá
        """
        conn = get_connection()
        try:
            product_quantities = {}
            for it in items:
                if it["item_type"] == "product":
                    product_quantities[it["item_id"]] = (
                        product_quantities.get(it["item_id"], 0) + it["quantity"]
                    )

            for product_id, quantity in product_quantities.items():
                row = conn.execute(
                    "SELECT name, stock FROM products WHERE id = ?",
                    (product_id,)
                ).fetchone()
                if row is None:
                    raise ValueError(f"San pham ID {product_id} khong ton tai.")
                if row["stock"] < quantity:
                    raise ValueError(
                        f"San pham '{row['name']}' chi con {row['stock']} trong kho, "
                        f"khong du de ban {quantity}."
                    )

            total = sum(it["quantity"] * it["unit_price"] for it in items)
            cursor = conn.execute(
                """
                INSERT INTO invoices (appointment_id, customer_id, total_amount, payment_method)
                VALUES (?, ?, ?, ?)
                """,
                (appointment_id, customer_id, total, payment_method)
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
                if it["item_type"] == "product":
                    conn.execute(
                        "UPDATE products SET stock = stock - ? WHERE id = ?",
                        (it["quantity"], it["item_id"])
                    )

            conn.commit()
            return invoice_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

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
