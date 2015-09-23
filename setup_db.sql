DROP DATABASE IF EXISTS gamesite;
CREATE DATABASE gamesite;
\connect gamesite;
DROP USER IF EXISTS heroku;
CREATE USER heroku;
ALTER USER heroku WITH PASSWORD 'seng330';
