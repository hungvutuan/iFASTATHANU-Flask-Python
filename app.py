#!/usr/bin/env python
# coding: utf-8
import os

from flask import Flask, render_template, jsonify, request, send_from_directory, abort
import json

from mysql.connector import DatabaseError

from database import database as db
from templates import decorator_serverboot

app = Flask(__name__)
app.secret_key = "4,\x178sg\xde=U=\xa7\xe5Hr\x11\xaf"
decorator_serverboot.decorate()


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


@app.route('/metrics/all', methods=['GET', 'POST'])
def get_all_metrics():
    if request.method == 'GET':
        return jsonify(metrics)


@app.route('/history/all', methods=['GET'])
def get_all_history():
    if request.method == 'GET':
        return db.get_all_history_sensor()


@app.route('/history/', methods=['GET'])
def get_history_by_id():
    if request.method == 'GET':
        history_id = request.args.get("history_id")
        return db.get_history_sensor_by_id(history_id)


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


@app.route('/sensors/history/', methods=['POST'])
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


@app.route("/devices/delete", methods=['DELETE'])
def delete_device():
    try:
        device_id = request.args.get("device_id")
        return db.delete_device(device_id)
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
