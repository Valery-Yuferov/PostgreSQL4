
import psycopg2


def create_db(conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(50),
            phones VARCHAR(50)[]
        );
    """)


def add_client(conn, first_name, last_name, email, phones=None):
    cur.execute("""
        INSERT INTO clients (first_name, last_name, email, phones)
        VALUES (%s, %s, %s, %s);
    """, (first_name, last_name, email, phones))


def add_phone(conn, client_id, phone):
    cur.execute("""
        UPDATE clients
        SET phones = array_append(phones, %s)
        WHERE id = %s;
    """, (phone, client_id))


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    cur.execute("""
        UPDATE clients
        SET first_name = COALESCE(%s, first_name),
            last_name = COALESCE(%s, last_name),
            email = COALESCE(%s, email),
            phones = COALESCE(%s, phones)
        WHERE id = %s;
    """, (first_name, last_name, email, phones, client_id))


def delete_phone(conn, client_id, phone):
    cur.execute("""
        UPDATE clients
        SET phones = array_remove(phones, %s)
        WHERE id = %s;
    """, (phone, client_id))


def delete_client(conn, client_id):
    cur.execute("""
        DELETE FROM clients
        WHERE id = %s;
    """, (client_id,))


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
        SELECT * FROM clients
        WHERE first_name = COALESCE(%s, first_name)
            AND last_name = COALESCE(%s, last_name)
            AND email = COALESCE(%s, email)
            AND %s = ANY(phones);
    """, (first_name, last_name, email, phone))
    return cur.fetchall()


with psycopg2.connect(database="clients_db", user="postgres", password="wellington6") as conn:
    with conn.cursor() as cur:
        create_db(conn)

        add_client(conn, "John", "Smith", "johnsmith@gmail.com", ["111-11-11", "222-22-22"])
        add_client(conn, "Ivan", "Petrov", "ivanpetrov@mail.ru", ["333-33-33", "444-44-44"])
        add_client(conn, "Olga", "Smirnova", "olgasmirnova@yandex.ru", ["555-55-55"])

        add_phone(conn, 3, "666-66-66")

        change_client(conn, 1, last_name="Robertson")

        delete_phone(conn, 40, "666-66-66")

        delete_client(conn, 38)

        print(find_client(conn, first_name="Olga", last_name="Smirnova", email="olgasmirnova@yandex.ru",
        phone="555-55-55"))

conn.close()







