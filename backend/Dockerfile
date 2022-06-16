FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

#COPY ./requirements.txt /app/requirements.txt

RUN pip install google-cloud-bigquery==2.26.0 \
    pandas==1.3.5 \
    pyarrow==7.0.0

# Add a /app volume
VOLUME ["/app"]

#COPY ./app /app

CMD [ "/start-reload.sh" ]
