# users tabelle
create table users(
    id serial primary key,
    username text,
    password text,
    hp integer,
    position text,
    dragonalive boolean,
    swordavail boolean,
    treasureavail boolean,
    brunnennutzungen integer
);
# raum tabelle
create table raum (
    id serial primary key,
    raumname text,
    x int,
    y int
);