from ast import Str
import imp
from typing import List
from xmlrpc.client import Boolean
import psycopg2
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from giat_hui_log import GiatHuiLog
from user import *
from hui_group import *
from transactions import *

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


# Get user info by user id
@app.route(f'{API_PREFIX}/user_info/<user_id>', methods=['GET'])
def get_user_info(user_id):
  try:
    user_info = UserInfo.get_user_info(user_id, get_db_conn)
    return result_template(True, [])
  except BaseException as e:
    return result_template(False, [], str(e))


# Find all users by phone number
@app.route(f'{API_PREFIX}/user_info/find_user/<phone_number>', methods=['GET'])
def find_users_by_phone_numer(phone_number):
  try:
    user_info = UserInfo.find_user_by_phone_number(phone_number, get_db_conn)
    return result_template(True, user_info)
  except BaseException as e:
    return result_template(False, [], str(e))


# Create user
@app.route(f'{API_PREFIX}/user_info', methods=['POST'])
def create_user():
  try:
    user_info = UserInfo.convert_from_json(request.json)
    user_info.create_user(get_db_conn)
    return result_template(True, [])
  except BaseException as e:
    return result_template(False, [], str(e))

# Update user status in group


@app.route(f'{API_PREFIX}/hui/user_status', methods=['PUT'])
def update_user_status():
  try:
    user_id = request.json['user_id']
    hui_id = request.json['hui_id']
    status = request.json['status']
    HuiGroup.update_user_status_in_group(user_id, hui_id, status, get_db_conn)
    return result_template(True, [])
  except BaseException as e:
    return result_template(False, [], str(e))


# Get all users in group hui
@app.route(f'{API_PREFIX}/hui/get_users/<hui_id>', methods=['GET'])
def get_users_in_group(hui_id):
  try:
    result = HuiGroup.get_all_users_in_group(hui_id, get_db_conn)
    return result_template(True, result)
  except BaseException as e:
    return result_template(False, [], str(e))


# Get all hui groups of user
@app.route(f'{API_PREFIX}/hui/<user_id>', methods=['GET'])
def get_hui_groups(user_id):
  try:
    result = HuiGroup.get_hui_groups(user_id, get_db_conn)
    return result_template(True, result)
  except BaseException as e:
    return result_template(False, [], str(e))

# GIAT HUI
@app.route(f'{API_PREFIX}/giat_hui', methods=['POST'])
def giat_hui():
  try:
    result = GiatHuiLog(**request.json).giat_hui(get_db_conn)
    return result_template(True, result)
  except BaseException as e:
    return result_template(False, [], str(e))

# Get all giat_hui log in a hui group
@app.route(f'{API_PREFIX}/giat_hui_log/<hui_id>', methods=['GET'])
def get_giat_hui_logs(hui_id):
  try:
    result = GiatHuiLog.get_giat_hui_log(hui_id, get_db_conn)
    return result_template(True, result)
  except BaseException as e:
    return result_template(False, [], str(e))

# Create hui group
@app.route(f'{API_PREFIX}/hui/<user_id>', methods=['POST'])
def create_hui_group(user_id):
  try:
    request.json['owner_id'] = user_id
    hui_group = HuiGroup.convert_from_json(request.json)
    hui_group.create_hui_group(get_db_conn)
    return result_template(True, [])
  except BaseException as e:
    return result_template(False, [], str(e))


# Invite user to join hui group
@app.route(f'{API_PREFIX}/hui/invite', methods=['POST'])
def invite_to_join_hui_group():
  user_id = request.json['user_id']
  hui_id = request.json['hui_id']
  status, msg = HuiGroup.invite_user(user_id, hui_id, get_db_conn)
  if status == True:
    return result_template(True, [])
  else:
    return result_template(False, [], str(msg))

# Get all transaction by hui id


@app.route(f'{API_PREFIX}/transaction/<hui_id>', methods=['GET'])
def get_all_transactions(hui_id):
  try:
    result = TransactionLog.get_all_transaction_by_group(hui_id, get_db_conn)
    return result_template(True, result)
  except BaseException as e:
    return result_template(False, [], str(e))


# withdraw_money from hui group and increase balance in self wallet
@app.route(f'{API_PREFIX}/withdraw_money', methods=['POST'])
def withdraw_money():
  try:
    user_id = request.json['user_id']
    hui_id = request.json['hui_id']
    amount = request.json['amount']
    UserInfo.withdraw_money(user_id, hui_id, amount,get_db_conn)
    return result_template(True, [])
  except BaseException as e:
    return result_template(False, [], str(e))


# Create transaction
@app.route(f'{API_PREFIX}/transaction', methods=['POST'])
def create_transaction():
  try:
    debtor_id = None
    user_id = request.json['user_id']
    hui_id = request.json['hui_id']
    amount = request.json['amount']
    if 'debtor_id' in request.json.keys():
      debtor_id = request.json['debtor_id']

    TransactionLog.payment(user_id, hui_id, amount, get_db_conn, debtor_id)
    return result_template(True, [])
  except BaseException as e:
    return result_template(False, [], str(e))


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
