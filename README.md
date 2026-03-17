# Airport System Management

A Python-based console application for managing airport operations, flights, bookings, passengers, and air traffic control data using PostgreSQL.

## Features

- Interactive command-line interface for querying and managing airport data
- 9 pre-written SQL queries covering:
  - Immigrant lookups by date and airport
  - Average flight delays (via stored procedure)
  - Aircraft details filtered by airline and service years
  - Passenger lookups by route and date
  - Flight availability by day, source, and destination
  - Pricing information by route
  - Runway maintenance sorted by last inspection date
  - Passenger counts for a given airport and time span
  - Frequent flyer identification by booking frequency
- Insert operations for runway maintenance records and bookings
- Update operations for passenger names and flight costs
- Custom SQL query execution
- Database trigger for tracking flight price history

## Database Schema Overview

The database uses the `airport_atc` schema and consists of 17 tables:

| Table | Description |
|-------|-------------|
| Airport | Airport details (code, name, runways, terminals, gates, location) |
| Commercial_Shop | Shops located within airports |
| Runway_Maintenance | Runway inspection records |
| Employee | Airport employees and their departments |
| Availability_Code | Day-of-week availability flags for flights |
| Passenger | Passenger identity and passport information |
| Aircraft | Aircraft type specifications (capacity, lifetime) |
| Airlines | Airline codes and names |
| Flight_Time_Table | Scheduled flight information and routes |
| Booking | Passenger bookings with PNR, visa type, and class |
| Baggage | Baggage records linked to bookings |
| Actual_Arr_Dep | Actual arrival/departure timestamps and gate assignments |
| Physical_Instance_Of_Aircraft | Individual aircraft instances with manufacturing dates |
| Aircraft_Used | Maps flights to physical aircraft |
| Pilots | Pilot information and airline affiliation |
| Prices | Flight pricing by class |
| Flight_Flew | Records of which pilots flew which flights |
| Flight_Price_History | Automatic price change audit log (trigger-managed) |

## Prerequisites

- Python 3.x
- PostgreSQL
- psycopg2 Python library

## Setup Instructions

1. Install the Python dependency:

   ```bash
   pip install psycopg2
   ```

2. Create a PostgreSQL database and set up the schema using the DDL script:

   ```bash
   psql -U <username> -d <database> -f DDL_Script.txt
   ```

3. Populate the database with sample data:

   ```bash
   psql -U <username> -d <database> -f Insert_Script.txt
   ```

4. (Optional) Install the flight price history trigger:

   ```bash
   psql -U <username> -d <database> -f Trigger_01.txt
   ```

5. Update the database connection settings in `console.py`:

   ```python
   db_name = '<your_database>'
   db_user = '<your_username>'
   db_host = '<your_host>'
   db_pass = '<your_password>'
   db_port = '5432'
   ```

6. Run the application:

   ```bash
   python console.py
   ```

## Usage

On startup, the application displays an interactive menu with five options:

1. **Write Your Own Query** -- Execute any custom SQL query against the database.
2. **Pre-written Queries** -- Run one of 9 predefined queries by entering a Query ID:
   - `1` Find expected immigrants on a given date at a given airport
   - `2` Find average delay for each flight
   - `3` Find aircraft details by airline and years left in service
   - `4` Find passenger IDs for a route and date
   - `5` Find available flights for a day, source, and destination
   - `6` Find flight costs for a given route
   - `7` Sort airports by latest runway inspection date
   - `8` Count passengers at an airport for a time span
   - `9` Find frequent flyers exceeding a booking threshold
3. **Inserts** -- Add new records:
   - `1` Insert a runway maintenance check
   - `2` Insert a booking
4. **Updates** -- Modify existing records:
   - `1` Update a passenger's name
   - `2` Update a flight's cost (triggers price history logging)
5. **Exit** -- Close the application.

## Project Structure

```
.
├── console.py                 Main application entry point with interactive CLI
├── my_queries.py              Pre-written SQL query, insert, and update definitions
├── DDL_Script.txt             Database schema definition (CREATE TABLE statements)
├── Insert_Script.txt          Sample data population script
├── Query.txt                  Query documentation
├── Trigger_01.txt             Flight price history trigger definition
├── ER Diagram.png             Entity-Relationship diagram
├── ER Diagram.dia             ER diagram source file (Dia format)
├── Relational Schema.png      Relational schema visualization
├── Stored_Procedure.pdf       Stored procedure documentation
├── queries_doc.txt            Descriptions of all pre-written queries
├── inserts_doc.txt            Descriptions of insert operations
└── updates_doc.txt            Descriptions of update operations
```

## ER Diagram

Refer to `ER Diagram.png` for the full Entity-Relationship diagram illustrating the database structure and table relationships.

![ER Diagram](ER%20Diagram.png)
