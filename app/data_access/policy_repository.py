from typing import List

from .interfaces import IPolicyRepository
from ..models import Customer, Destination, InsuranceAgent, InsurancePolicy, db


class SqlAlchemyPolicyRepository(IPolicyRepository):
    def list_policies(self):
        return InsurancePolicy.query.order_by(InsurancePolicy.id.asc()).all()

    def get_policy(self, policy_id: int):
        return db.session.get(InsurancePolicy, policy_id)

    def list_agents(self):
        return InsuranceAgent.query.order_by(InsuranceAgent.id.asc()).all()

    def list_customers(self):
        return Customer.query.order_by(Customer.id.asc()).all()

    def list_destinations(self):
        return Destination.query.order_by(Destination.country.asc()).all()

    def get_agent(self, agent_id: int):
        return db.session.get(InsuranceAgent, agent_id)

    def get_customer(self, customer_id: int):
        return db.session.get(Customer, customer_id)

    def get_destinations_by_ids(self, destination_ids: List[int]):
        if not destination_ids:
            return []
        return Destination.query.filter(Destination.id.in_(destination_ids)).all()

    def add_policy(self, policy) -> None:
        db.session.add(policy)
        self._commit()

    def update_policy(self, policy) -> None:
        db.session.add(policy)
        self._commit()

    def delete_policy(self, policy) -> None:
        db.session.delete(policy)
        self._commit()

    @staticmethod
    def _commit() -> None:
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
