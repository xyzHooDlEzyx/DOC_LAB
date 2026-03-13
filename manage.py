import click

from app import create_app
from app.di import build_importer
from app.models import db


app = create_app()


@app.cli.command("init-db")
@click.option(
    "--csv",
    "csv_path",
    default="/home/overlord/DOCS/app/data/insurance_data.csv",
    help="Path to CSV file",
)
def init_db(csv_path):
    """Create tables and import CSV data."""
    importer = build_importer()
    with app.app_context():
        db.create_all()
        summary = importer.import_from_csv(csv_path)
    click.echo(
        "Imported: "
        f"agents={summary['agents']}, "
        f"customers={summary['customers']}, "
        f"destinations={summary['destinations']}, "
        f"policies={summary['policies']}"
    )
