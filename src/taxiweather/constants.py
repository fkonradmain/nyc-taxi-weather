"""
Constants for taxiweather
"""

from enum import Enum


class Timezone(Enum):
    """
    Defines the available time zones.
    """

    cet = "Europe/Berlin"
    utc = "UTC"
    nyc = "America/New_York"
