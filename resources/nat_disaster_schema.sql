DROP DATABASE IF EXISTS natural_disasterdb;
CREATE DATABASE IF NOT EXISTS natural_disasterdb;
USE natural_disasterdb;

DROP TABLE IF EXISTS tornadoes;
DROP TABLE IF EXISTS hail;
DROP TABLE IF EXISTS wind;
DROP TABLE IF EXISTS tsunamis;
DROP TABLE IF EXISTS volcanoes;
DROP TABLE IF EXISTS significant_earthquakes;
DROP TABLE IF EXISTS earthquakes;

CREATE TABLE IF NOT EXISTS tornadoes (
tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
id INT(11),
year INT(4),
month INT(4),
day  INT(4),
date VARCHAR(255),
time VARCHAR(255),
timezone INT(2),
state VARCHAR(255),
state_fips INT(2),
state_nbr INT(4),
mag INT(2),
injuries INT(4),
deaths INT(4),
damage DECIMAL(40, 10), 
crop_loss DECIMAL(40, 10),
s_lat DECIMAL(10, 6), 
s_lng DECIMAL(10, 6), 
e_lat DECIMAL(10, 6), 
e_lng DECIMAL(10, 6),
length_traveled DECIMAL(10, 6), 
width INT(5),
nbr_states_affected INT(2),
sn INT(2),
sg INT(2),
f1 INT(4),
f2 INT(4),
f3 INT(4),
f4 INT(4),
fc INT(2))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS hail (
tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
id INT(11),
year INT(4),
month INT(4),
day  INT(4),
date VARCHAR(255),
time VARCHAR(255),
timezone INT(2),
state VARCHAR(255),
state_fips INT(2),
state_nbr INT(4),
mag DECIMAL(5,2),
injuries INT(4),
deaths INT(4),
damage DECIMAL(15, 1), 
crop_loss DECIMAL(15, 1),
s_lat DECIMAL(10, 6), 
s_lng DECIMAL(10, 6), 
e_lat DECIMAL(10, 6), 
e_lng DECIMAL(10, 6),
f1 INT(4))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS wind (
tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
id INT(11),
year INT(4),
month INT(4),
day  INT(4),
date VARCHAR(255),
time VARCHAR(255),
timezone INT(2),
state VARCHAR(255),
state_fips INT(2),
state_nbr INT(4),
mag DECIMAL(5,2),
injuries INT(4),
deaths INT(4),
damage DECIMAL(15, 1), 
crop_loss DECIMAL(15, 1),
s_lat DECIMAL(10, 6), 
s_lng DECIMAL(10, 6), 
e_lat DECIMAL(10, 6), 
e_lng DECIMAL(10, 6),
mag_type INT(4)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS wind (
tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
id INT(11),
year INT(4),
month INT(4),
day  INT(4),
date VARCHAR(255),
time VARCHAR(255),
timezone INT(2),
state VARCHAR(255),
state_fips INT(2),
state_nbr INT(4),
mag DECIMAL(5,2),
injuries INT(4),
deaths INT(4),
damage DECIMAL(15, 1), 
crop_loss DECIMAL(15, 1),
s_lat DECIMAL(10, 6), 
s_lng DECIMAL(10, 6), 
e_lat DECIMAL(10, 6), 
e_lng DECIMAL(10, 6),
mag_type INT(4)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tsunamis (
tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
year INT(4),
month INT(4),
day  INT(4),
hour INT(4),
min INT(4),
second INT(4),
validity VARCHAR(255),
source VARCHAR(255),
earthquake_mag DECIMAL(5,2),
country VARCHAR(255),
name VARCHAR(255),
lat DECIMAL(10, 6),
lng DECIMAL(10, 6),
water_height DECIMAL(10,2),
tsunami_mag_lida DECIMAL(4,1),
tsunami_intensity DECIMAL(4,1),
death_nbr INT(8),
injuries_nbr INT(8),
damage_mill DECIMAL(10,3),
damage_code INT(2),
house_destroyed INT(8),
house_code INT(2)
)ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS volcanoes (
tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
year INT(4),
month INT(4),
day  INT(4),
tsu INT(4),
eq INT(4),
name VARCHAR(255),
location VARCHAR(255),
country VARCHAR(255),
lat DECIMAL(10, 6),
lng DECIMAL(10, 6),
elevation DECIMAL(8,2),
type VARCHAR(255),
volcanic_index INT(2),
fatality_cause VARCHAR(255),
death INT(6),
death_code INT(1),
injuries INT(6),
injuries_code INT(1),
damage DECIMAL(10, 6),
damage_code INT(1),
houses INT(5),
houses_code INT(1)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS significant_earthquakes (
db_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
id VARCHAR(255), 
yr INT(5), 
month INT(3), 
day INT(3), 
hr INT(3), 
min INT(2), 
eq_mag_primary DECIMAL(4,2), 
eq_mag_mw DECIMAL(4,2) DEFAULT NULL, 
eq_mag_ms DECIMAL(4,2) DEFAULT NULL, 
intensity VARCHAR(255), 
country VARCHAR(255), 
location_name VARCHAR(255), 
lat DECIMAL(10, 6), 
lng DECIMAL(10,6), 
region_code INT(4), 
deaths INT(10), 
deaths_descriptions INT(4), 
damage_millions DECIMAL(12,2), 
damage_description INT(5), 
total_deaths INT(10), 
total_deaths_description INT(2), 
total_injuries VARCHAR(255) NOT NULL DEFAULT 'unknown', 
total_injuries_description VARCHAR(255) NOT NULL DEFAULT 'unknown', 
total_damage_millions VARCHAR(255) NOT NULL DEFAULT 'unknown', 
total_damage_description VARCHAR(255) NOT NULL DEFAULT 'unknown');

CREATE TABLE IF NOT EXISTS earthquakes (
id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
magnitude VARCHAR(255), 
place VARCHAR(255), 
time VARCHAR(255), 
timezone VARCHAR(255), 
url VARCHAR(255), 
tsunami INT(1), 
ids VARCHAR(255), 
specific_type VARCHAR(255), 
geometry VARCHAR(255), 
lat DECIMAL(10, 6), 
lng DECIMAL(10,6), 
depth DECIMAL(6,2)) 
ENGINE=InnoDB;