from models.customer_model import CustomerModel
from models.pet_model import PetModel


class PetController:
    def __init__(self):
        self.model = PetModel()
        self.customer_model = CustomerModel()

    def get_customers(self):
        return self.customer_model.get_all()

    def get_pets(self, customer_id=None):
        return self.model.get_by_customer(customer_id) if customer_id else self.model.get_all()

    def add(self, customer_id, data):
        if not customer_id:
            return False, "Vui long chon khach hang truoc!"
        if not data["name"]:
            return False, "Ten thu cung khong duoc de trong!"
        self.model.add(customer_id, data["name"], data["species"], data["breed"], data["age"])
        return True, "Da them thu cung!"

    def update(self, pet_id, data):
        if not data["name"]:
            return False, "Ten thu cung khong duoc de trong!"
        self.model.update(pet_id, data["name"], data["species"], data["breed"], data["age"])
        return True, "Da cap nhat thu cung!"

    def delete(self, pet_id):
        self.model.delete(pet_id)
        return True, "Da xoa thu cung!"

