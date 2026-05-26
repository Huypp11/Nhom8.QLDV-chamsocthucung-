from models.user_model import UserModel


class UserController:
    def __init__(self):
        self.model = UserModel()

    def get_all(self):
        return self.model.get_all()

    def username_exists(self, username):
        return self.model.username_exists(username)

    def login(self, username, password):
        if not username or not password:
            return False, "Vui long nhap day du thong tin!", None
        user = self.model.login(username, password)
        if not user:
            return False, "Ten dang nhap hoac mat khau khong dung!", None
        return True, "", user

    def register_employee(self, full_name, username, password, confirm):
        if not full_name or not username or not password or not confirm:
            return False, "Vui long nhap day du thong tin!"
        if password != confirm:
            return False, "Mat khau khong khop!"
        if len(password) < 6:
            return False, "Mat khau phai it nhat 6 ky tu!"
        if not self.model.add(username, password, full_name, "nhanvien"):
            return False, "Ten dang nhap da ton tai!"
        return True, "Dang ky thanh cong!"

    def add(self, data):
        if not data["username"] or not data["password"] or not data["full_name"]:
            return False, "Vui long nhap day du thong tin!"
        if self.model.username_exists(data["username"]):
            return False, f"Ten dang nhap '{data['username']}' da ton tai!"
        self.model.add(data["username"], data["password"], data["full_name"], data["role"])
        return True, "Da tao tai khoan!"

    def update_password(self, user_id, new_password):
        if not new_password:
            return False, "Mat khau khong duoc de trong!"
        self.model.update_password(user_id, new_password)
        return True, "Da doi mat khau!"

    def delete(self, user_id):
        if not self.model.delete(user_id):
            return False, "Khong the xoa admin cuoi cung trong he thong!"
        return True, "Da xoa tai khoan!"
