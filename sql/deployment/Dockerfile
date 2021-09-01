FROM mysql/mysql-server

ENV MYSQL_DATABASE=wikidata
ENV MYSQL_ALLOW_EMPTY_PASSWORD=true
ENV MYSQL_LOG_CONSOLE=true
ENV MYSQL_INITDB_SKIP_TZINFO=true

COPY settings.sql /docker-entrypoint-initdb.d/
COPY *enwiki*.sql /data/
COPY my.cnf /etc/

EXPOSE 3306
