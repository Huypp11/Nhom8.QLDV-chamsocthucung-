"""
Tầng 2 - MODEL: Xử lý dữ liệu người dùng
"""
from database.db_manager import get_connection, hash_password


class UserModel:

    def login(self, username: str, password: str):
        """
        Kiểm tra đăng nhập.
        Trả về dict user nếu đúng, None nếu sai.
        """
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password))
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_all(self):
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, username, full_name, role, created_at FROM users ORDER BY role, full_name"
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add(self, username: str, password: str, full_name: str, role: str):
        """Tạo tài khoản mới. Trả về True nếu thành công, False nếu username trùng."""
        try:
            conn = get_connection()
            conn.execute(
                "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
                (username, hash_password(password), full_name, role)
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    def update_password(self, user_id: int, new_password: str):
        conn = get_connection()
        conn.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hash_password(new_password), user_id)
        )
        conn.commit()
        conn.close()

    def update(self, user_id: int, full_name: str, role: str):
        conn = get_connection()
        conn.execute(
            "UPDATE users SET full_name = ?, role = ? WHERE id = ?",
            (full_name, role, user_id)
        )
        conn.commit()
        conn.close()

    def delete(self, user_id: int):
        """Xóa tài khoản (không cho xóa admin cuối cùng)"""
        conn = get_connection()
        # Kiểm tra còn ít nhất 1 admin
        admin_count = conn.execute(
            "SELECT COUNT(*) FROM users WHERE role = 'admin'"
        ).fetchone()[0]
        current_role = conn.execute(
            "SELECT role FROM users WHERE id = ?", (user_id,)
        ).fetchone()

        if current_role and current_role[0] == "admin" and admin_count <= 1:
            conn.close()
            return False  # Không cho xóa admin cuối

        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True

    def username_exists(self, username: str) -> bool:
        conn = get_connection()
        row = conn.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        return row is not None