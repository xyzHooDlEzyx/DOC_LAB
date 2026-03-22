import click

from app import create_app
from app.config import Config
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


@app.cli.command("export-incidents")
@click.option(
    "--config",
    "config_path",
    default=Config.INCIDENTS_CONFIG_PATH,
    help="Path to incidents config JSON",
)
def export_incidents(config_path: str) -> None:
    """Download Dallas incidents, save to file, then output via strategy."""
    from app.business.incident_exporter import IncidentExporter
    from app.business.output_strategies import build_output_strategy
    from app.data_access.http_json_fetcher import HttpJsonFetcher
    from app.data_access.json_file_reader import JsonFileReader
    from app.data_access.json_file_writer import JsonFileWriter
    from app.data_access.output_config import load_incident_config

    config = load_incident_config(config_path)
    dataset = config.get("dataset", {})
    output_config = config.get("output", {})
    url = dataset.get("url")
    output_file = dataset.get("output_file")
    if not url or not output_file:
        raise click.ClickException("Config must include dataset.url and output_file")

    strategy = build_output_strategy(output_config)
    exporter = IncidentExporter(
        HttpJsonFetcher(),
        JsonFileWriter(),
        JsonFileReader(),
        strategy,
    )
    result = exporter.export(url, output_file)
    click.echo(
        "Downloaded: "
        f"{result['downloaded']}, "
        "Saved: "
        f"{result['saved']}, "
        "Output: "
        f"{result['output']}"
    )
