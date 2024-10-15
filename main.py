import psycopg2

def creat_db ():
    conn = psycopg2.connect(database = "customer_base", user = 'postgres', password = "Mb20041995", host = 'localhost' )
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXIST clients (
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR (30) NOT NULL,
                llast_name VARCHAR (30) NOT NULL,
                email VARCHAR (30) INIQUE DEFALT 'Не указан'
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXIST phone (
                phone_id SERIAL PRIMARY KEY,
                phone VARCHAR (15) INIQUE DEFALT 'Не указан',
                client_id INTEGER NOT NULL REFERENCES clients (clien_id) ON DELETE CASCADE
            );
            """)
        return conn.commit()

print(creat_db)
