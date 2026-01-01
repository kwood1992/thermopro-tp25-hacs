"""Constants for the Thermopro TP25 integration."""

import logging
from typing import Final

_LOGGER = logging.getLogger(__package__)

DOMAIN: Final[str] = "thermopro_tp25_hacs"
PLATFORMS: Final[list[str]] = ["sensor"]
