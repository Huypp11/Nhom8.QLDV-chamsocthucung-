"""
Tầng 2 - MODEL: Xử lý dữ liệu thú cưng
"""
from database.db_manager import get_connection


class PetModel:

    def get_by_customer(self, customer_id):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM pets WHERE customer_id=? ORDER BY name",
            (customer_id,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT p.*, c.name as customer_name
            FROM pets p JOIN customers c ON p.customer_id = c.id
            ORDER BY p.name
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    def search(self, customer_id=None, keyword=""):
        conn = get_connection()
        
        query = """
            SELECT p.*, c.name as customer_name, c.phone as customer_phone
            FROM pets p JOIN customers c ON p.customer_id = c.id
            WHERE 1=1
        """
        params = []

        if customer_id and str(customer_id) != "0" and str(customer_id) != "all":
            query += " AND p.customer_id = ?"
            params.append(customer_id)

        if keyword:
            # Tìm gần đúng theo Tên khách, Số điện thoại khách HOẶC Tên thú cưng
            query += " AND (c.name LIKE ? OR c.phone LIKE ? OR p.name LIKE ?)"
            keyword_param = f"%{keyword}%"
            params.extend([keyword_param, keyword, keyword_param])

        query += " ORDER BY p.name"
        
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add(self, customer_id, name, species, breed, age):
        conn = get_connection()
        conn.execute(
            "INSERT INTO pets (customer_id, name, species, breed, age) VALUES (?, ?, ?, ?, ?)",
            (customer_id, name, species, breed, age)
        )
        conn.commit()
        conn.close()

    def update(self, pet_id, name, species, breed, age):
        conn = get_connection()
        conn.execute(
            "UPDATE pets SET name=?, species=?, breed=?, age=? WHERE id=?",
            (name, species, breed, age, pet_id)
        )
        conn.commit()
        conn.close()

    def delete(self, pet_id):
        conn = get_connection()
        conn.execute("DELETE FROM pets WHERE id=?", (pet_id,))
        conn.commit()
        conn.close()

    def count(self):
        conn = get_connection()
        count = conn.execute("SELECT COUNT(*) FROM pets").fetchone()[0]
        conn.close()
        return count
