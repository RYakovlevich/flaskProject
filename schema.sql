DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email varchar(100) NOT NULL unique ,
    password varchar(100),
    name varchar(100)
);