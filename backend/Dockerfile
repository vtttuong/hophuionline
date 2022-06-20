FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip install psycopg2-binary flask-sqlalchemy Flask-Migrate

# Add a /app volume
VOLUME ["/app"]
