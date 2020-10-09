#!/usr/bin/env python
# coding: utf-8
import sys
import threading
from datetime import date

from flask_cors import CORS, cross_origin
from flask import Flask, render_template, jsonify, request
from mysql.connector import DatabaseError
from werkzeug.exceptions import InternalServerError

from AI import engine
from Client import *
from bin import decorator_serverboot as decorator, global_var as VAR
from database import database as db

app = Flask(__name__)
app.secret_key = "4,\x178sg\xde=U=\xa7\xe5Hr\x11\xaf"
decorator.decorate()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Confirm that we're using Python 3
assert sys.version_info.major == 3, VAR.get_error_python_version()


def connect_sensors():
    client.loop_start()
    val = client.connect("test.mosquitto.org", 1883, 60)
    client.disconnect()
    client.loop_stop()
    return val


def get_current_time():
    return time.strftime("%H:%M:%S", time.localtime())


def get_current_date():
    return date.today().strftime("%Y-%m-%d")


def read_json_file(json_file):
    """Read *.json files"""
    with open(json_file, 'r') as _metrics:
        return json.load(_metrics)


metrics = read_json_file('metrics.json')


@app.route('/')
@cross_origin()
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
        except Exception:
            raise InternalServerError


@app.route('/live/kitchen', methods=['GET'])
def get_live_kitchen_metrics():
    try:
        # current_time = get_current_time()
        # sensor_data_kitchen["current_time"] = current_time
        return jsonify(sensor_data_kitchen)
    except Exception:
        raise InternalServerError


@app.route('/live/bedroom', methods=['GET'])
def get_live_bedroom_metrics():
    try:
        # current_time = get_current_time()
        # sensor_data_kitchen["current_time"] = current_time
        return jsonify(sensor_data_bedroom)
    except Exception:
        raise InternalServerError


@app.route('/live/livingroom', methods=['GET'])
def get_live_livingroom_metrics():
    try:
        # current_time = get_current_time()
        # sensor_data_kitchen["current_time"] = current_time
        return jsonify(sensor_data_living)
    except Exception:
        raise InternalServerError


@app.route('/history', methods=['GET'])
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
        raise InternalServerError


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
        raise InternalServerError


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
        raise InternalServerError


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
        raise InternalServerError


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
        raise InternalServerError


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
        raise InternalServerError


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
            raise InternalServerError


@app.route('/sensors/smoke/', methods=['POST'])
def insert_smoke_sensor():
    try:
        smoke_name = request.args.get("smoke_name")
        loc_id = request.args.get("loc_id")
        return db.insert_smoke_sensor(smoke_name, loc_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route('/sensors/loc/', methods=['POST'])
def insert_loc_sensor():
    try:
        loc_name = request.args.get("loc_name")
        return db.insert_sensor_loc(loc_name)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route('/sensors/gas/', methods=['POST'])
def insert_gas_sensor():
    try:
        gas_name = request.args.get("gas_name")
        loc_id = request.args.get("loc_id")
        return db.insert_gas_sensor(gas_name, loc_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route('/sensors/temp/', methods=['POST'])
def insert_temp_sensor():
    try:
        temp_name = request.args.get("temp_name")
        loc_id = request.args.get("loc_id")
        return db.insert_temp_sensor(temp_name, loc_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route('/history', methods=['POST'])
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
        if request.args.get("alarm_id") is not None:
            alarm_id = request.args.get("alarm_id")
        else:
            alarm_id = 1  # alarm 1 means auto
        return db.insert_history_sensor(device_id, temp_reading, smoke_reading, gas_reading, date_reading, temp_id,
                                        smoke_id, gas_id, alarm_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


# Delete by id
@app.route("/devices", methods=['DELETE'])
def delete_device():
    try:
        device_id = request.args.get("id")
        return db.delete_device_by_id(device_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route("/history", methods=['DELETE'])
def delete_history():
    try:
        history_id = request.args.get("id")
        return db.delete_history_sensor_by_id(history_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route("/sensors/gas", methods=['DELETE'])
def delete_sensor_gas():
    try:
        gas_id = request.args.get("id")
        return db.delete_gas_sensor_by_id(gas_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route("/sensors/smoke", methods=['DELETE'])
def delete_sensor_smoke():
    try:
        smoke_id = request.args.get("id")
        return db.delete_smoke_sensor_by_id(smoke_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route("/sensors/temp", methods=['DELETE'])
def delete_sensor_temp():
    try:
        temp_id = request.args.get("id")
        return db.delete_temp_sensor_by_id(temp_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route("/sensors/loc", methods=['DELETE'])
def delete_sensor_loc():
    try:
        loc_id = request.args.get("id")
        return db.delete_sensor_loc_by_id(loc_id)
    except DatabaseError as e:
        app.logger.exception(e)
        raise InternalServerError


@app.route("/piechart", methods=['GET'])
def get_pie():
    try:
        return db.get_pie_chart()
    except Exception:
        raise InternalServerError


@app.route("/barchart", methods=['GET'])
def get_bar_chart():
    try:
        cur_month = int(get_current_date().split("-")[1])
        return db.get_bar_chart(cur_month)
    except Exception:
        raise InternalServerError


class LiveInput(threading.Thread):
    """Retrieve the input from the 3 pairs of sensors with a delay.
    Description: This class is never called by the API. It loops forever.
    Purpose: Request the inputs in the background, and pass to the ML engine.
    If high chance of fire -> send notification to mobile."""

    def __init__(self, delay):
        threading.Thread.__init__(self)
        self.delay = delay

    def run(self):
        while True:
            # get values from sensors
            engine.check_input({
                "kitchen": sensor_data_kitchen,
                "bedroom": sensor_data_bedroom,
                "living": sensor_data_living
            })
            time.sleep(self.delay)


retrieve_input = LiveInput(VAR.DELAY_LIVE_INPUT)
retrieve_input.start()


# out of scope
@app.route("/notification/firebase", methods=['POST'])
def notification():
    try:
        return db.return_message("Noti sent")
    except Exception:
        raise InternalServerError


@app.route("/prediction/kitchen", methods=['GET'])
def get_kitchen_percentage():
    try:
        return engine.live_percentage("kitchen", sensor_data_kitchen)
    except Exception:
        raise InternalServerError


@app.route("/prediction/bedroom", methods=['GET'])
def get_bedroom_percentage():
    try:
        return engine.live_percentage("bedroom", sensor_data_bedroom)
    except Exception:
        raise InternalServerError


@app.route("/prediction/living", methods=['GET'])
def get_living_percentage():
    try:
        return engine.live_percentage("living", sensor_data_living)
    except Exception:
        raise InternalServerError


@app.route("/prediction", methods=["GET"])
def get_mean_percentage():
    try:
        return jsonify(engine.mean_live_percentage(sensor_data_kitchen, sensor_data_bedroom, sensor_data_living))
    except Exception:
        raise InternalServerError


@app.route("/notification/feedback", methods=['POST'])
@cross_origin()
def get_user_feedback():
    try:
        data = request.get_json()
        if not data['status']:
            res = engine.feedback(data)
            if res:
                return db.return_message("Dataset updated and the model changed")
            else:
                raise Exception
        else:
            return db.return_message("Dataset and model unchanged")
    except Exception:
        raise InternalServerError


@app.after_request
def add_header(resp):
    resp.headers['Allow'] = "POST, GET, DELETE, OPTIONS"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/shutdown', methods=['POST'])
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


if __name__ == '__ main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
