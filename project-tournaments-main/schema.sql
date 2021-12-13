drop table if exists player;
drop table if exists tournament;
drop table if exists team;
drop table if exists account;
drop table if exists password;


CREATE TABLE player (
    id integer primary key autoincrement,
    name text not null unique,
    registration text not null,
    wins int,
    loses int
);

CREATE TABLE tournament (
    id integer primary key autoincrement,
    name text not null,
    format text,
    size int,
    score int,
    player_name text not null,
    game_name text not null,
    description text
);

CREATE TABLE team(
     id integer primary key autoincrement,
     name text,
     color int
);

CREATE TABLE account(
    id integer primary key autoincrement,
    name text not null unique,
    hash text not null unique
);


