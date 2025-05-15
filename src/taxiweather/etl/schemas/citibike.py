from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    TimestampNTZType,
    DoubleType,
)

citibike_schema: StructType = StructType(
    [
        StructField("ride_id", StringType(), False),
        StructField("rideable_type", StringType(), True),
        StructField("started_at", TimestampNTZType(), True),
        StructField("ended_at", TimestampNTZType(), True),
        StructField("start_station_name", StringType(), True),
        StructField("start_station_id", StringType(), True),
        StructField("end_station_name", StringType(), True),
        StructField("end_station_id", StringType(), True),
        StructField("start_lat", DoubleType(), True),
        StructField("start_lng", DoubleType(), True),
        StructField("end_lat", DoubleType(), True),
        StructField("end_lng", DoubleType(), True),
        StructField("member_casual", StringType(), True),
    ]
)
