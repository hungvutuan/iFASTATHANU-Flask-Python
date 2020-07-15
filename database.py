import mysql.connector
import json
import datetime
import DTO

query_get_all_history_sensor = "select * from history_sensor"
query_get_all_gas_sensor = "select * from gas_sensor"
query_get_all_sensor_loc = "select * from sensor_loc"
query_get_all_device = "SELECT * FROM DEVICE"
query_get_all_smoke_sensor = "SELECT * FROM smoke_sensor"
query_get_all_temp_sensor = "SELECT * FROM temp_sensor"


def init_db(host, user, pw, _db):
    """MySQL database initialization"""
    return mysql.connector.connect(
        host=host,
        user=user,
        password=pw,
        database=_db
    )


# init db
db = init_db("localhost", "root", "IFA$T123", "ifast_resource")


def default(o):
    """Serializes date format to JSON"""
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def handle_return(query, dto):
    """Perform the QUERY and return an DTO json object"""
    cursor = db.cursor()
    cursor.execute(query)
    db_results = cursor.fetchall()

    container = {}
    for row in db_results:
        for i in range(len(dto)):
            default(row[i])
            container.update({dto[i]: row[i]})

    cursor.close()
    db.rollback()
    # return json.dumps(container, default=default)
    return container


def get_all_history_sensor():
    return handle_return(query_get_all_history_sensor, DTO.get_dto_history_sensor())


def get_all_gas_sensor():
    return handle_return(query_get_all_gas_sensor, DTO.get_dto_gas_sensor())


def get_all_device():
    return handle_return(query_get_all_device, DTO.get_dto_device())


def get_all_sensor_loc():
    return handle_return(query_get_all_sensor_loc, DTO.get_dto_sensor_loc())


def get_all_smoke_sensor():
    return handle_return(query_get_all_smoke_sensor, DTO.get_dto_smoke_sensor())


def get_all_temp_sensor():
    return handle_return(query_get_all_temp_sensor, DTO.get_dto_temp_sensor())
