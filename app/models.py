from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

policy_destinations = db.Table(
    "policy_destinations",
    db.Column(
        "policy_id",
        db.Integer,
        db.ForeignKey("insurance_policies.id"),
        primary_key=True,
    ),
    db.Column(
        "destination_id",
        db.Integer,
        db.ForeignKey("destinations.id"),
        primary_key=True,
    ),
)


class InsuranceAgent(db.Model):
    __tablename__ = "insurance_agents"

    id = db.Column(db.Integer, primary_key=True)
    agent_identifier = db.Column(db.String(40), unique=True, nullable=False)
    specialization = db.Column(db.String(80), nullable=False)

    policies = db.relationship("InsurancePolicy", back_populates="agent")


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_identifier = db.Column(db.String(40), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    health_state = db.Column(db.String(60), nullable=False)

    policies = db.relationship("InsurancePolicy", back_populates="customer")


class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80), unique=True, nullable=False)
    risk_level = db.Column(db.String(30), nullable=False)


class InsurancePolicy(db.Model):
    __tablename__ = "insurance_policies"

    id = db.Column(db.Integer, primary_key=True)
    policy_identifier = db.Column(db.String(40), unique=True, nullable=False)
    base_premium = db.Column(db.Float, nullable=False)
    final_price = db.Column(db.Float, nullable=False)
    coverage_start = db.Column(db.Date, nullable=False)
    coverage_end = db.Column(db.Date, nullable=False)

    agent_id = db.Column(
        db.Integer, db.ForeignKey("insurance_agents.id"), nullable=False
    )
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.id"), nullable=False
    )

    agent = db.relationship("InsuranceAgent", back_populates="policies")
    customer = db.relationship("Customer", back_populates="policies")
    destinations = db.relationship(
        "Destination",
        secondary=policy_destinations,
        lazy="subquery",
    )
