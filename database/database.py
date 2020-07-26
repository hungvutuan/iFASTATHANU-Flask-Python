import mysql.connector
import json
import datetime
from flask import jsonify
import DTO

# select all
query_get_all_history_sensor = "select * from history_sensor;"
query_get_all_gas_sensor = "select * from gas_sensor;"
query_get_all_sensor_loc = "select * from sensor_loc;"
query_get_all_device = "SELECT * FROM DEVICE;"
query_get_all_smoke_sensor = "SELECT * FROM smoke_sensor;"
query_get_all_temp_sensor = "SELECT * FROM temp_sensor;"

# select by id
query_get_history_sensor_by_id = "select * from history_sensor where history_id = {};"
query_get_gas_sensor_by_id = "select * from device where device_id = {};"
query_get_smoke_sensor_by_id = "select * from smoke_sensor where smoke_id = {};"
query_get_temp_sensor_by_id = "select * from temp_sensor where temp_id = {};"
query_get_sensor_loc_by_id = "select * from sensor_loc where loc_id = {};"
query_get_device_by_id = "select * from device where device_id = {};"

# insert
query_insert_device = "INSERT INTO DEVICE (device_name, device_type, device_loc_id, smoke_id, gas_id, temp_id) " \
                      "VALUES{};"
query_insert_smoke_sensor = "insert into smoke_sensor(smoke_name, loc_id)values{};"
query_insert_sensor_loc = "insert into sensor_loc(loc_name) values{};"
query_insert_temp_sensor = "insert into temp_sensor(temp_name, loc_id) values{};"
query_insert_gas_sensor = "insert into gas_sensor(gas_name, loc_id) values{};"
query_insert_history_sensor = "insert into history_sensor(device_id, temp_reading, smoke_reading, gas_reading, " \
                              "date_reading, temp_id, smoke_id, gas_id) values{}; "

# delete
query_delete_device_by_id = "DELETE FROM device WHERE device_id = {} LIMIT 1;"
query_delete_smoke_sensor_by_id = "DELETE FROM smoke_sensor WHERE smoke_id = {} LIMIT 1;"
query_delete_sensor_loc_by_id = "DELETE FROM sensor_loc WHERE loc_id = {} LIMIT 1;"
query_delete_temp_sensor_by_id = "DELETE FROM temp_sensor WHERE temp_id = {} LIMIT 1;"
query_delete_gas_sensor_by_id = "DELETE FROM gas_sensor WHERE gas_id = {} LIMIT 1;"
query_delete_history_sensor_by_id = "DELETE FROM history_sensor WHERE history_id = {} LIMIT 1;"

fail_db_message = {"message": "Database error while sending query",
                   "success": False}


def get_fail_db_message():
    return fail_db_message


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


def handle_select_query(query, dto, *args):
    """Perform the QUERY and return an DTO json object
    If an argument is passed, it assumes that it is ID
    to fill in the query"""
    if dto is not None:
        cursor = db.cursor()

        # if no argument (i.e. id) is passed, perform the whole query
        if len(args) == 0:
            cursor.execute(query)
            db_results = cursor.fetchall()

        # else if an id is passed -> format the query and return only one line of values
        else:
            cursor.execute(query.format(args[0]))
            db_results = cursor.fetchall()
            if len(db_results) > 1:
                return_message(None)

        all_obj = []
        obj = {}
        for row in db_results:
            for i in range(len(row)):
                # default(row[i])
                obj.update({dto[i]: row[i]})
            all_obj.append(obj.copy())
        cursor.close()
        db.rollback()
        return jsonify(all_obj)
    else:
        return return_message(None)


def return_message(String):
    if String is None:
        return jsonify(
            {"success": False,
             "message": "Request unsuccessful"}
        )
    return jsonify(
        {"success": True,
         "message": String}
    )


def handle_insert_query(query, *args):
    """Run an insert query, with many params as values in the sql command VALUES()"""
    cursor = db.cursor()
    cursor.execute(query.format(args))

    cursor.close()
    # save changes
    db.commit()
    return cursor.statement


def handle_delete_query(query, arg):
    """Run a delete query, taking only one argument as the ID of the object/DTO"""
    c = db.cursor()
    c.execute(query.format(arg))

    c.close()
    db.commit()
    return c.statement


# DELETE queries
def delete_device_by_id(device_id):
    handle_delete_query(query_delete_device_by_id, device_id)
    return return_message("Device with ID " + str(device_id) + " was deleted")


def delete_smoke_sensor_by_id(smoke_id):
    handle_delete_query(query_delete_smoke_sensor_by_id, smoke_id)
    return return_message("Smoke sensor with ID " + str(smoke_id) + " was deleted")


def delete_sensor_loc_by_id(loc_id):
    handle_delete_query(query_delete_sensor_loc_by_id, loc_id)
    return return_message("Location with ID " + str(loc_id) + " was deleted")


def delete_temp_sensor_by_id(temp_id):
    handle_delete_query(query_delete_temp_sensor_by_id, temp_id)
    return return_message("Temperature sensor with ID " + str(temp_id) + " was deleted")


def delete_gas_sensor_by_id(gas_id):
    handle_delete_query(query_delete_gas_sensor_by_id, gas_id)
    return return_message("Gas sensor with ID " + str(gas_id) + " was deleted")


def delete_history_sensor_by_id(history_id):
    handle_delete_query(query_delete_history_sensor_by_id, history_id)
    return return_message("History with ID " + str(history_id) + " was deleted")


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


# GET by id
def get_history_sensor_by_id(history_id):
    return handle_select_query(query_get_history_sensor_by_id, DTO.get_dto_history_sensor(), history_id)


def get_gas_sensor_by_id(gas_id):
    return handle_select_query(query_get_gas_sensor_by_id, DTO.get_dto_gas_sensor(), gas_id)


def get_smoke_sensor_by_id(smoke_id):
    return handle_select_query(query_get_smoke_sensor_by_id, DTO.get_dto_smoke_sensor(), smoke_id)


def get_temp_sensor_by_id(temp_id):
    return handle_select_query(query_get_temp_sensor_by_id, DTO.get_dto_temp_sensor(), temp_id)


def get_sensor_loc_by_id(loc_id):
    return handle_select_query(query_get_sensor_loc_by_id, DTO.get_dto_sensor_loc(), loc_id)


def get_device_by_id(device_id):
    return handle_select_query(query_get_device_by_id, DTO.get_dto_device(), device_id)
