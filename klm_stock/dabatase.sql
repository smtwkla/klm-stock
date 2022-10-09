-- table for sectors
create table sectors
(
    code      char(10)    not null
        primary key,
    full_name varchar(50) null
);

-- table for scripts
create table scripts
(
    id          int auto_increment
        primary key,
    script_code char(15)    not null,
    script_name varchar(50) not null,
    sector_code char(10)    null,
    constraint scripts_pk
        unique (script_code)
);

-- table for buy and sell transactions
create table transactions
(
    id            int auto_increment
        primary key,
    script_id     int           not null,
    date_of_trans date          not null,
    qty           int           not null,
    price         decimal(8, 2) not null
);

-- table for last traded price
create table ltp
(
    script_id int           not null
        primary key,
    ts        datetime      not null,
    ltp       decimal(8, 2) not null
);
