"""
Configuration and environment reader
"""

import os
from taxiweather.constants import Timezone


class Config:
    """
    Class that includes all configuration parameters as constants.
    """

    LOG_LEVEL: str = os.getenv("LOGLEVEL", "INFO")
    INPUT_DIR: str = os.getenv("INPUT_DIR", "../../input")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "../../output")
    SPARK_TIMEZONE: str = os.getenv("SPARK_TIMEZONE", Timezone.UTC)
