"""
Tầng 2 - MODEL: Xử lý dữ liệu dịch vụ
"""
from database.db_manager import get_connection


class ServiceModel:

    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM services ORDER BY name").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def search(self, keyword):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT * FROM services
            WHERE name LIKE ? OR description LIKE ? OR species_category LIKE ?
            ORDER BY name
            """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_by_species(self, species):
        conn = get_connection()
        rows = conn.execute("""
            SELECT * FROM services
            WHERE species_category = ?
               OR species_category = 'Tat ca'
               OR species_category IS NULL
               OR TRIM(species_category) = ''
            ORDER BY name
        """, (species or "",)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add(self, name, description, price, duration, species_category):
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO services (name, description, price, duration, species_category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, description, price, duration, species_category)
        )
        conn.commit()
        conn.close()

    def update(self, service_id, name, description, price, duration, species_category):
        conn = get_connection()
        conn.execute(
            """
            UPDATE services
            SET name=?, description=?, price=?, duration=?, species_category=?
            WHERE id=?
            """,
            (name, description, price, duration, species_category, service_id)
        )
        conn.commit()
        conn.close()

    def delete(self, service_id):
        conn = get_connection()
        conn.execute("DELETE FROM services WHERE id=?", (service_id,))
        conn.commit()
        conn.close()

    def get_popular(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT s.name, COUNT(a.id) as count
            FROM services s LEFT JOIN appointments a ON s.id = a.service_id
            GROUP BY s.id ORDER BY count DESC LIMIT 10
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]
