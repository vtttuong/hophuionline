FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

#COPY ./requirements.txt /app/requirements.txt

RUN pip install psycopg2==2.9.3

# Add a /app volume
VOLUME ["/app"]

#COPY ./app /app

CMD [ "/start-reload.sh" ]
