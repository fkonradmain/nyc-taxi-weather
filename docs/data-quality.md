<!-- markdownlint-disable MD024 -->

# Ensuring the data quality of this analysis project

## Actions in general

### Input side

If there is a way to contact the data producer, you should work together
with them to improve the data on the input side. Increasing the data
quality on the earliest stage possible is a key element in increasing the
overall data quality.

#### Timestamps

Ask data producer to document the time zone they are using

use UTC and/or EPOCH timestamps. The example data uses
timestamps without time zones. We had to guess the time zone. Which was
possible because actual humans use these services.

#### Reconsidering the input file type

Ask data producer to reconsider changing the output data type in the
following order:

##### 1. Advanced column oriented file types

Ideally the producer should use file types like Parquet or ORC to store their
data. These data types allow compression, faster readability, parallel
processing and advanced and hierarchical data types.

If Parquet or ORC is going to be recommended, heavily depends on the tech
stack that is going to be used for processing.
As of writing, parquet has the edge over ORC, especially since it allows
more complex data types and is supported by more tech stacks.

Here, we use Spark. Since Spark is optimized for Parquet and since we
are going to use that data type for storing our data, we also
recommend that data type to our producers.

##### 2. Advanced row oriented file types

Avro

In general, these types provide worse compression and do not allow the same
degree of parallel processing, but they also allow schema validation.

Additionally, they are less optimized for throughput.

##### 3. Acceptable legacy file types

File types that can be processed if the data was incomplete:

- **CSV**
- **TSV**

Do not use CSV or TSV if your raw data strings include semicolons
or tabulators respectively.

##### 4. Other acceptable, but worse file types

- **JSON**
- **XML**
- **SQL DML source code** (e.g. if our source database allows
  dumping the data that way)

They have better string handling capabilities. Processing them
has a high performance overhead, since the whole file has to be parsed
at once. Also, any error is going to invalidate the whole file.

##### 5. Bad file types (bad to even worse)

- Excel et al (especially in multinational companies)
- Any non standard data type (e.g. raw binary data, plain text)
- SQL dumps (e.g. Postgresql, MySQL)
- Yaml, Toml, ini and other types of config files
- PDF, HTML, any other Office File types

#### Encoding/Line endings

Ask the producer to produce their data in an encoding that does not change.
If the producer has automated their retrieval process, this should
already be the case.

Ideally, since all of our processing is done on Linux systems, they should
exclusively use LF line endings.

Since we are capable of processing and storing Unicode Data, and since we
usually do not measure our string length by byte length but by character
count, the producer should use Unicode, which provides a better
overall experience than ISO encodings.

### Processing side

#### Actively checking raw data compliance

Before starting to process the raw input data, we should check the current
input file for compliance.
That includes the following steps (non exhaustive):

- Checking the line endings
- Checking the encoding
- Validating that the last line is complete (ditch i)

#### Schema validation

We should check the input against a hard coded schema. While this requires
manual actions when the schema is changed, it prevents lots of
possible errors when reading and processing the data. It also has
several advantages:

- Simplification of End to End tests
- Simplification of the ETL pipeline itself (less edge case handling)
- Immediate recognition of flaws in the input data
- Protection against code injection (though unlikely)

## Citibike trip data

To ensure citibike data quality, we recommend the following actions
specifically for that data set.

### Input side

- Better time zone documentation, we had to guess the time zone by
  the use case itself (Location New York City is given) and by the
  usage distribution over 24 hours (less people ride the
  bike at night)

### Processing side

- CSV specific handling
  - Checking that the all lines are complete
  - Checking that each lines include as many semicolons as required
    by the schema
  - Checking that each CSV file includes a header
- Watching master data drift between the rows `start_station_name`,
  `start_station_id`, `end_station_name`, `end_station_id`,
  `start_lat`,`start_lng`,`end_lat`,`end_lng`
  -> to increase the data quality even further, especially if
  we want to further analyze the data, we should store the master
  data in a seperate, versionized, table.
- Geofence `start_lat`,`start_lng`,`end_lat`,`end_lng` - we know
  all of these bike rides happen in new york City
  -> either ditch the whole row or set the respective
  cell to null
- Ditch all rides with timeframes outside of the month that is
  analyzed here. Be aware of edge cases (e.g. starting the ride
  on December 31st and ending it on January 1st )

### Further Processing based on intermediate results

- Depending on the edge cases
