CREATE DATABASE MODUS_TEST;
----------------------------

----------------------------
CREATE USER dev WITH password="secretpass";
----------------------------

----------------------------
GRANT ALL PRIVILEGES ON DATABASE MODUS_TEST TO dev;
----------------------------