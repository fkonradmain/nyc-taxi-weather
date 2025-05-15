"""
Configuration and environment reader
"""

import os


class Config:
    """
    Class that includes all configuration parameters as constants.
    """

    LOG_LEVEL: str = os.getenv("LOGLEVEL", "INFO")
    INPUT_DIR: str = os.getenv("INPUT_DIR", "../../input")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "../../output")
