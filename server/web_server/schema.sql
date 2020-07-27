DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_file;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE user_file (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  uploaded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_name VARCHAR NOT NULL,
  file_path VARCHAR NOT NULL,
  FOREIGN KEY
(user_id) REFERENCES user
(id)
);