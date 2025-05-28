CREATE EXTENSION IF NOT EXISTS pgcrypto;


CREATE TABLE users (
   username VARCHAR(255) NOT NULL PRIMARY KEY,
   password TEXT NOT NULL
);
  INSERT INTO users (username, password)
   VALUES ('benoit', crypt('password', gen_salt('bf')));

  INSERT INTO users (username, password)
   VALUES ('admin', crypt('password', gen_salt('bf')));

  INSERT INTO users (username, password)
   VALUES ('marijn', crypt('password', gen_salt('bf')));

  INSERT INTO users (username, password)
   VALUES ('test', crypt('password', gen_salt('bf')));

