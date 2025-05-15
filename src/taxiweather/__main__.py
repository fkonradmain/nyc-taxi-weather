from pyspark.sql import SparkSession, DataFrame, Window
import pyspark.sql.functions as F
from taxiweather.config import Config
from typing import Any

# TODO: actually use the logger
# from taxiweather.logger import logger
from taxiweather.constants import Timezone
from taxiweather.transformation.transformation_lib import (
    create_timestamp_columns,
    deprecate_columns,
)
from taxiweather.etl.load import load_citibike_csv, load_weather_parquet


# TODO: correct type hints, Any is far from ideal
def main(*args: Any, **kwargs: Any) -> None:
    """
    Main function that is called when the module launches

    args: positional arguments.
    kwargs: keyword arguments.

    Raises:
        RuntimeError: If no spark context can be initialized
    """
    spark: SparkSession = SparkSession.builder.getOrCreate()
    if not isinstance(spark, SparkSession):
        raise RuntimeError("spark object is not of type pyspark.sql.SparkSession")
    spark.conf.set("spark.sql.session.timeZone", Config.SPARK_TIMEZONE)

    # load Input data into dataframes
    df_citibike_raw: DataFrame = load_citibike_csv(spark=spark)
    df_weather_raw: DataFrame = load_weather_parquet(spark=spark)

    # Clean Input data
    df_citibike_clean: DataFrame = clean_citibike_data(df_citibike_raw=df_citibike_raw)
    df_weather_clean: DataFrame = clean_weather_data(df_weather_raw=df_weather_raw)

    # Enhance weather data to include time spans instead of just single points in time
    df_weather_timespans: DataFrame = create_weather_timespans(
        df_weather_clean=df_weather_clean
    )

    # Join Weather data onto Citibike data
    df_citibike_weather: DataFrame = match_citibike_weather(
        df_citibike_clean=df_citibike_clean, df_weather_timespans=df_weather_timespans
    )

    # TODO: rename columns after matching

    # Write the joined data to a parquet output file
    df_citibike_weather.write.parquet(
        mode="overwrite", path=f"{Config.OUTPUT_DIR}/nyc_taxi_weather.parquet"
    )


def match_citibike_weather(
    df_citibike_clean: DataFrame, df_weather_timespans: DataFrame
) -> DataFrame:
    """
    Matches citibike data with weather data based on the start time of the ride.

    Args:
        df_citibike_clean (DataFrame): The cleaned citibike data DataFrame.
        df_weather_timespans (DataFrame): The citibike data DataFrame, that includes the validity time span of each weather record.

    Returns:
        DataFrame: A DataFrame containing the matched citibike and weather data.
    """
    df_citibike_weather = df_citibike_clean.alias("c").join(
        df_weather_timespans.alias("w"),
        on=(F.col("c.timestamp_started_at_epoch_ms") >= F.col("w.valid_from_epoch_ms"))
        & (F.col("c.timestamp_started_at_epoch_ms") < F.col("w.valid_until_epoch_ms")),
        how="left",
    )
    return df_citibike_weather


def clean_citibike_data(df_citibike_raw: DataFrame) -> DataFrame:
    """
    Cleans the citibike data by selecting relevant columns and creating timestamp columns.
    Args:
        df_citibike_raw (DataFrame): The raw citibike data DataFrame.
    """
    # df_citibike_clean: DataFrame  = df_citibike_raw.select(
    #     ["start_station_id", "started_at"]
    # )
    df_citibike_clean = create_timestamp_columns(
        df=df_citibike_raw,
        ts_result_column_name="started_at",
        timestamp_string_column_expression=F.col("started_at"),
        timestamp_string_format="yyyy-MM-dd HH:mm:ss.SSS",
        tz=Timezone.NYC,
    )

    df_citibike_clean = create_timestamp_columns(
        df=df_citibike_raw,
        ts_result_column_name="ended_at",
        timestamp_string_column_expression=F.col("ended_at"),
        timestamp_string_format="yyyy-MM-dd HH:mm:ss.SSS",
        tz=Timezone.NYC,
    )

    df_citibike_clean = deprecate_columns(
        df=df_citibike_clean, columns_to_deprecate=["started_at", "ended_at"]
    )

    return df_citibike_clean


def clean_weather_data(df_weather_raw: DataFrame) -> DataFrame:
    """
    Cleans the weather data by selecting relevant columns and creating timestamp columns.
    Args:
        df_weather_raw (DataFrame): The raw weather data DataFrame.
    """
    df_weather_clean: DataFrame = df_weather_raw.select(
        ["Station_ID", "Station_name", "DATE", "temperature"]
    )
    df_weather_clean = create_timestamp_columns(
        df=df_weather_clean,
        ts_result_column_name="DATE",
        timestamp_string_column_expression=F.col("DATE"),
        timestamp_string_format="yyyy-MM-dd'T'HH:mm:ss",
        tz=Timezone.NYC,
    )

    df_weather_clean = deprecate_columns(
        df=df_weather_clean, columns_to_deprecate=["DATE"]
    )

    return df_weather_clean


def create_weather_timespans(df_weather_clean: DataFrame) -> DataFrame:
    """
    Creates time spans for the weather data based on the timestamp of the
    current weather update and the start timestamp of the next weather update.
        df_weather_clean (DataFrame): The cleaned weather data DataFrame.
    """
    df_valid_from: DataFrame = df_weather_clean.withColumn(
        "valid_from_epoch_ms", F.col("timestamp_DATE_epoch_ms")
    )
    validity_window = Window.orderBy(F.col("valid_from_epoch_ms"))
    df_weather_timespans: DataFrame = df_valid_from.withColumn(
        "valid_until_epoch_ms",
        F.lead(F.col("valid_from_epoch_ms")).over(validity_window),
    )

    return df_weather_timespans
