"""
Tầng 2 - MODEL: Xử lý dữ liệu lịch hẹn
"""
from database.db_manager import get_connection


class AppointmentModel:

    def get_by_date_range(self, date_from, date_to):
        conn = get_connection()
        rows = conn.execute("""
            SELECT a.id, a.customer_id, a.pet_id,
                   c.name as customer_name, c.phone as customer_phone,
                   p.name as pet_name, p.species as pet_species,
                   s.name as service_name, a.datetime, a.status, a.note
            FROM appointments a
            JOIN customers c ON a.customer_id = c.id
            JOIN pets p      ON a.pet_id = p.id
            JOIN services s  ON a.service_id = s.id
            WHERE DATE(a.datetime) BETWEEN ? AND ?
            ORDER BY a.datetime
        """, (date_from, date_to)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT a.id, a.customer_id, a.pet_id,
                   c.name as customer_name, c.phone as customer_phone,
                   p.name as pet_name, p.species as pet_species,
                   s.name as service_name, a.datetime, a.status, a.note
            FROM appointments a
            JOIN customers c ON a.customer_id = c.id
            JOIN pets p      ON a.pet_id = p.id
            JOIN services s  ON a.service_id = s.id
            ORDER BY a.datetime DESC
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    
    def search(self, date_from=None, date_to=None, keyword=""):
        conn = get_connection()
        
        query = """
            SELECT a.id, a.customer_id, a.pet_id,
                   c.name as customer_name, c.phone as customer_phone,
                   p.name as pet_name, p.species as pet_species,
                   s.name as service_name, a.datetime, a.status, a.note
            FROM appointments a
            JOIN customers c ON a.customer_id = c.id
            JOIN pets p      ON a.pet_id = p.id
            JOIN services s  ON a.service_id = s.id
            WHERE 1=1
        """
        params = []

        # 1. Lọc theo khoảng ngày (Nếu người dùng có chọn ngày)
        if date_from and date_to:
            query += " AND DATE(a.datetime) BETWEEN ? AND ?"
            params.extend([
                
                f"{date_from} 00:00:00",
                f"{date_to} 23:59:59"
                
                ])

        # 2. Lọc theo từ khóa (Tìm theo Tên khách, SĐT khách, hoặc Tên thú cưng)
        if keyword:
            query += " AND (c.name LIKE ? OR c.phone = ? OR p.name LIKE ?)"
            k = f"%{keyword}%"
            params.extend([k, keyword, k])

        # Sắp xếp lịch hẹn mới nhất lên đầu
        query += " ORDER BY a.datetime DESC"
        
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add(self, customer_id, pet_id, service_id, datetime_str, note=""):
        conn = get_connection()
        conn.execute(
            "INSERT INTO appointments (customer_id, pet_id, service_id, datetime, note) VALUES (?, ?, ?, ?, ?)",
            (customer_id, pet_id, service_id, datetime_str, note)
        )
        conn.commit()
        conn.close()

    def update_status(self, appointment_id, status):
        conn = get_connection()
        conn.execute(
            "UPDATE appointments SET status=? WHERE id=?",
            (status, appointment_id)
        )
        conn.commit()
        conn.close()

    def delete(self, appointment_id):
        conn = get_connection()
        conn.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
        conn.commit()
        conn.close()

    def count(self):
        conn = get_connection()
        count = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
        conn.close()
        return count
