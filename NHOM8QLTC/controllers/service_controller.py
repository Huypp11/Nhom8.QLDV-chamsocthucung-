from models.service_model import ServiceModel


class ServiceController:
    def __init__(self):
        self.model = ServiceModel()

    def get_all(self):
        return self.model.get_all()

    def search(self, keyword):
        return self.model.search(keyword) if keyword else self.model.get_all()

    def add(self, data):
        if not data["name"]:
            return False, "Ten dich vu khong duoc de trong!"
        self.model.add(data["name"], data["description"], data["price"], data["duration"])
        return True, "Da them dich vu!"

    def update(self, service_id, data):
        if not data["name"]:
            return False, "Ten dich vu khong duoc de trong!"
        self.model.update(service_id, data["name"], data["description"], data["price"], data["duration"])
        return True, "Da cap nhat dich vu!"

    def delete(self, service_id):
        self.model.delete(service_id)
        return True, "Da xoa dich vu!"

    def get_popular(self):
        return self.model.get_popular()

