FROM python:3.8

RUN pip install flask flask-mysqldb mysql-connector-python flask-cors requests pandas

WORKDIR /app

VOLUME ["/app"]

ENV MYSQL_HOST=DB
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=Password123
ENV MYSQL_ROOT_PASSWORD=Password123

EXPOSE 5000

# run the application and sleep indefinitely
CMD python3 app.py 