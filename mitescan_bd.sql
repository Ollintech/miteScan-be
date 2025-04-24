create database MiteScan;
\c MiteScan;

create table accesses(
    id serial primary key,
    name varchar(200) not null,
    description varchar(200) not null
)

create table companies(
    id serial primary key,
    name varchar(200) not null,
    cnpj int not null
)

create table users(
    id serial primary key,
    name varchar(200) not null,
    email varchar(200) not null,
    password_hash varchar(100) not null,
    last_login timestamp,
    status boolean not null default false,
    access_id int not null,
    company_id int not null,
    foreign key (access_id) references accesses(id),
    foreign key (company_id) references companies(id)
)

create table bee_types(
    id serial primary key,
    name varchar(200) not null,
    description varchar(200),
    user_id int,
    foreign key (user_id) references users(id)
)

create table hives(
    id serial primary key,
    user_id int,
    bee_type_id int,
    location_lat float not null,
    location_lng float not null,
    size int not null,
    humidity float,
    temperature float,
    foreign key (user_id) references users(id),
    foreign key (bee_type_id) references bee_types(id)
)

create table hive_analysis(
    id serial primary key,
    hive_id int,
    user_id int,
    image_path varchar(255) not null,
    varroa_detected boolean not null default false,
    detection_confidence float notnull,
    created_at timestamp default(now),
    foreign key (hive_id) references hives(id),
    foreign key (user_id) references users(id)
)

create table analysis_backups(
    id serial primary key,
    user_id int,
    file_path varchar(255) not null,
    analysis_id int,
    foreign key (user_id) references users(id)
)