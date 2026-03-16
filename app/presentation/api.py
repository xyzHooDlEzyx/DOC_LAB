import csv
import os
import tempfile

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_smorest.fields import Upload
from marshmallow import Schema, fields

from ..di import build_importer
from ..models import db


class ImportSummarySchema(Schema):
    agents = fields.Int(required=True)
    customers = fields.Int(required=True)
    destinations = fields.Int(required=True)
    policies = fields.Int(required=True)


class UploadSchema(Schema):
    file = Upload(required=True)


blp = Blueprint(
    "import",
    __name__,
    url_prefix="/api",
    description="CSV import operations",
)


@blp.route("/import")
class ImportResource(MethodView):
    @blp.doc(
        summary="Import insurance data from CSV",
        description=(
            "Drops all tables, recreates them, and imports from the uploaded CSV."
        ),
    )
    @blp.arguments(UploadSchema, location="files")
    @blp.response(200, ImportSummarySchema)
    def post(self, files):
        upload = files.get("file")
        if not upload or upload.filename == "":
            abort(400, message="CSV file is missing or empty.")

        tmp_path = None
        required_columns = {
            "agent_id",
            "agent_specialization",
            "customer_id",
            "customer_name",
            "customer_age",
            "customer_health_state",
            "policy_id",
            "base_premium",
            "final_price",
            "coverage_start",
            "coverage_end",
            "destination_country",
            "destination_risk_level",
        }
        try:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".csv"
            ) as tmp_file:
                upload.save(tmp_file.name)
                tmp_path = tmp_file.name

            with open(tmp_path, "r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames:
                    abort(400, message="CSV file has no header row.")
                missing = required_columns.difference(set(reader.fieldnames))
                if missing:
                    abort(
                        400,
                        message=(
                            "CSV file is missing required columns: "
                            + ", ".join(sorted(missing))
                        ),
                    )
                if next(reader, None) is None:
                    abort(400, message="CSV file has no data rows.")

            importer = build_importer()
            db.drop_all()
            db.create_all()
            summary = importer.import_from_csv(tmp_path)
        except (KeyError, ValueError) as exc:
            abort(400, message=str(exc))
        except Exception as exc:
            abort(500, message=str(exc))
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

        return summary
