# New York City Taxi Weather

This is a data analysis project, that aims to retrieve the current weather
for a taxi ride or a bike ride in New York City.

## NYC Taxi

### NYC Green Cab

---

> Source: <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page>
>
> Attribution: New York City Taxi and Limousine Commission (TLC)
>
> Terms of Use: <https://www.nyc.gov/home/terms-of-use.page>

### NYC Yellow Cab

---

> Source: <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page>
>
> Attribution: New York City Taxi and Limousine Commission (TLC)
>
> Terms of Use: <https://www.nyc.gov/home/terms-of-use.page>

## NYC Citibike

This dataset analyzes trip data from
[citibike](https://citibikenyc.com/system-data) and shows the given
weather for the current ride.

The time zone is not documented. Testing with the March Data, no negative
time spans occured because of the switch to daylight saving time when the
time zone was set to `America/New_York`.
Neither did they occur when the time zone was set to `UTC`. (They did occur
when the time zone was set to `Europe/Berlin`though).

---

> Source: <https://citibikenyc.com/system-data>
>
> Attribution: Citigroup Inc., Lyft Inc.
>
> Terms of Use: <https://www.citibikenyc.com/data-sharing-policy>

## Chicago Taxi

In this case we retrieve information about the taxi rides in the City of
Chicago from 2024-01 to 2025-03. The data is not as exact as the NYC data,
especially since the locations have been further anonymized.

---

> Source: <https://data.cityofchicago.org/Transportation/Taxi-Trips-2024-/ajtu-isnz/about_data>
>
> Attribution: City of Chicago Department of Business Affairs & Consumer Protection
>
> Terms of Use: <https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html>

## Raw Data Sets

<!-- markdownlint-disable MD013 -->

| Dataset Name                 | Description                  | Timespan                  | Input Format              | Number of records |
| ---------------------------- | ---------------------------- | ------------------------- | ------------------------- | ----------------- |
| `green_tripdata_2025-01`     | NYC Green Taxi Trip Records  | January 2025              | Parquet                   | 48326             |
| `yellow_tripdata_2025-01`    | NYC Yellow Taxi Trip Records | January 2025              | Parquet                   | 3475226           |
| `202501-citibike-tripdata`   | NYC Citibike Trip Data       | January 2025              | multiple CSVs with header | 2124475           |
| `202503-citibike-tripdata`   | NYC Citibike Trip Data       | March 2025                | CSV with header           | 3168271           |
| `Chicago_Taxi_Trips__2024-_` | Chicago Taxi Trip Records    | January 2024 - March 2025 | CSV with header           | 7917845           |
