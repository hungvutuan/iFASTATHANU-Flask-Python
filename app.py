#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, jsonify, request
import json
import sys
from mysql.connector import DatabaseError
from Client import client
from database import database as db
from bin import decorator_serverboot as decorator, global_var

app = Flask(__name__)
app.secret_key = "4,\x178sg\xde=U=\xa7\xe5Hr\x11\xaf"
decorator.decorate()

# Confirm that we're using Python 3
assert sys.version_info.major == 3, global_var.get_error_python_version()


def connect_sensors():
    client.loop_start()
    client.connect("test.mosquitto.org", 1883, 60)
    client.disconnect()
    client.loop_stop()

#

def read_json_file(json_file):
    """Read *.json files"""
    with open(json_file, 'r') as _metrics:
        return json.load(_metrics)


metrics = read_json_file('metrics.json')


@app.route('/')
def init_dashboard():
    return render_template("dashboard.html")


@app.errorhandler(400)
def error_bad_request():
    resp = jsonify({
        'status': 400,
        'message': 'Bad Request'
    })
    resp.status_code = 400
    return resp


@app.errorhandler(401)
def error_unauthorized():
    resp = jsonify({
        'status': 401,
        'message': 'Unauthorized Connection'
    })
    resp.status_code = 401
    return resp


@app.errorhandler(403)
def error_bad_request():
    resp = jsonify({
        'status': 403,
        'message': 'Forbidden Access'
    })
    resp.status_code = 403
    return resp


@app.errorhandler(409)
def error_conflict():
    resp = jsonify({
        'status': 409,
        'message': 'Conflict'
    })
    resp.status_code = 409
    return resp


@app.errorhandler(404)
def error_not_found(error=None):
    return render_template("error_404.html"), 404


@app.errorhandler(405)
def error_method_not_allowed(error=None):
    return render_template("error_405.html"), 405


@app.errorhandler(500)
def error_internal_server_error(error=None):
    return render_template("error_500.html"), 500


# Get/Select
@app.route('/metrics', methods=['GET', 'POST'])
def get_all_metrics():
    if request.method == 'GET':
        try:
            return jsonify(metrics)
        except:
            return db.return_message(None)


@app.route('/sensors/history', methods=['GET'])
def get_history():
    try:
        if request.method == 'GET':
            history_id = request.args.get("id")
            if history_id is None:
                return db.get_all_history_sensor()
            else:
                return db.get_history_sensor_by_id(history_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route('/sensors/gas', methods=['GET'])
def get_gas_sensor():
    try:
        gas_id = request.args.get("id")
        if gas_id is None:
            return db.get_all_gas_sensor()
        else:
            return db.get_gas_sensor_by_id(gas_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route('/sensors/smoke', methods=['GET'])
def get_smoke_sensor():
    try:
        smoke_id = request.args.get("id")
        if smoke_id is None:
            return db.get_all_smoke_sensor()
        else:
            return db.get_smoke_sensor_by_id(smoke_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route('/sensors/temp', methods=['GET'])
def get_temp_sensor():
    try:
        temp_id = request.args.get("id")
        if temp_id is None:
            return db.get_all_temp_sensor()
        else:
            return db.get_temp_sensor_by_id(temp_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route('/sensors/loc', methods=['GET'])
def get_sensor_loc():
    try:
        loc_id = request.args.get("id")
        if loc_id is None:
            return db.get_all_sensor_loc()
        else:
            return db.get_sensor_loc_by_id(loc_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route('/devices', methods=['GET'])
def get_device():
    try:
        device_id = request.args.get("id")
        if device_id is None:
            return db.get_all_device()
        else:
            return db.get_device_by_id(device_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


# Add/Insert
@app.route('/devices/', methods=['POST'])
def insert_device():
    if request.method == 'POST':
        try:
            device_name = request.args.get("deviceName")
            device_type = request.args.get("type")
            device_loc_id = request.args.get("locId")
            smoke_id = request.args.get("smokeId")
            gas_id = request.args.get("gasId")
            temp_id = request.args.get("tempId")
            return db.insert_device(device_name, device_type, device_loc_id, smoke_id, gas_id, temp_id)
        except DatabaseError as e:
            app.logger.exception(e)
            return db.get_fail_db_message()


@app.route('/sensors/smoke/', methods=['POST'])
def insert_smoke_sensor():
    try:
        smoke_name = request.args.get("smoke_name")
        loc_id = request.args.get("loc_id")
        return db.insert_smoke_sensor(smoke_name, loc_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route('/sensors/loc/', methods=['POST'])
def insert_loc_sensor():
    try:
        loc_name = request.args.get("loc_name")
        return db.insert_sensor_loc(loc_name)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route('/sensors/gas/', methods=['POST'])
def insert_gas_sensor():
    try:
        gas_name = request.args.get("gas_name")
        loc_id = request.args.get("loc_id")
        return db.insert_gas_sensor(gas_name, loc_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route('/sensors/temp/', methods=['POST'])
def insert_temp_sensor():
    try:
        temp_name = request.args.get("temp_name")
        loc_id = request.args.get("loc_id")
        return db.insert_temp_sensor(temp_name, loc_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route('/sensors/history', methods=['POST'])
def insert_history_sensor():
    try:
        device_id = request.args.get("device_id")
        temp_reading = request.args.get("temp_reading")
        smoke_reading = request.args.get("smoke_reading")
        gas_reading = request.args.get("gas_reading")
        date_reading = request.args.get("date_reading")
        temp_id = request.args.get("temp_id")
        smoke_id = request.args.get("smoke_id")
        gas_id = request.args.get("gas_id")
        return db.insert_history_sensor(device_id, temp_reading, smoke_reading, gas_reading, date_reading, temp_id,
                                        smoke_id, gas_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


# Delete by id
@app.route("/devices", methods=['DELETE'])
def delete_device():
    try:
        device_id = request.args.get("id")
        return db.delete_device_by_id(device_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route("/sensors/history", methods=['DELETE'])
def delete_history():
    try:
        history_id = request.args.get("id")
        return db.delete_history_sensor_by_id(history_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route("/sensors/gas", methods=['DELETE'])
def delete_sensor_gas():
    try:
        gas_id = request.args.get("id")
        return db.delete_gas_sensor_by_id(gas_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route("/sensors/smoke", methods=['DELETE'])
def delete_sensor_smoke():
    try:
        smoke_id = request.args.get("id")
        return db.delete_smoke_sensor_by_id(smoke_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route("/sensors/temp", methods=['DELETE'])
def delete_sensor_temp():
    try:
        temp_id = request.args.get("id")
        return db.delete_temp_sensor_by_id(temp_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.route("/sensors/loc", methods=['DELETE'])
def delete_sensor_loc():
    try:
        loc_id = request.args.get("id")
        return db.delete_sensor_loc_by_id(loc_id)
    except DatabaseError as e:
        app.logger.exception(e)
        return db.get_fail_db_message()


@app.after_request
def add_header(resp):
    resp.headers['Allow'] = "POST, GET"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__ main__':
    app.run(host='localhost', threaded=True, debug=True)
