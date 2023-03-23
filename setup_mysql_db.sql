-- Prepares a MYSQL Development Server for the project
-- Database name: nuws_data_db
-- User name: nuws_dev
-- User Password: Nuws_dev_pwd@2012#
-- Grants all privileges for nuws_dev on nuws_data_db
-- Grants SELECT privileges for nuws_dev on performance schema

CREATE DATABASE IF NOT EXISTS nuws_data_db;
CREATE USER IF NOT EXISTS 'nuws_dev'@'localhost' IDENTIFIED BY 'Nuws_dev_pwd@2012#';
GRANT ALL PRIVILEGES ON `nuws_data_db`.* TO 'nuws_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'nuws_dev'@'localhost';
FLUSH PRIVILEGES;