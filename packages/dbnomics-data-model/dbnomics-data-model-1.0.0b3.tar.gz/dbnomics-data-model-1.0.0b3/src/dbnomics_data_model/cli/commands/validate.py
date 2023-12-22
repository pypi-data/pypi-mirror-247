import json
from typing import Annotated, Optional

from typer import Abort, Context, Option, echo

from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.validation.storage_validator import StorageValidator
from dbnomics_data_model.validation.validation_reports import StorageValidationReport

__all__ = ["validate"]


def validate(
    *,
    ctx: Context,
    series_per_dataset_limit: Annotated[
        Optional[int],
        Option(
            envvar="SERIES_PER_DATASET_LIMIT",
            help="Maximum number of series to validate per dataset. If not set, validate all series.",
        ),
    ] = None,
) -> None:
    """Validate data of a DBnomics storage."""
    root_ctx_params = ctx.find_root().params
    check_series_dimensions_exist: bool = root_ctx_params["check_series_dimensions_exist"]
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    if series_per_dataset_limit is not None and series_per_dataset_limit <= 0:
        echo(f"series limit must be strictly positive, got {series_per_dataset_limit!r}", err=True)
        raise Abort

    storage = open_storage(storage_uri_or_dir)
    storage_validation_report = StorageValidationReport()

    validator = StorageValidator(
        check_series_dimensions_exist=check_series_dimensions_exist,
        series_per_dataset_limit=series_per_dataset_limit,
        storage=storage,
        validation_report=storage_validation_report,
    )
    validator.validate()

    validation_report_json = storage_validation_report.to_json()
    if validation_report_json:
        echo(json.dumps(validation_report_json, indent=2, sort_keys=True))
        raise Abort
