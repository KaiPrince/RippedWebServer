INSERT INTO user
	(username, password)
VALUES
	('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
	('other', 'pbkdf2:sha256:150000$InesQWDK$53300f70cd0d8f59285307569976fd9e442e120dc6bc46fc321bddcb7c2d8efb');

-- INSERT INTO permission
-- 	(access_level, scope)
-- VALUES
-- 	('read', 'files'),
-- 	('write', 'files'),
-- 	('read', 'disk_storage'),
-- 	('write', 'disk_storage');

INSERT INTO user_permissions
	(user_id, permission_id)
VALUES
	(2, 1),
	(2, 2),
	(2, 3),
	(2, 4),
	(3, 1),
	(3, 3);