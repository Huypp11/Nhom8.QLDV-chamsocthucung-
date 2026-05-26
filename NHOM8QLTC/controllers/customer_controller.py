from models.customer_model import CustomerModel


class CustomerController:
    def __init__(self):
        self.model = CustomerModel()

    def get_all(self):
        return self.model.get_all()

    def search(self, keyword):
        return self.model.search(keyword) if keyword else self.model.get_all()

    def get_by_id(self, customer_id):
        return self.model.get_by_id(customer_id)

    def add(self, data):
        if not data["name"]:
            return False, "Ten khach hang khong duoc de trong!"
        self.model.add(data["name"], data["phone"], data["email"], data["address"])
        return True, "Da them khach hang!"

    def update(self, customer_id, data):
        if not data["name"]:
            return False, "Ten khach hang khong duoc de trong!"
        self.model.update(customer_id, data["name"], data["phone"], data["email"], data["address"])
        return True, "Da cap nhat khach hang!"

    def delete(self, customer_id):
        self.model.delete(customer_id)
        return True, "Da xoa khach hang!"

