DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_permission;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE user_permissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  permission_id INTEGER NOT NULL,
  FOREIGN KEY
(user_id) REFERENCES user
(id),
  FOREIGN KEY 
  (permission_id) REFERENCES permission
  (id)
);

CREATE TABLE permission (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  access_level VARCHAR NOT NULL,
  scope VARCHAR NOT NULL
);
