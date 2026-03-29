from .interfaces import ICustomerRepository
from ..models import Customer, db


class SqlAlchemyCustomerRepository(ICustomerRepository):
    def list_customers(self):
        return Customer.query.order_by(Customer.id.asc()).all()

    def get_customer(self, customer_id: int):
        return db.session.get(Customer, customer_id)

    def add_customer(self, customer) -> None:
        db.session.add(customer)
        self._commit()

    def update_customer(self, customer) -> None:
        db.session.add(customer)
        self._commit()

    def delete_customer(self, customer) -> None:
        db.session.delete(customer)
        self._commit()

    @staticmethod
    def _commit() -> None:
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
