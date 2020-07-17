#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request
from flask_restful import Api
import json
from database import database as db
from templates import decorator_serverboot

app = Flask(__name__)
api = Api(app)
app.secret_key = "vth"
decorator_serverboot.decorate()


def read_json_file(json_file):
    """Read *.json files"""
    with open(json_file, 'r') as _metrics:
        return json.load(_metrics)


metrics = read_json_file('metrics.json')


# class SecretKey(Resource):
#     def get(self):
#         return app.secret_key
#
#
# api.add_resource(SecretKey, '/secretKey')

# todos = {}
#
#
# class TodoSimple(Resource):
#     def get(self, todo_id):
#         return {todo_id: todos[todo_id]}
#
#     def put(self, todo_id):
#         todos[todo_id] = request.form['data']
#         return {todo_id: todos[todo_id]}
#
#
# api.add_resource(TodoSimple, '/<string:todo_id>')


@app.route('/')
def init_dashboard():
    return render_template("dashboard.html")


@app.errorhandler(404)
def not_found():
    message = {
        'status': 404,
        'message': 'Not found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(500)
def internal_server_error():
    mess = {
        "status": 500,
        "message": "Internal server error at " + request.url
    }
    resp = jsonify(mess)
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
