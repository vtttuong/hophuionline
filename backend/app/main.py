import psycopg2, os
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
 
CORS(app)

API_PREFIX = '/api/v1'
@app.route("/")
def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.8 (from the example template)"

def get_db_conn():
    return psycopg2.connect(
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"), port= os.getenv("DB_PORT"), sslmode=os.getenv("DB_SSL_MODE")
    )

@app.route(f'{API_PREFIX}/user_info/<user_id>',methods=['GET'])
# TODO Get information about user by user_id  BINH
def get_user_info(user_id):
    pass

@app.route(f'{API_PREFIX}/user_info',methods=['POST'])
# TODO Create user with information BINH
def create_user():
    pass

@app.route(f'{API_PREFIX}/hui/<user_id',methods=['GET'])
# TODO Get all hui groups by user id BINH
def get_hui_groups(user_id):
    pass

@app.route(f'{API_PREFIX}/hui/<user_id',methods=['POST'])
# TODO Create hui group by user id BINH
def create_hui_group(user_id):
    pass

@app.route(f'{API_PREFIX}/hui/invite/<user_id',methods=['POST'])
# TODO Invite user join hui group
def invite_to_join_hui_group(user_id):
    pass


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