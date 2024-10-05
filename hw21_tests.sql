--select hello_user('Michael');

--SELECT * FROM sp_4acts(15.0, 5.0);

--SELECT sp_get_min(10, 20);

--SELECT sp_get_min3(10, 20, 30);

--select sp_rnd_between(5, 15);

--select * from book_stats();

--select * from prolific_author();

--select * from cheapest_book();

--select * from sp_avg_books_and_authors();

--SELECT sp_insert_book('The Caves of Steel', '1953-10-01', 32.1, 8);
-----------------------------------------------------------------------------------------------
--SELECT sp_insert_author('David Weber');

--select * from sp_avg_book_count();

--SELECT sp_insert_book('On Basilisk Station', '1994-12-13', 82.1, 71);
--call sp_update_book('On Basilisk Station', '1993-04-12', 72.1, 71,365);

--SELECT sp_insert_author('G. Orwell');
--SELECT sp_insert_book('1984', '1949-06-08', 52.1, 72);
--call sp_update_author('George Orwell', 72);

--select * from sp_get_books_between(40.5, 60.25);

--select * from sp_get_books_not_by('J.R.R. Tolkien', 'Jane Austen');

--select upsert_book('Animal Farm', '1945-08-17', 42.1, 72);

--select * from book_data('A');
--select * from book_data('D');

--select book_sale('A Game of Thrones', true, 20);
select book_sale('A Game of Thrones', false, 20);