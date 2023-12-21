#! /usr/bin/env python3

import logging
from typing import Annotated, Final

import daiquiri
from typer import Option, Typer

from dbnomics_data_model.cli import callbacks

from .commands.dataset.app import dataset_app
from .commands.provider.app import provider_app
from .commands.series.app import series_app
from .commands.update import update
from .commands.validate import validate

DEFAULT_LOG_LEVELS: Final = "dbnomics_data_model.cli=INFO"


logger = daiquiri.getLogger(__name__)


app = Typer(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)
app.add_typer(dataset_app)
app.add_typer(provider_app)
app.add_typer(series_app)
app.command(name="update")(update)
app.command(name="validate")(validate)


@app.callback()
def app_callback(
    *,
    check_series_dimensions_exist: Annotated[
        bool,
        Option(
            envvar="CHECK_SERIES_DIMENSIONS_EXIST",
            help="Check that the codes of the series dimensions and their values are defined in dataset metadata.",
        ),
    ] = True,
    debug: Annotated[bool, Option(help="Display debug messages logged by dbnomics_data_model")] = False,
    fail_fast: Annotated[bool, Option(envvar="FAIL_FAST", help="Stop at the first exception")] = False,  # noqa: ARG001
    log_levels: Annotated[
        str,
        Option(
            callback=callbacks.from_csv,
            envvar="LOG_LEVELS",
            help="Logging levels: logger_name1=log_level1,logger_name2=log_level2[,...]",
        ),
    ] = DEFAULT_LOG_LEVELS,
    storage_uri_or_dir: Annotated[str, Option(..., envvar="STORAGE_URI")],  # noqa: ARG001
    verbose: Annotated[
        bool, Option("-v", "--verbose", help="Display debug messages logged by dbnomics_data_model")
    ] = False,
) -> None:
    """DBnomics CLI tool."""
    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [("dbnomics_data_model", logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)],
    )
    daiquiri.parse_and_set_default_log_levels(log_levels)


if __name__ == "__main__":
    app()
