"""
1.
CREATE OR REPLACE FUNCTION hello_user(name VARCHAR)
RETURNS varchar
LANGUAGE plpgsql AS
$$
BEGIN
    RETURN CONCAT('hello ', name, ' ! ', current_timestamp);
END;
$$;
"""
'''
2.
CREATE OR REPLACE FUNCTION sp_4acts(x DOUBLE PRECISION, y DOUBLE PRECISION,
    OUT prod DOUBLE PRECISION, 
    OUT div_res DOUBLE PRECISION, 
    OUT sum_res DOUBLE PRECISION,
    OUT diff_res DOUBLE PRECISION)
LANGUAGE plpgsql AS
$$
DECLARE
    z DOUBLE PRECISION := 1.0;
BEGIN
    prod = x * y * z;
    div_res = x / y;
    sum_res = x + y;
    diff_res = x - y;
END;
$$;
   
'''
'''
3.
CREATE OR REPLACE FUNCTION sp_get_min(_x INTEGER, _y INTEGER)
RETURNS INTEGER
LANGUAGE plpgsql AS
$$
BEGIN
    IF _x < _y THEN
        RETURN _x;
    ELSE
        RETURN _y;
    END IF;
END;
$$;

'''
'''
4.
CREATE OR REPLACE FUNCTION sp_get_min3(_x INTEGER, _y INTEGER, _z INTEGER)
RETURNS INTEGER
LANGUAGE plpgsql AS
$$
BEGIN
    IF _x < _y AND _x < _z THEN
        RETURN _x;
    ELSIF _y < _z THEN
        RETURN _y;
    ELSE
        RETURN _z;
    END IF;
END;
$$;
            
'''
'''
5.
CREATE OR REPLACE FUNCTION sp_rnd_between(low INTEGER, high INTEGER)
RETURNS INTEGER
LANGUAGE plpgsql AS
$$
BEGIN
   RETURN floor(random()* (high-low + 1) + low);
END;
$$;
'''
'''
6.
CREATE OR REPLACE FUNCTION book_stats(
    OUT cheap_book VARCHAR(100),
    OUT expensive_book VARCHAR(100),
    OUT avg_book VARCHAR(100),
    OUT books_count INTEGER)
LANGUAGE plpgsql AS
    $$
        BEGIN
            select min(price) into cheap_book from books b;
			select avg(price) into avg_book from books b;
			select max(price) into expensive_book from books b;
			select count(*) into books_count from books b;
        END;
    $$;
    
'''
'''
7.
CREATE OR REPLACE FUNCTION prolific_author(
    OUT author_name VARCHAR(100),
    OUT books_count INTEGER)
LANGUAGE plpgsql AS
    $$
        BEGIN
            SELECT a.name, t.book_count
		    INTO author_name, books_count
		    FROM (
		        SELECT author_id, COUNT(id) AS book_count 
		        FROM books 
		        GROUP BY author_id
		    ) t
		    JOIN authors a ON a.id = t.author_id
		    WHERE t.book_count = (
		        SELECT MAX(book_count)
		        FROM (
		            SELECT author_id, COUNT(id) AS book_count 
		            FROM books 
		            GROUP BY author_id
		        )
		    );
		
        END;
    $$;     
'''
'''
8.
CREATE OR REPLACE FUNCTION cheapest_book(
                OUT cheap_book TEXT)
LANGUAGE plpgsql AS
    $$
        DECLARE
            min_price DOUBLE PRECISION := 0;
        BEGIN
            SELECT MIN(price) INTO min_price FROM books;
            
            SELECT title INTO cheap_book
            FROM books
            WHERE price = min_price;
        END;
    $$;  
'''
'''
9.
CREATE OR REPLACE FUNCTION sp_avg_books_and_authors(
    OUT avg_books_and_authors INT)
LANGUAGE plpgsql AS
$$
DECLARE
    count_authors BIGINT := 0;
    count_books BIGINT := 0;
BEGIN
    SELECT COUNT(*) INTO count_books FROM books;
    SELECT COUNT(*) INTO count_authors FROM authors;
    avg_books_and_authors := (count_books + count_authors)/2;
END;
$$;
'''
'''
10.
CREATE OR REPLACE FUNCTION sp_insert_book(
    _title TEXT, _release_date TIMESTAMP, _price DOUBLE PRECISION, _author_id BIGINT)
RETURNS BIGINT
LANGUAGE plpgsql AS
$$
DECLARE
    new_id BIGINT := 0;
BEGIN
    INSERT INTO books (title, release_date, price, author_id)
    VALUES (_title, _release_date, _price, _author_id)
    RETURNING id INTO new_id;

    RETURN new_id;
END;
$$;
'''
"""________________________________________________________________________________________"""
'''
11.
CREATE OR REPLACE FUNCTION sp_insert_author(_name TEXT)
RETURNS BIGINT
LANGUAGE plpgsql AS
$$
DECLARE
    new_id BIGINT := 0;
BEGIN
    INSERT INTO authors (name) 
    VALUES (_name)
    RETURNING id INTO new_id;

    RETURN new_id;
END;
$$;
'''
'''
12.
CREATE OR REPLACE FUNCTION sp_avg_book_count(
    OUT avg_book_count INT)
RETURNS DOUBLE PRECISION
LANGUAGE plpgsql AS
$$
BEGIN
    SELECT avg(book_count)
    INTO avg_book_count
		        FROM (
		            SELECT author_id, COUNT(id) AS book_count 
		            FROM books 
		            GROUP BY author_id
		        )
END;
$$;
'''
'''
13.
CREATE OR REPLACE PROCEDURE sp_update_book(
    _title TEXT, _release_date TIMESTAMP, _price DOUBLE PRECISION, _author_id BIGINT, _update_id BIGINT)
LANGUAGE plpgsql AS
$$
BEGIN
    UPDATE books
    SET title = _title, release_date = _release_date, price = _price, author_id = _author_id
    WHERE id = _update_id;
END;
$$;
'''
'''
14.
CREATE OR REPLACE PROCEDURE sp_update_author(
    _name TEXT, _update_id BIGINT)
LANGUAGE plpgsql AS
$$
BEGIN
    UPDATE authors
    SET name = _name
    WHERE id = _update_id;
END;
$$;
'''
'''
15.
CREATE OR REPLACE FUNCTION sp_get_books_between(low DOUBLE PRECISION, high DOUBLE PRECISION)
RETURNS TABLE(id BIGINT, title TEXT, release_date DATE, price DOUBLE PRECISION, author_id BIGINT, author_name TEXT)
LANGUAGE plpgsql AS
$$
BEGIN
    RETURN QUERY

    SELECT b.id, b.title, b.release_date, b.price, b.author_id, a.name
    FROM books b
    JOIN authors a ON b.author_id = a.id
    WHERE b.price BETWEEN low AND high;
END;
$$;
'''
'''
16.
CREATE OR REPLACE FUNCTION sp_get_books_not_by(_author1 TEXT, _author2 TEXT)
RETURNS TABLE(id BIGINT, title TEXT, release_date DATE, price DOUBLE PRECISION, author_id BIGINT, author_name TEXT)
LANGUAGE plpgsql AS
$$
BEGIN
    RETURN QUERY
    WITH books_auth1 AS (
        SELECT * FROM books WHERE author_id = (SELECT id FROM authors WHERE name = _author1)
    ), books_auth2 AS (
        SELECT * FROM books WHERE author_id = (SELECT id FROM authors WHERE name = _author2)
    )
    SELECT b.id, b.title, b.release_date, b.price, b.author_id, a.name
    FROM books b
    JOIN authors a ON b.author_id = a.id
    WHERE b.id NOT IN (SELECT books_auth1.id FROM books_auth1)
    AND b.id NOT IN (SELECT books_auth2.id FROM books_auth2);
END;
$$;
            
'''
'''
17.
CREATE OR REPLACE FUNCTION upsert_book(
    _title TEXT, _release_date TIMESTAMP, _price DOUBLE PRECISION, _author_id BIGINT)
RETURNS BIGINT
LANGUAGE plpgsql AS
$$
DECLARE
    new_id BIGINT := 0;
BEGIN
     IF NOT EXISTS (SELECT 1 FROM books WHERE title = _title AND author_id = _author_id) THEN
        INSERT INTO books (title, release_date, price, author_id)
        VALUES (_title, _release_date, _price, _author_id)
        RETURNING id INTO new_id;
    ELSE
        UPDATE books
        SET title = _title, release_date = _release_date, price = _price, author_id = _author_id
        RETURNING id INTO new_id;
    END IF;
    RETURN new_id;
    
END;
$$;
'''
'''
18.

'''