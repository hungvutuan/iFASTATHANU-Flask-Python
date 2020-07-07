#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_restful import Resource, Api
import metrics
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)
app.secret_key = "vth"

# db config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'IFA$T123'
app.config['MYSQL_DB'] = 'iFASTATHANU'

mysql = MySQL(app)

class SecretKey(Resource):
    def get(self):
        return app.secret_key


api.add_resource(SecretKey, '/secretKey')

todos = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


api.add_resource(TodoSimple, '/<string:todo_id>')


@app.route('/')
def init_dashboard():
    return render_template("dashboard.html")


@app.route('/live', methods=['GET', 'POST'])
def init(deviceName):
    if request.method == 'GET':
        device = request.args.get('device', default="", type=int)
        metrics[deviceName] = device
        return metrics


if __name__ == '__ main__':
    app.run(host='localhost', debug=True, threaded=True)
