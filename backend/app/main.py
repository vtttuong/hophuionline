import psycopg2, os
from flask import Flask

app = Flask(__name__)

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