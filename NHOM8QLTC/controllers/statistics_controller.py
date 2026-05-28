from models.appointment_model import AppointmentModel
from models.customer_model import CustomerModel
from models.invoice_model import InvoiceModel
from models.pet_model import PetModel
from models.service_model import ServiceModel


class StatisticsController:
    def get_summary(self):
        return {
            "customers": CustomerModel().count(),
            "pets": PetModel().count(),
            "appointments": AppointmentModel().count(),
        }

    def get_monthly_revenue(self, year):
        return InvoiceModel().get_monthly_revenue(year)

    def get_revenue_by_period(self, period, year):
        return InvoiceModel().get_revenue_by_period(period, year)

    def get_popular_services(self):
        return ServiceModel().get_popular()

    def get_customer_count_by_period(self, period, year):
        return CustomerModel().get_customer_count_by_period(period, year)

    def get_products_sold(self, year):
        return InvoiceModel().get_products_sold(year)

    def get_products_sold_by_period(self, period, year):
        return InvoiceModel().get_products_sold_by_period(period, year)
