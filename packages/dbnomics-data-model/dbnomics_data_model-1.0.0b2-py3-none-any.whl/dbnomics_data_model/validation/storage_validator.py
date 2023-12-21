import daiquiri

from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.storage import Storage

from .provider_validator import ProviderValidator
from .validation_reports import StorageValidationReport

logger = daiquiri.getLogger(__name__)


class StorageValidator:
    def __init__(
        self,
        *,
        check_series_dimensions_exist: bool = True,
        series_per_dataset_limit: int | None = None,
        storage: Storage,
        validation_report: StorageValidationReport | None = None,
    ) -> None:
        if validation_report is None:
            validation_report = StorageValidationReport()

        self.check_series_dimensions_exist = check_series_dimensions_exist
        self.series_per_dataset_limit = series_per_dataset_limit
        self.validation_report = validation_report
        self._storage = storage

    def validate(self) -> None:
        logger.debug("Validating storage...", storage=self._storage)

        for provider_code in self._storage.iter_provider_codes():
            self.validate_provider(provider_code)

        logger.debug("Validation end", validation_report=self.validation_report)

    def validate_provider(self, provider_code: ProviderCode) -> None:
        provider_validator = ProviderValidator(
            check_series_dimensions_exist=self.check_series_dimensions_exist,
            provider_code=provider_code,
            series_per_dataset_limit=self.series_per_dataset_limit,
            storage=self._storage,
            validation_report=self.validation_report.providers[provider_code],
        )
        provider_validator.validate()
