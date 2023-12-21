import enum
import importlib_metadata


def _get_version() -> str:
    try:
        return importlib_metadata.version(__package__)
    except importlib_metadata.PackageNotFoundError:
        return "dev"


__version__ = _get_version()


class TimeSeriesType(enum.Enum):
    FORECAST = 1
    """Forecast point predictions"""

    HISTORICAL = 2
    """Historical predictions"""
