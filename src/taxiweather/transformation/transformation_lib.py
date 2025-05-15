from pyspark.sql import SparkSession, DataFrame, Column
from pyspark.sql.types import TimestampNTZType, TimestampType, LongType
import pyspark.sql.functions as F
from taxiweather.constants import Constants, Timezone

spark: SparkSession = SparkSession.builder.getOrCreate()
if not isinstance(spark, SparkSession):
    raise RuntimeError("spark object is not of type pyspark.sql.SparkSession")


# Library Method
def create_timestamp_columns(
    df: DataFrame,
    ts_result_column_name: str,
    timestamp_string_column_expression: Column,
    timestamp_string_format: str,
    tz: str = Timezone.UTC,
    is_private_column: bool = False,
    rfc3339_format_str: str = "yyyy-MM-dd'T'HH:mm:ssxxx'['VV']'",
) -> DataFrame:
    """
    Converts a timestamp from a string or long format into two compliant columns '_rfc3339' and '_epoch_ms'.
    Supported are strings with the corresponding formatting pattern.
    In cases of 13 digit or 10 digit long values timestamp_string_format must be set to either "epoch_13digit" or
    "epoch_10digit".

    Examples (with 'cet' as timezone setting):
        - 2022-05-23 00:45:34 becomes 2022-05-23T00:45:34.000+0200 (_rfc3339)
        - 2022-05-23 00:45:34 becomes 2022-05-22T22:45:34.000+0200 (_epoch_ms)

        - 1647302402125 becomes 2022-03-15T01:00:02.125+0100 (_rfc3339)
        - 1647302402125 becomes 2022-03-15T00:00:02.125Z (_epoch_ms)

    For parsing of string columns, especially timezones
    See https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html

    :param df: the Dataframe where timestamp columns RFC3339 and epoch ms will be added
    :param ts_result_column_name: the `column_name` for timestamp columns,
    results in names "Timestamp_`name`_[Epoch_ms|RFC3339]"
    :param timestamp_string_column_expression: column expression which gives timestamp *string* column
    that fits to `format` parameter
    :param timestamp_string_format: format the column_expression *string* column is in.
    :param is_private_column: indicates whether the timestamp columns should be prefixed with a `_`
    """
    old_timezone: str = spark.conf.get("spark.sql.session.timeZone")
    spark.conf.set("spark.sql.session.timeZone", tz)
    private_prefix = "_" if is_private_column else ""
    # TODO: correct the column cast - The timestamp has to be read as if it had no timezone assigned to it
    # timestamp_string_column_expression = F.cast(
    #     TimestampNTZType, timestamp_string_column_expression
    # )
    # If timestamp is a 13 digit/10 digit epoch long value
    if timestamp_string_format in ("epoch_ms", "epoch_s"):

        accommodate_unix_epoch_length = (
            1000 if timestamp_string_format == "epoch_ms" else 1
        )

        # Create RFC3339 compliant string type column
        df = df.withColumn(
            f"{private_prefix}{Constants.TIMESTAMPS_PREFIX}_{ts_result_column_name}_{Constants.RFC3339_SUFFIX}",
            col=F.date_format(
                date=F.to_timestamp(
                    col=timestamp_string_column_expression
                    / accommodate_unix_epoch_length,
                ),
                format=rfc3339_format_str,
            ),
        )
        # Create RFC3339 compliant timestamp type column
        df = df.withColumn(
            f"{private_prefix}{Constants.TIMESTAMPS_PREFIX}_{ts_result_column_name}_{Constants.EPOCH_MS_SUFFIX}",
            col=F.to_timestamp(
                col=timestamp_string_column_expression / accommodate_unix_epoch_length,
            ),
        )
    # If timestamp is a string value
    else:
        millis = F.date_format(
            F.to_timestamp(timestamp_string_column_expression, timestamp_string_format),
            "SSS",
        ).cast(LongType())

        df = df.withColumn(
            f"{private_prefix}{Constants.TIMESTAMPS_PREFIX}_{ts_result_column_name}_{Constants.RFC3339_SUFFIX}",
            F.date_format(
                # F.unix_timestamp() neglects fractions of seconds. This is why they are added here manually.
                (
                    F.unix_timestamp(
                        timestamp_string_column_expression,
                        format=timestamp_string_format,
                    )
                    + millis / 1_000
                ).cast(TimestampType()),
                rfc3339_format_str,
            ),
        ).withColumn(
            f"{private_prefix}{Constants.TIMESTAMPS_PREFIX}_{ts_result_column_name}_{Constants.EPOCH_MS_SUFFIX}",
            (
                F.unix_timestamp(
                    timestamp_string_column_expression, format=timestamp_string_format
                )
                + millis / 1_000
            ).cast(TimestampType()),
        )
    spark.conf.set("spark.sql.session.timeZone", old_timezone)
    return df


def deprecate_column(df: DataFrame, col: str) -> DataFrame:
    """Deprecate a column by adding a suffix to its name.

    Args:
        col (Column | str): The column to deprecate.

    Returns:
        Column: The deprecated column.
    """
    return df.withColumnRenamed(col, f"_DEPRECATED_{col}")


def deprecate_columns(
    df: DataFrame, columns_to_deprecate: list[str], preserve: bool = False
) -> DataFrame:
    """
    Deprecates columns, hence renames them. Optionally preserves old columns for further usage during ETL Pipeline
    :param df: DataFrame on which shall be operated
    :param columns_to_deprecate: List of column names that shall be deprecated
    :param preserve: If True, keeps original column instead of deleting it
    :return:
    """
    for element in columns_to_deprecate:
        df = df.withColumn(f"{Constants.DEPRECATED_PREFIX}{element}", F.col(element))
        if not preserve:
            df = df.drop(F.col(element))
    return df
