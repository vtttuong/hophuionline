from ast import Str
import imp
from typing import List
from xmlrpc.client import Boolean
import psycopg2
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from user import *
from hui_group import *


app = Flask(__name__)

CORS(app)


def result_template(is_success: Boolean, results: List, msg: Str = ''):
    return jsonify({
        "is_success": is_success,
        "results": results,
        "msg": msg
    })


API_PREFIX = '/api/v1'


@app.route("/")
def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.8 (from the example template)"


def get_db_conn():
    return psycopg2.connect(
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), sslmode=os.getenv("DB_SSL_MODE")
    )


@app.route(f'{API_PREFIX}/user_info/<user_id>', methods=['GET'])
def get_user_info(user_id):
    try:
        user_info = UserInfo.get_user_info(user_id, get_db_conn)
        return result_template(True, [])
    except BaseException as e:
        return result_template(False, [], str(e))


@app.route(f'{API_PREFIX}/user_info', methods=['POST'])
def create_user():
    try:
        user_info = UserInfo.convert_from_json(request.json)
        user_info.create_user(get_db_conn)
        return result_template(True, [])
    except BaseException as e:
        return result_template(False, [], str(e))


@app.route(f'{API_PREFIX}/hui/<user_id>', methods=['GET'])
def get_hui_groups(user_id):
    try:
        result = HuiGroup.get_hui_groups(user_id,get_db_conn)
        return result_template(True, result)
    except BaseException as e:
        return result_template(False, [], str(e))    


@app.route(f'{API_PREFIX}/hui/<user_id>', methods=['POST'])
def create_hui_group(user_id):
    try:
        request.json['owner_id'] = user_id
        hui_group = HuiGroup.convert_from_json(request.json)
        hui_group.create_hui_group(get_db_conn)
        return result_template(True, [])
    except BaseException as e:
        return result_template(False, [], str(e))


@app.route(f'{API_PREFIX}/hui/invite', methods=['POST'])
def invite_to_join_hui_group():
    user_id = request.json['user_id']
    hui_id = request.json['hui_id']
    status , msg =HuiGroup.invite_user(user_id,hui_id,get_db_conn)
    if status == True:
        return result_template(True, [])
    else:
        return result_template(False, [], str(msg))


@app.route("/db_version")
def db_version():

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("select version()")
     
    data = cursor.fetchone()

    # please close conn manually
    conn.close()

    return f"Connection established to: {data}"


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=8088)
