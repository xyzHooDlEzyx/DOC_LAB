import os
import sys

from sqlalchemy import func

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import create_app
from app.models import Customer, Destination, InsuranceAgent, InsurancePolicy, db


def main():
    app = create_app()
    with app.app_context():
        counts = {
            "agents": db.session.query(func.count(InsuranceAgent.id)).scalar(),
            "customers": db.session.query(func.count(Customer.id)).scalar(),
            "destinations": db.session.query(func.count(Destination.id)).scalar(),
            "policies": db.session.query(func.count(InsurancePolicy.id)).scalar(),
        }

        sample_policy = (
            db.session.query(InsurancePolicy)
            .order_by(InsurancePolicy.id.asc())
            .limit(1)
            .one_or_none()
        )

        print("Counts:")
        for key, value in counts.items():
            print(f"- {key}: {value}")

        if sample_policy:
            destination_names = ", ".join(
                destination.country for destination in sample_policy.destinations
            )
            print("\nSample policy:")
            print(f"- policy_id: {sample_policy.policy_identifier}")
            print(f"- agent_id: {sample_policy.agent.agent_identifier}")
            print(f"- customer_id: {sample_policy.customer.customer_identifier}")
            print(f"- destinations: {destination_names}")


if __name__ == "__main__":
    main()
