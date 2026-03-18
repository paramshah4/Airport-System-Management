import os

import psycopg2
from psycopg2 import sql
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_NAME = os.environ.get('DB_NAME', 'airport_db')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute('SET SEARCH_PATH TO airport_atc;')
        cur.close()
        return conn
    except Exception:
        if conn is not None:
            conn.close()
        raise


@app.route('/')
def index():
    return jsonify({"status": "ok", "message": "Airport System Management API"})


@app.route('/api/health')
def health():
    conn = None
    try:
        conn = get_db_connection()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500
    finally:
        if conn is not None:
            conn.close()


@app.route('/api/flights/search')
def search_flights():
    day = request.args.get('day')
    src = request.args.get('src')
    dst = request.args.get('dst')
    if not day or not src or not dst:
        return jsonify({"error": "Missing required parameters: day, src, dst"}), 400
    if day.lower() not in VALID_DAYS:
        return jsonify({"error": "Invalid day. Must be one of: " + ", ".join(VALID_DAYS)}), 400
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        day_col = sql.Identifier(day.lower())
        query = sql.SQL(
            "SELECT flight_code FROM flight_time_table NATURAL JOIN availability_code WHERE {day_col} = true AND src_airport_code = %s AND des_airport_code = %s"
        ).format(day_col=day_col)
        cur.execute(query, (src, dst))
        rows = cur.fetchall()
        cur.close()
        flights = [{"flight_code": row[0]} for row in rows]
        return jsonify({"flights": flights})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


@app.route('/api/flights/prices')
def flight_prices():
    src = request.args.get('src')
    dst = request.args.get('dst')
    if not src or not dst:
        return jsonify({"error": "Missing required parameters: src, dst"}), 400
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT flight_code, class, cost FROM prices NATURAL JOIN flight_time_table WHERE src_airport_code = %s AND des_airport_code = %s GROUP BY class, flight_code",
            (src, dst)
        )
        rows = cur.fetchall()
        cur.close()
        prices = [{"flight_code": row[0], "class": row[1], "cost": row[2]} for row in rows]
        return jsonify({"prices": prices})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


@app.route('/api/flights/delays')
def flight_delays():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT get_delay();")
        rows = cur.fetchall()
        cur.close()
        delays = [row[0] for row in rows]
        return jsonify({"delays": delays})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


@app.route('/api/flights/<flight_code>')
def get_flight(flight_code):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT flight_code, duration_in_hours, sch_dep_time, sch_arr_terminal, sch_dep_terminal, flight_type, src_airport_code, des_airport_code, day_code, aircraft_type, airline_code FROM flight_time_table WHERE flight_code = %s",
            (flight_code,)
        )
        row = cur.fetchone()
        cur.close()
        if row is None:
            return jsonify({"error": "Flight not found"}), 404
        flight = {
            "flight_code": row[0],
            "duration_in_hours": row[1],
            "sch_dep_time": str(row[2]),
            "sch_arr_terminal": row[3],
            "sch_dep_terminal": row[4],
            "flight_type": row[5],
            "src_airport_code": row[6],
            "des_airport_code": row[7],
            "day_code": row[8],
            "aircraft_type": row[9],
            "airline_code": row[10]
        }
        return jsonify({"flight": flight})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


@app.route('/api/passengers/immigrants')
def passenger_immigrants():
    date = request.args.get('date')
    airport = request.args.get('airport')
    if not date or not airport:
        return jsonify({"error": "Missing required parameters: date, airport"}), 400
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT passenger_name FROM (SELECT * FROM (SELECT * FROM booking WHERE visatype = 'Immigrant' AND exp_arr_date = %s) AS r NATURAL JOIN flight_time_table WHERE des_airport_code = %s) AS r2 NATURAL JOIN passenger",
            (date, airport)
        )
        rows = cur.fetchall()
        cur.close()
        passengers = [{"passenger_name": row[0]} for row in rows]
        return jsonify({"passengers": passengers})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


@app.route('/api/passengers/bookings')
def passenger_bookings():
    date = request.args.get('date')
    src = request.args.get('src')
    dst = request.args.get('dst')
    if not date or not src or not dst:
        return jsonify({"error": "Missing required parameters: date, src, dst"}), 400
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT passenger_id FROM booking NATURAL JOIN flight_time_table WHERE exp_dep_date = %s AND src_airport_code = %s AND des_airport_code = %s",
            (date, src, dst)
        )
        rows = cur.fetchall()
        cur.close()
        bookings = [{"passenger_id": row[0]} for row in rows]
        return jsonify({"bookings": bookings})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


@app.route('/api/passengers/frequent')
def frequent_flyers():
    min_bookings = request.args.get('min_bookings', '1')
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT airlines.airline_name, passenger_name, count(pnr) FROM booking NATURAL JOIN flight_time_table NATURAL JOIN airlines NATURAL JOIN passenger GROUP BY passenger.passenger_id, airlines.airline_code HAVING count(pnr) > %s",
            (int(min_bookings),)
        )
        rows = cur.fetchall()
        cur.close()
        frequent = [{"airline_name": row[0], "passenger_name": row[1], "booking_count": row[2]} for row in rows]
        return jsonify({"frequent_flyers": frequent})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


@app.route('/api/airports/maintenance')
def airport_maintenance():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT airport_code, airport_name, mx FROM (SELECT airport_code, max(check_date) AS mx FROM runway_maintenance GROUP BY airport_code) AS r NATURAL JOIN airport ORDER BY mx DESC"
        )
        rows = cur.fetchall()
        cur.close()
        maintenance = [{"airport_code": row[0], "airport_name": row[1], "last_check_date": str(row[2])} for row in rows]
        return jsonify({"maintenance": maintenance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


@app.route('/api/aircraft/old')
def old_aircraft():
    airline = request.args.get('airline')
    min_years = request.args.get('min_years')
    if not airline or not min_years:
        return jsonify({"error": "Missing required parameters: airline, min_years"}), 400
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM physical_instance_of_aircraft WHERE airline_code = %s AND DATE_PART('year', now()::date) - DATE_PART('year', manufacturing_date::date) > %s",
            (airline, int(min_years))
        )
        rows = cur.fetchall()
        cur.close()
        aircraft = [{"aircraft_no": row[0], "manufacturing_date": str(row[1]), "aircraft_type": row[2], "airline_code": row[3]} for row in rows]
        return jsonify({"aircraft": aircraft})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
