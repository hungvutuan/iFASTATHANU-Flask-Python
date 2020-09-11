-- create DB
DROP database if exists ifast_resource;
create database ifast_resource;
USE ifast_resource;

-- drop  tables
drop table if exists DEVICE;
drop table if exists smoke_sensor;
drop table if exists gas_sensor;
drop table if exists temp_sensor;
drop table if exists sensor_loc;
drop table if exists history_sensor;

-- then create tables
create table sensor_loc(
	loc_id 	int unique NOT NULL AUTO_INCREMENT,
    loc_name varchar(50) not null,
    primary key (loc_id)
);

create table alarm(
	alarm_id 		int unique NOT NULL AUTO_INCREMENT,
    alarm_status 	varchar(50) not null,
    alarm_type 		varchar(50) not null default "AUTO",
    primary key (alarm_id)
);

create table DEVICE (
	device_id 		INT unique NOT NULL AUTO_INCREMENT,
	device_name		VARCHAR(50) not null,
    device_type		VARCHAR(20),
    device_loc_id	int,
    smoke_id		int,
    gas_id		int,
    temp_id			int,
    primary key (device_id),
    foreign key (device_loc_id) references sensor_loc(loc_id)
);

create table smoke_sensor(
	smoke_id 			int unique NOT NULL AUTO_INCREMENT,
    smoke_name 			varchar(50),
    loc_id 	int,
    primary key (smoke_id),
    foreign key (loc_id) references sensor_loc(loc_id)
);

create table gas_sensor(
	gas_id 		int unique NOT NULL AUTO_INCREMENT,
    gas_name 		varchar(50),
    loc_id 				int,
    primary key (gas_id),
    foreign key (loc_id) references sensor_loc(loc_id)
);

create table temp_sensor(
	temp_id 		int unique NOT NULL AUTO_INCREMENT,
    temp_name 		varchar(50),
    loc_id 			int,
    primary key (temp_id),
    foreign key (loc_id) references sensor_loc(loc_id)
);

create table history_fire(
	fire_id  		int not null auto_increment,
    fire_date 		date,
    fire_percentage	int default 0,
    loc_id          int,
    primary key (fire_id),
    foreign key (loc_id) references sensor_loc(loc_id)
);


create table history_sensor(
	history_id 		int not null auto_increment,
    device_id 		int not null, -- we get the location from the device
    temp_reading 	int,
    smoke_reading 	int,
    gas_reading 	int,
    date_reading 	date,
    alarm_id 		int,
    temp_id 		int,
    smoke_id 		int,
    gas_id 			int,
    foreign key (temp_id) references temp_sensor(temp_id),
    foreign key (smoke_id) references smoke_sensor(smoke_id),
    foreign key (gas_id) references gas_sensor(gas_id),
    foreign key (device_id) references device(device_id),
    foreign key (alarm_id) references alarm(alarm_id),
	primary key (history_id)
);

-- create table readings_sensor(
-- 	reading_id 		int not null auto_increment,
--     sensor_id 		int,
--     foreign key	(sensor_id) references
--     primary key (reading_id)
-- );

insert into sensor_loc(loc_name) values('Bedroom');
insert into sensor_loc(loc_name) values('Living room');
insert into sensor_loc(loc_name) values('Kitchen');

insert into alarm(alarm_status)
	values 	('Fire');
insert into alarm(alarm_status)
	values 	('Prominent');
insert into alarm(alarm_status)
	values 	('Safe');


INSERT INTO DEVICE (device_name, device_type, device_loc_id, smoke_id, gas_id, temp_id)
	VALUES	('Bedroom sensor', 'Raspberry Pi', 1, '01', '01', '01');
INSERT INTO DEVICE (device_name, device_type, device_loc_id, smoke_id, gas_id, temp_id)
	VALUES	('Kitchen-1', 'Raspberry Pi', 2, '02', '02', '02');

insert into smoke_sensor(smoke_name, loc_id)
	values	('Kitchen sensor', 1);
insert into temp_sensor(temp_name, loc_id)
	values	('Kitchen sensor', 1);
insert into gas_sensor(gas_name, loc_id)
	values 	('Kitchen sensor', 1);

-- pseudo values for history
insert into history_sensor(device_id, temp_reading, smoke_reading, gas_reading, date_reading, temp_id, smoke_id, gas_id, alarm_id)
	values	(1, 10, 20, 30, "2020-04-15", 1, 1, 1, 1);
insert into history_sensor(device_id, temp_reading, smoke_reading, gas_reading, date_reading, temp_id, smoke_id, gas_id, alarm_id)
	values	(1, 10, 20, 30, "2020-04-15", 1, 1, 1, 1);

insert into history_fire(fire_date, fire_percentage, loc_id)
	values ("2020-12-10", 14, 1);

select history_id, alarm_status, loc_name, device_name, date_reading, alarm_type
from history_sensor h join alarm a on h.alarm_id = a.alarm_id
	 join device d on h.device_id = d.device_id
     join sensor_loc sl on sl.loc_id = d.device_loc_id;
