import mysql.connector
import json
import datetime

from flask import jsonify

import DTO

query_get_all_history_sensor = "select * from history_sensor;"
query_get_all_gas_sensor = "select * from gas_sensor;"
query_get_all_sensor_loc = "select * from sensor_loc;"
query_get_all_device = "SELECT * FROM DEVICE;"
query_get_all_smoke_sensor = "SELECT * FROM smoke_sensor;"
query_get_all_temp_sensor = "SELECT * FROM temp_sensor;"

query_insert_device = "INSERT INTO DEVICE (device_name, device_type, device_loc_id, smoke_id, gas_id, temp_id) " \
                      "VALUES{};"
query_insert_smoke_sensor = "insert into smoke_sensor(smoke_name, loc_id)values{};"
query_insert_sensor_loc = "insert into sensor_loc(loc_name) values{};"
query_insert_temp_sensor = "insert into temp_sensor(temp_name, loc_id) values{};"
query_insert_gas_sensor = "insert into gas_sensor(gas_name, loc_id) values{};"
query_insert_history_sensor = "insert into history_sensor(device_id, temp_reading, smoke_reading, gas_reading, " \
                              "date_reading, temp_id, smoke_id, gas_id) values{}; "


def init_db(host, user, pw, _db):
    """MySQL database initialization"""
    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=pw,
            database=_db,
            auth_plugin='mysql_native_password'
        )
    except mysql.connector.Error as err:
        print("The connection to the MySQL database was interrupted.\n"
              "Error found: {}".format(err))
        return err


# init db
db_host = "localhost"
db_user = "root"
db_password = "IFA$T123"
db_database = "ifast_resource"
db = init_db(db_host, db_user, db_password, db_database)


def default(o):
    """Serializes date format to JSON"""
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def handle_select_query(query, dto):
    """Perform the QUERY and return an DTO json object"""
    cursor = db.cursor()
    cursor.execute(query)
    db_results = cursor.fetchall()

    if dto is not None:
        container = {}
        for row in db_results:
            for i in range(len(dto)):
                default(row[i])
                container.update({dto[i]: row[i]})
        cursor.close()
        db.rollback()
        # return json.dumps(container, default=default)
        return container
    else:
        cursor.close()
        db.rollback()
        return return_message("Nothing was run")


def return_message(String):
    return {"message": String}


def handle_insert_query(query, *args):
    """Run an insert query, with *args as values in the sql command VALUES()"""
    cursor = db.cursor()
    cursor.execute(query.format(args))

    cursor.close()
    # save changes
    db.commit()
    return cursor.statement


# Insert queries
def insert_device(device_name, device_type, device_loc_id, smoke_id, gas_id, temp_id):
    handle_insert_query(query_insert_device, device_name, device_type, device_loc_id, smoke_id, gas_id, temp_id)
    return return_message("A device was added")


def insert_smoke_sensor(smoke_name, loc_id):
    handle_insert_query(query_insert_smoke_sensor, smoke_name, loc_id)
    return return_message("A smoke sensor was added")


def insert_sensor_loc(loc_name):
    handle_insert_query(query_insert_sensor_loc, loc_name)
    return return_message("A sensor's location was added")


def insert_temp_sensor(temp_name, loc_id):
    handle_insert_query(query_insert_temp_sensor, temp_name, loc_id)
    return return_message("A temperature sensor was added")


def insert_gas_sensor(gas_name, loc_id):
    handle_insert_query(query_insert_gas_sensor, gas_name, loc_id)
    return return_message("A gas sensor was added")


def insert_history_sensor(device_id, temp_reading, smoke_reading, gas_reading, date_reading, temp_id, smoke_id, gas_id):
    handle_insert_query(query_insert_history_sensor, device_id, temp_reading, smoke_reading, gas_reading, date_reading,
                        temp_id, smoke_id, gas_id)
    return return_message("A sensor's history was added")


# GET queries
def get_all_history_sensor():
    return handle_select_query(query_get_all_history_sensor, DTO.get_dto_history_sensor())


def get_all_gas_sensor():
    return handle_select_query(query_get_all_gas_sensor, DTO.get_dto_gas_sensor())


def get_all_device():
    return handle_select_query(query_get_all_device, DTO.get_dto_device())


def get_all_sensor_loc():
    return handle_select_query(query_get_all_sensor_loc, DTO.get_dto_sensor_loc())


def get_all_smoke_sensor():
    return handle_select_query(query_get_all_smoke_sensor, DTO.get_dto_smoke_sensor())


def get_all_temp_sensor():
    return handle_select_query(query_get_all_temp_sensor, DTO.get_dto_temp_sensor())
