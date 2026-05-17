"""
Tầng 2 - MODEL: Xử lý dữ liệu lịch hẹn
"""
from database.db_manager import get_connection


class AppointmentModel:

    def get_by_date_range(self, date_from, date_to):
        conn = get_connection()
        rows = conn.execute("""
            SELECT a.id, c.name as customer_name, c.phone as customer_phone,
                   p.name as pet_name,
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
            SELECT a.id, c.name as customer_name, c.phone as customer_phone,
                   p.name as pet_name,
                   s.name as service_name, a.datetime, a.status, a.note
            FROM appointments a
            JOIN customers c ON a.customer_id = c.id
            JOIN pets p      ON a.pet_id = p.id
            JOIN services s  ON a.service_id = s.id
            ORDER BY a.datetime DESC
        """).fetchall()
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
