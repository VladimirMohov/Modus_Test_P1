CREATE OR REPLACE PROCEDURE users.add_user_auth(
   telegramID integer,
   username varchar
)
LANGUAGE SQL    
AS $$
    INSERT INTO users.auth (telegramID, username)
            VALUES (telegramID, username)
$$;
---------------------------

---------------------------
CREATE OR REPLACE PROCEDURE users.accept_request(
    telegramID integer
)
LANGUAGE SQL
AS $$
    UPDATE users.auth
    SET isGrandUse = true
    WHERE telegramID = telegramID;
$$;
---------------------------

---------------------------
CREATE OR REPLACE PROCEDURE users.insert_photo(
    telegramID integer,
	photo_path varchar
)
LANGUAGE SQL
AS $$
    INSERT INTO users.photos (telegramID, photo_path)
            VALUES (telegramID, photo_path)
$$;
---------------------------

---------------------------
CREATE OR REPLACE FUNCTION users.get_user(tid integer)
RETURNS TABLE (telegramid integer, username varchar, isgranduse boolean)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT telegramid, username, isgranduse
    FROM users.auth
    WHERE telegramid = tid;
END;
$$;
---------------------------