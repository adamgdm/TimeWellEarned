FROM mysql:8.0

WORKDIR /docker-entrypoint-initdb.d

COPY ./init.sql /docker-entrypoint-initdb.d

ENV MYSQL_DATABASE=db
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=Password123
ENV MYSQL_ROOT_PASSWORD=Password123

EXPOSE 3306

CMD ["mysqld"]