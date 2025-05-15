"""Module provividing the Load logic for nyc-taxi-weather
Raises:
    RuntimeError: If the spark object is not of type pyspark.sql.SparkSession
"""

from pyspark.sql import SparkSession, DataFrame

# import pyspark.sql.functions as F
from pyspark.sql.types import StructType
from taxiweather.etl.schemas.citibike import citibike_schema
from taxiweather.config import config
from taxiweather.constants import Timezone

spark: SparkSession = SparkSession.builder.getOrCreate()
if not isinstance(spark, SparkSession):
    raise RuntimeError("spark object is not of type pyspark.sql.SparkSession")


def load_citibike_csv(
    spark: SparkSession,
    month: str,
    schema: StructType | None = citibike_schema,
    infer_schema: bool = False,
    tz: str = Timezone.nyc.value,
) -> DataFrame:
    """Load CSV files from the input directory for the specified month.

    Args:
        spark (SparkSession): SparkSession to run in
        month (str): The month in the format YYYYMM.
        schema (StructType, optional): The schema to use when parsing the citibike data.
            Defaults to citibike_schema.
        infer_schema (bool, optional): If the schema is to be auto generated or pre-defined.
            Defaults to False -> predefined.
        tz (str): The time zone to evaluate the input data timestamps as.

    Returns:
        DataFrame: A Spark DataFrame containing the loaded data.
    """
    # Get the current time zone then set the time zone to "America/New_York"
    old_timezone: str | None = spark.conf.get("spark.sql.session.timeZone")
    spark.conf.set("spark.sql.session.timeZone", tz)

    df: DataFrame = spark.read.csv(
        header=True,
        schema=schema,
        inferSchema=infer_schema,
        path=f"{config.INPUT_DIR}/{month}-citibike-tripdata*.csv",
    )
    # Restore the old time zone
    if old_timezone is not None:
        spark.conf.set("spark.sql.session.timeZone", old_timezone)
    return df


def load_weather_parquet(
    spark: SparkSession,
    station_id: str = "USW00094728",  # Central Park
    year: str = "2025",
    tz: str = Timezone.nyc.value,
) -> DataFrame:
    """Load CSV files from the input directory for the specified month.

    Args:
        spark (SparkSession): SparkSession to run in
        year (str): The year in the format YYYY
        tz (str): The time zone to evaluate the input data timestamps as.

    Returns:
        DataFrame: A Spark DataFrame containing the loaded data.
    """
    # Get the current time zone then set the time zone to "America/New_York"
    old_timezone: str | None = spark.conf.get("spark.sql.session.timeZone")
    spark.conf.set("spark.sql.session.timeZone", tz)

    df: DataFrame = spark.read.parquet(
        f"{config.INPUT_DIR}/GHCNh_{station_id}_{year}.parquet",
    )
    # Restore the old time zone
    if old_timezone is not None:
        spark.conf.set("spark.sql.session.timeZone", old_timezone)
    return df
