import json
import os
import psycopg2

QUERIES = {
    1: "select passenger_name from (Select * from (select * from booking where visatype = 'Immigrant' and exp_arr_date = '{}') as r natural join flight_time_table where des_airport_code = '{}') as r2  natural join passenger ;",
    2: "SELECT get_delay();",
    3: "select * from physical_instance_of_aircraft where  airline_code = '{}' and DATE_PART('year',now()::date)- DATE_PART('year',manufacturing_date::date)>{};",
    4: "select passenger_id from booking natural join flight_time_table where exp_dep_date = '{}' and src_airport_code = '{}' and des_airport_code = '{}';",
    5: "select flight_time_table.flight_code from flight_time_table natural join availability_code where {}=true and src_airport_code = '{}' and des_airport_code = '{}';",
    6: "select flight_code,class,cost from prices natural join flight_time_table where src_airport_code = '{}' and des_airport_code = '{}' group by (class,flight_code);",
    7: "select airport_code,airport_name,mx from (select airport_code,max(check_date) as mx from runway_maintenance group by airport_code)as r natural join airport order by mx desc;",
    8: "select count(pnr) from (select * from flight_time_table natural join actual_arr_dep where src_airport_code = '{}' or des_airport_code = 'DEL') as r natural join booking where date(dep_timestamp) >= '{}' and date(dep_timestamp) <= '{}' and date(arr_timestamp) >= '{}' and date(arr_timestamp) >= '{}';",
    9: "select airlines.airline_name,passenger_name,count(pnr) from booking natural join flight_time_table natural join airlines natural join passenger group by passenger.passenger_id,airlines.airline_code having count(pnr)>{};",
}


def lambda_handler(event, context):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            host=os.environ["DB_HOST"],
            password=os.environ["DB_PASS"],
            port=os.environ.get("DB_PORT", "5432"),
        )
        cursor = conn.cursor()
        cursor.execute("SET search_path TO airport_atc;")

        action = event.get("action")

        if action == "execute":
            query = event["query"]
            cursor.execute(query)
            results = cursor.fetchall()
        elif action == "query":
            query_id = int(event["query_id"])
            params = event.get("params", [])
            sql = QUERIES[query_id].format(*params)
            cursor.execute(sql)
            results = cursor.fetchall()
        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid action"})}

        conn.commit()
        return {
            "statusCode": 200,
            "body": json.dumps({"results": [list(row) for row in results]}, default=str),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    finally:
        if conn:
            conn.close()
