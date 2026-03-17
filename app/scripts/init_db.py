import argparse
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import create_app
from app.di import build_importer
from app.models import db


def main():
    parser = argparse.ArgumentParser(description="Initialize database and import CSV")
    parser.add_argument(
        "--csv",
        default="/home/overlord/DOCS/app/data/insurance_data.csv",
        help="Path to CSV file",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop existing tables before creating new ones",
    )
    args = parser.parse_args()

    app = create_app()
    importer = build_importer()

    with app.app_context():
        if args.reset:
            db.drop_all()
        db.create_all()
        summary = importer.import_from_csv(args.csv)

    print(
        "Imported: "
        f"agents={summary['agents']}, "
        f"customers={summary['customers']}, "
        f"destinations={summary['destinations']}, "
        f"policies={summary['policies']}"
    )


if __name__ == "__main__":
    main()
