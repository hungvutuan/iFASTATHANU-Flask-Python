-- create DB
DROP database if exists ifast_resource;
create database ifast_resource;
USE ifast_resource; 

-- drop  tables
drop table if exists DEVICE;
drop table if exists smoke_sensor;
drop table if exists humidity_sensor;
drop table if exists temp_sensor;
drop table if exists sensor_loc;
drop table if exists history_sensor;

-- then create tables
create table sensor_loc(
	loc_id 	int unique NOT NULL AUTO_INCREMENT,
    loc_name varchar(50) not null,
    primary key (loc_id)
);

create table DEVICE (
	device_id 		INT unique NOT NULL AUTO_INCREMENT,
	device_name		VARCHAR(50) not null,
    device_type		VARCHAR(20),
    device_loc_id	int,
    smoke_id		int,
    humidity_id		int,
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

create table humidity_sensor(
	humidity_id 		int unique NOT NULL AUTO_INCREMENT,
    humidity_name 		varchar(50),
    loc_id 				int,
    primary key (humidity_id),
    foreign key (loc_id) references sensor_loc(loc_id)
);

create table temp_sensor(
	temp_id 		int unique NOT NULL AUTO_INCREMENT,
    temp_name 		varchar(50),
    loc_id 			int,
    primary key (temp_id),
    foreign key (loc_id) references sensor_loc(loc_id)
);

create table history_sensor(
	history_id 		int not null auto_increment,
    device_id 		int not null, -- we get the location from the device
    temp_reading 	int,
    smoke_reading 	int,
    humidity_reading int,
    date_reading 	date,
    temp_id 		int,	
    smoke_id 		int,
    humidity_id 	int,
    foreign key (temp_id) references temp_sensor(temp_id),
    foreign key (smoke_id) references smoke_sensor(smoke_id),
    foreign key (humidity_id) references humidity_sensor(humidity_id),
	primary key (history_id)
);

insert into sensor_loc(loc_name) values('VGU Binh Duong');
insert into sensor_loc(loc_name) values('Bosch Cong Hoa');

INSERT INTO DEVICE (device_name, device_type, device_loc_id, smoke_id, humidity_id, temp_id)
	VALUES 			('Home sensor', 'Raspberry Pi', 1, '01', '01', '01');

INSERT INTO DEVICE (device_name, device_type, device_loc_id, smoke_id, humidity_id, temp_id)
	VALUES ('Wokrplace-1', 'Raspberry Pi', 2, '02', '02', '02');

insert into smoke_sensor(smoke_name, loc_id)
	values('Restroom sensor', 1);
	