CREATE TABLE "login" (
	"id"	INTEGER NOT NULL UNIQUE,
	"login"	INTEGER NOT NULL UNIQUE,
	"password"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO login (login, password) VALUES ("admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918") ;
INSERT INTO login (login, password) VALUES ("user", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8") ;