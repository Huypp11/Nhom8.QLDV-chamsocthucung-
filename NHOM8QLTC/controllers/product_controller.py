from models.Product_model import ProductModel


class ProductController:
    def __init__(self):
        self.model = ProductModel()

    def get_all(self):
        return self.model.get_all()

    def search(self, keyword):
        return self.model.search(keyword) if keyword else self.model.get_all()

    def get_by_id(self, product_id):
        return self.model.get_by_id(product_id)

    def add(self, data):
        if not data["name"]:
            return False, "Ten san pham khong duoc de trong!"
        self.model.add(data["name"], data["description"], data["price"], data["category"], data["stock"])
        return True, "Da them san pham!"

    def update(self, product_id, data):
        if not data["name"]:
            return False, "Ten san pham khong duoc de trong!"
        self.model.update(product_id, data["name"], data["description"], data["price"], data["category"], data["stock"])
        return True, "Da cap nhat san pham!"

    def delete(self, product_id):
        self.model.delete(product_id)
        return True, "Da xoa san pham!"

