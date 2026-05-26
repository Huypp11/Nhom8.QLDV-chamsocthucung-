from models.appointment_model import AppointmentModel
from models.customer_model import CustomerModel
from models.pet_model import PetModel
from models.service_model import ServiceModel


class AppointmentController:
    def __init__(self):
        self.model = AppointmentModel()
        self.customer_model = CustomerModel()
        self.pet_model = PetModel()
        self.service_model = ServiceModel()

    def get_by_date_range(self, date_from, date_to):
        rows = self.model.get_by_date_range(date_from, date_to)
        return rows if rows else self.model.get_all()

    def get_all(self):
        return self.model.get_all()

    def get_customers(self):
        return self.customer_model.get_all()

    def get_pets_by_customer(self, customer_id):
        return self.pet_model.get_by_customer(customer_id)

    def get_services(self):
        return self.service_model.get_all()

    def add(self, data):
        if not all([data["customer_id"], data["pet_id"], data["service_id"]]):
            return False, "Vui long chon day du thong tin!"
        self.model.add(data["customer_id"], data["pet_id"], data["service_id"], data["datetime"], data["note"])
        return True, "Da dat lich hen!"

    def complete(self, appointment_id):
        self.model.update_status(appointment_id, "Hoan thanh")
        return True, "Da danh dau hoan thanh!"

    def cancel(self, appointment_id):
        self.model.update_status(appointment_id, "Da huy")
        return True, "Da huy lich hen!"

