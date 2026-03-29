import argparse
import csv
import os
import random
import sys
from datetime import date, timedelta

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.data.countries import COUNTRIES, HIGH_RISK_COUNTRIES


AGENT_SPECIALIZATIONS = [
    "family",
    "business",
    "student",
    "adventure",
    "premium",
]

HEALTH_STATES = ["excellent", "good", "average", "risk"]
GENDERS = ["female", "male", "non-binary"]
HEALTH_CONDITIONS = [
    "none",
    "asthma",
    "diabetes",
    "hypertension",
    "allergy",
]

RISK_LEVELS = ["low", "medium", "high"]
TRIP_TYPES = ["business", "leisure", "adventure", "study"]


def _build_country_risks():
    random.seed(42)
    mapping = {}
    for country in COUNTRIES:
        if country in HIGH_RISK_COUNTRIES:
            mapping[country] = "high"
        else:
            mapping[country] = random.choice(RISK_LEVELS)
    return mapping


def generate_rows(target_rows: int):
    random.seed(42)
    agents = [f"A{index:03d}" for index in range(1, 21)]
    customers = [f"C{index:04d}" for index in range(1, 401)]
    country_risks = _build_country_risks()

    rows = []
    policy_index = 1

    country_index = 0
    while len(rows) < target_rows:
        agent_id = random.choice(agents)
        customer_id = random.choice(customers)
        policy_id = f"P{policy_index:05d}"

        specialization = random.choice(AGENT_SPECIALIZATIONS)
        name = f"Customer {customer_id}"
        age = random.randint(18, 70)
        health_state = random.choice(HEALTH_STATES)
        gender = random.choice(GENDERS)
        health_condition = random.choice(HEALTH_CONDITIONS)

        base_premium = round(random.uniform(50, 300), 2)
        multiplier = random.uniform(1.05, 1.5)
        final_price = round(base_premium * multiplier, 2)

        start_date = date.today() + timedelta(days=random.randint(1, 90))
        end_date = start_date + timedelta(days=random.randint(3, 21))

        destination_count = random.randint(1, 3)
        trip_type = random.choice(TRIP_TYPES)
        is_family = random.choice([True, False])
        family_size = random.randint(2, 5) if is_family else 1
        selected_countries = random.sample(COUNTRIES, destination_count)
        if country_index < len(COUNTRIES):
            selected_countries[0] = COUNTRIES[country_index]
            country_index += 1
        for country in selected_countries:
            risk = country_risks[country]
            rows.append(
                {
                    "agent_id": agent_id,
                    "agent_specialization": specialization,
                    "customer_id": customer_id,
                    "customer_name": name,
                    "customer_age": str(age),
                    "customer_health_state": health_state,
                    "customer_gender": gender,
                    "customer_health_condition": health_condition,
                    "policy_id": policy_id,
                    "base_premium": f"{base_premium:.2f}",
                    "final_price": f"{final_price:.2f}",
                    "coverage_start": start_date.isoformat(),
                    "coverage_end": end_date.isoformat(),
                    "trip_type": trip_type,
                    "is_family": str(is_family).lower(),
                    "family_size": str(family_size),
                    "destination_country": country,
                    "destination_risk_level": risk,
                }
            )

        policy_index += 1

    return rows[:target_rows]


def main():
    parser = argparse.ArgumentParser(description="Generate insurance CSV data")
    parser.add_argument(
        "--rows",
        type=int,
        default=1000,
        help="Minimum number of rows to generate",
    )
    parser.add_argument(
        "--output",
        default="/home/overlord/DOCS/app/data/insurance_data.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()

    rows = generate_rows(args.rows)

    with open(args.output, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows at {args.output}")


if __name__ == "__main__":
    main()
