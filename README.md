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

## NCEI weather data

In this case, we retrieve the weather data from the National Centers for
Environment Information.

Be aware: the NCEI is deprecating their old ISD schema in favor of the new GHCNh
schema.

As of now, we use the Central Park weather station for all of New York. Yet there
are multiple stations in the area.

> Source: <https://www.ncei.noaa.gov/products/global-historical-climatology-network-hourly>
>
> Attribution: National Oceanic and Atmospheric Administration
>
> Terms of Use: <https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C01688/html>

Source of the relevant parquet file:
<https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/access/by-year/2025/parquet/GHCNh_USW00094728_2025.parquet>

## NCEI Weather Station List

By using the NCEI weather station list, we can locate the station that is the
nearest to the current position. That way the weather results become more exact.

<https://www.ncei.noaa.gov/pub/data/noaa/isd-inventory.csv>
<https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv>

> Integrated Surface Database Station History, April 2025
> THIS INVENTORY SHOWS THE NUMBER OF WEATHER OBSERVATIONS BY STATION-YEAR-MONTH
> FOR BEGINNING OF RECORD THROUGH APRIL 2025. THE DATABASE CONTINUES TO BE
> UPDATED AND ENHANCED, AND THIS INVENTORY WILL BE UPDATED ON A REGULAR BASIS.

## Raw Data Sets

<!-- markdownlint-disable MD013 -->

| Dataset Name                 | Description                  | Timespan                  | Input Format              | Number of records |
| ---------------------------- | ---------------------------- | ------------------------- | ------------------------- | ----------------- |
| `green_tripdata_2025-01`     | NYC Green Taxi Trip Records  | January 2025              | Parquet                   | 48326             |
| `yellow_tripdata_2025-01`    | NYC Yellow Taxi Trip Records | January 2025              | Parquet                   | 3475226           |
| `202501-citibike-tripdata`   | NYC Citibike Trip Data       | January 2025              | multiple CSVs with header | 2124475           |
| `202503-citibike-tripdata`   | NYC Citibike Trip Data       | March 2025                | CSV with header           | 3168271           |
| `Chicago_Taxi_Trips__2024-_` | Chicago Taxi Trip Records    | January 2024 - March 2025 | CSV with header           | 7917845           |
