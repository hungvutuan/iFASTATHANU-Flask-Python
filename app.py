#!/usr/bin/env python
import os

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
from database import database as db
from templates import decorator_serverboot

app = Flask(__name__)
app.secret_key = "vth"
decorator_serverboot.decorate()


def read_json_file(json_file):
    """Read *.json files"""
    with open(json_file, 'r') as _metrics:
        return json.load(_metrics)


metrics = read_json_file('metrics.json')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


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
    resp = jsonify({
        'status': 404,
        'message': 'Not found: ' + request.url,
        'error': error
    })
    resp.status_code = 404
    return resp


@app.errorhandler(500)
def error_internal_server_error(error=None):
    resp = jsonify({
        "status": 500,
        "message": "Internal server error at " + request.url,
        "error": error
    })
    resp.status_code = 500
    return resp


@app.route('/metrics', methods=['GET', 'POST'])
def get_metrics():
    if request.method == 'GET':
        return jsonify(metrics)


@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'GET':
        return db.get_all_history_sensor()


if __name__ == '__ main__':
    app.run(host='localhost', threaded=True)
