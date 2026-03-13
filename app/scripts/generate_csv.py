import argparse
import csv
import random
from datetime import date, timedelta


AGENT_SPECIALIZATIONS = [
    "family",
    "business",
    "student",
    "adventure",
    "premium",
]

HEALTH_STATES = ["excellent", "good", "average", "risk"]

DESTINATIONS = [
    ("France", "low"),
    ("Italy", "low"),
    ("Spain", "low"),
    ("USA", "medium"),
    ("Canada", "low"),
    ("Brazil", "medium"),
    ("Thailand", "medium"),
    ("Australia", "low"),
    ("India", "medium"),
    ("South Africa", "medium"),
    ("Mexico", "medium"),
    ("Japan", "low"),
    ("Argentina", "medium"),
    ("Norway", "low"),
    ("Egypt", "medium"),
    ("Nepal", "high"),
    ("Iceland", "low"),
    ("UAE", "medium"),
    ("Kenya", "medium"),
    ("Peru", "high"),
]


def generate_rows(target_rows: int):
    random.seed(42)
    agents = [f"A{index:03d}" for index in range(1, 21)]
    customers = [f"C{index:04d}" for index in range(1, 401)]

    rows = []
    policy_index = 1

    while len(rows) < target_rows:
        agent_id = random.choice(agents)
        customer_id = random.choice(customers)
        policy_id = f"P{policy_index:05d}"

        specialization = random.choice(AGENT_SPECIALIZATIONS)
        name = f"Customer {customer_id}"
        age = random.randint(18, 70)
        health_state = random.choice(HEALTH_STATES)

        base_premium = round(random.uniform(50, 300), 2)
        multiplier = random.uniform(1.05, 1.5)
        final_price = round(base_premium * multiplier, 2)

        start_date = date.today() + timedelta(days=random.randint(1, 90))
        end_date = start_date + timedelta(days=random.randint(3, 21))

        destination_count = random.randint(1, 3)
        for country, risk in random.sample(DESTINATIONS, destination_count):
            rows.append(
                {
                    "agent_id": agent_id,
                    "agent_specialization": specialization,
                    "customer_id": customer_id,
                    "customer_name": name,
                    "customer_age": str(age),
                    "customer_health_state": health_state,
                    "policy_id": policy_id,
                    "base_premium": f"{base_premium:.2f}",
                    "final_price": f"{final_price:.2f}",
                    "coverage_start": start_date.isoformat(),
                    "coverage_end": end_date.isoformat(),
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
