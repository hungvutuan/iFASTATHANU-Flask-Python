import mysql.connector
import json
import datetime

query_get_all_history_sensor = "select * from history_sensor"
query_get_all_gas_sensor = "select * from gas_sensor"


def init_db(host, user, pw, _db):
    """database init"""
    return mysql.connector.connect(
        host=host,
        user=user,
        password=pw,
        database=_db
    )


db = init_db("localhost", "root", "IFA$T123", "ifast_resource")


# cursor = db.cursor()

# print all history sensor
# cursor.execute("select * from history_sensor")
# for c in cursor:
#     print(c)

def default(o):
    """Serializes date format to JSON"""
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def get_all_history_sensor():
    cursor = db.cursor()
    cursor.execute(query_get_all_history_sensor)
    # for c in cursor:
    #     print(c)
    #     dict_return_val.append(c)
    #
    # for i in range(len(dict_return_val)):
    #     json_return_val = {
    #         "history_id": [dict_return_val[0]],
    #         "device_id": [dict_return_val[1]]
    #     }
    # print(json.dumps(json_return_val))
    res = cursor.fetchall()
    return_res = json.dumps(res, sort_keys=True, default=default)
    
    cursor.close()
    db.rollback()
    return return_res


def get_all_gas_sensor():
    cursor = db.cursor()
    cursor.execute(query_get_all_gas_sensor)
