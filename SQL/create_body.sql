----------------------------
CREATE SCHEMA IF NOT EXISTS users;
----------------------------

----------------------------
CREATE TABLE IF NOT EXISTS users.auth(
	telegramID integer NOT NULL PRIMARY KEY,
	username varchar NOT NULL,
	isGrandUse boolean default false
);
----------------------------

----------------------------
CREATE TABLE IF NOT EXISTS users.photos(
    photo_id SERIAL PRIMARY KEY,
    telegramID INTEGER REFERENCES users.auth(telegramID),
    photo_path varchar(256) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
----------------------------