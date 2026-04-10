# Airport System Management

A database-driven Airport and Air Traffic Control (ATC) management system built with Python and PostgreSQL. This project models the operations of an airport system including flight scheduling, passenger bookings, airline management, and runway maintenance.

## Database Schema

The system uses a PostgreSQL database with the following entities:

| Table | Description |
|-------|-------------|
| **Airport** | Airport details (code, name, runways, terminals, gates, location) |
| **Airlines** | Airline information (code, name) |
| **Aircraft** | Aircraft types with capacity and lifetime |
| **Physical_Instance_Of_Aircraft** | Individual aircraft instances owned by airlines |
| **Flight_Time_Table** | Scheduled flight information (route, timing, aircraft type) |
| **Booking** | Passenger bookings with PNR, visa type, and class |
| **Passenger** | Passenger details (name, nationality, passport number) |
| **Baggage** | Baggage records linked to bookings |
| **Actual_Arr_Dep** | Actual arrival and departure timestamps and gate/runway info |
| **Pilots** | Pilot information and airline association |
| **Flight_Flew** | Records of which pilots flew which flights |
| **Prices** | Flight pricing by class |
| **Employee** | Airport employees by department |
| **Commercial_Shop** | Shops operating within airports |
| **Runway_Maintenance** | Runway inspection records |
| **Availability_Code** | Day-of-week availability for flights |

## ER Diagram

![ER Diagram](ER%20Diagram.png)

## Relational Schema

![Relational Schema](Relational%20Schema.png)

## Features

### Console Application

The system provides an interactive console (`console.py`) with the following options:

1. **Write Your Own Query** — Execute custom SQL queries directly
2. **Pre-written Queries / Stored Procedures:**
   - Find expected immigrants on a given date at a given airport
   - Find average delay for each flight (stored procedure)
   - Find aircraft details by airline based on years left in service
   - Get passenger IDs for travelers between two airports on a given date
   - Find all flights available on a given day between two airports
   - Get flight costs between source and destination airports
   - Sort airports by latest runway maintenance check date
   - Count passengers at a given airport for a given time span
   - Find frequent flyers by airline above a given threshold
3. **Inserts:**
   - Insert a runway maintenance check
   - Insert a booking
4. **Updates:**
   - Update a passenger's name
   - Update the cost of a flight

### Trigger

A trigger (`Trigger_01.txt`) automatically logs price changes into a `Flight_Price_History` table whenever a flight's cost is updated.

## Tech Stack

- **Language:** Python
- **Database:** PostgreSQL
- **Driver:** psycopg2

## Prerequisites

- Python 3.x
- PostgreSQL server
- `psycopg2` Python package

## Setup

1. **Install dependencies:**
   ```bash
   pip install psycopg2
   ```

2. **Set up the database:**
   - Create a PostgreSQL database
   - Run the DDL script (`DDL_Script.txt`) to create the schema
   - Run the insert script (`Insert_Script.txt`) to populate initial data

3. **Configure database connection:**
   Update the connection parameters in `console.py`:
   ```python
   db_name = 'your_database'
   db_user = 'your_username'
   db_host = 'your_host'
   db_pass = 'your_password'
   db_port = '5432'
   ```

4. **Run the application:**
   ```bash
   python console.py
   ```

## Project Files

| File | Description |
|------|-------------|
| `console.py` | Main console application entry point |
| `my_queries.py` | SQL query functions for all operations |
| `DDL_Script.txt` | Database schema creation script |
| `Insert_Script.txt` | Sample data insertion script |
| `Query.txt` | Reference list of SQL queries |
| `queries_doc.txt` | Query descriptions |
| `inserts_doc.txt` | Insert operation descriptions |
| `updates_doc.txt` | Update operation descriptions |
| `Trigger_01.txt` | Price history trigger definition |
| `Stored_Procedure.pdf` | Stored procedure documentation |
| `ER Diagram.png` | Entity-Relationship diagram |
| `Relational Schema.png` | Relational schema diagram |
