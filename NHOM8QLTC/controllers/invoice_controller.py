from models.appointment_model import AppointmentModel
from models.customer_model import CustomerModel
from models.invoice_model import InvoiceModel
from models.Product_model import ProductModel
from models.service_model import ServiceModel


class InvoiceController:
    def __init__(self):
        self.model = InvoiceModel()
        self.customer_model = CustomerModel()
        self.appointment_model = AppointmentModel()
        self.product_model = ProductModel()
        self.service_model = ServiceModel()

    def get_customers(self):
        return self.customer_model.get_all()

    def get_appointments(self):
        return self.appointment_model.get_all()

    def get_services(self):
        return self.service_model.get_all()

    def get_products(self):
        return self.product_model.get_all()

    def get_invoices(self, customer_id=None, keyword=""):
        if keyword:
            return self.model.search_by_customer(keyword)
        return self.model.get_by_customer(customer_id) if customer_id else self.model.get_all()

    def create(self, data):
        if not data["appointment_id"] and not data["customer_id"]:
            return False, "Vui long chon lich hen hoac khach hang truc tiep!", None
        if not data["items"]:
            return False, "Hoa don phai co it nhat 1 dich vu hoac san pham!", None
        invoice_id = self.model.add_full(
            data["appointment_id"],
            data["payment_method"],
            data["items"],
            data["customer_id"],
        )
        return True, f"Da tao hoa don #{invoice_id} thanh cong!", invoice_id

    def get_items(self, invoice_id):
        return self.model.get_items(invoice_id)

    def get_monthly_revenue(self, year):
        return self.model.get_monthly_revenue(year)

