"""
Tầng 2 - MODEL: Xử lý dữ liệu sản phẩm
"""
from database.db_manager import get_connection


class ProductModel:

    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM products ORDER BY category, name").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def search(self, keyword):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM products WHERE name LIKE ? OR description LIKE ? OR category LIKE ?",
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add(self, name, description, price, category, stock):
        conn = get_connection()
        conn.execute(
            "INSERT INTO products (name, description, price, category, stock) VALUES (?, ?, ?, ?, ?)",
            (name, description, price, category, stock)
        )
        conn.commit()
        conn.close()

    def update(self, product_id, name, description, price, category, stock):
        conn = get_connection()
        conn.execute(
            "UPDATE products SET name=?, description=?, price=?, category=?, stock=? WHERE id=?",
            (name, description, price, category, stock, product_id)
        )
        conn.commit()
        conn.close()

    def delete(self, product_id):
        conn = get_connection()
        conn.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()

    def get_by_id(self, product_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_categories(self):
        conn = get_connection()
        rows = conn.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
        conn.close()
        return [r["category"] for r in rows]