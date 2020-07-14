#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api
import json
import database
import decorator_serverboot

app = Flask(__name__)
api = Api(app)
app.secret_key = "vth"

print(database.get_all_history_sensor())

# Read .json files
with open('metrics.json', 'r') as _metrics:
    metrics = json.load(_metrics)
# print("Metrics:")
# for metric in metrics:
#     print(metric)


class SecretKey(Resource):
    def get(self):
        return app.secret_key


api.add_resource(SecretKey, '/secretKey')

todos = {}


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
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.route('/metrics', methods=['GET', 'POST'])
def init(device_name=None):
    if request.method == 'GET':
        return jsonify(metrics)


if __name__ == '__ main__':
    app.run(host='localhost', debug=True, threaded=True)
