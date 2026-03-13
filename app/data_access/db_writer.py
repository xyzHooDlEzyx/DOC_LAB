from .interfaces import IDataWriter
from ..models import db


class SqlAlchemyDataWriter(IDataWriter):
    def save_models(self, agents, customers, destinations, policies) -> None:
        try:
            db.session.add_all(agents)
            db.session.add_all(customers)
            db.session.add_all(destinations)
            db.session.add_all(policies)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
