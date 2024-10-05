import psycopg2
import psycopg2.extras

try:
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="admin",  # postgres
        password="admin",
        port="5556"
    )

    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    select_query = "select * from sp_get_books_between(25.5, 30.25);"
    cursor.execute(select_query)

    rows = cursor.fetchall()
    print("------------- Query #01 --------------")
    if rows:
        for row in rows:
            # rows_dict = dict(row)
            # print(rows_dict)
            print(f"ID: {row['id']} TITLE: {row['title']:^20}, R.D.: {row['release_date']}, " +\
                  f"PRICE: {row['price']} AUTHOR: {row['author_name']:^8} ")

    else:
        print("No books found within the specified range.")

    select_query = "select * from sp_avg_books_and_authors();"
    cursor.execute(select_query)

    rows = cursor.fetchall()
    print("\n------------- Query #02 --------------")
    if rows:
        for row in rows:
            rows_dict = dict(row)
            print(rows_dict)
            # print(f"ID: {row['id']} TITLE: {row['title']:^20}, R.D.: {row['release_date']}, " + \
            #       f"PRICE: {row['price']} AUTHOR: {row['author_name']:^8} ")

    else:
        print("No books or authors found within the specified range.")

    select_query = "select * from book_stats();"
    cursor.execute(select_query)

    rows = cursor.fetchall()
    print("\n------------- Query #03 --------------")
    if rows:
        for row in rows:
            rows_dict = dict(row)
            print(rows_dict)


    else:
        print("No books found.")

    print("\n------------- Insert Query --------------")
    select_query = "SELECT sp_insert_author('Kurt Vonnegut');"
    cursor.execute(select_query)
    new_id = cursor.fetchone()[0]
    print('new_id', new_id)
    insert_query = """insert into books (title, release_date, price, author_id)
     values (%s, %s, %s, %s) returning id;
     """
    insert_values = ('Slaughterhouse-Five', '1969-03-31', 59, new_id)
    cursor.execute(insert_query, insert_values)
    new_id = cursor.fetchone()[0]
    print('new_id', new_id)

    connection.commit()

except Exception as error:
    print(f"Error: {error}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()