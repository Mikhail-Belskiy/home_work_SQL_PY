import psycopg2

def creat_db ():
    conn = psycopg2.connect(database = "customer_base", user = 'postgres', password = "Mb20041995", host = 'localhost' )
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR (30) NOT NULL,
                llast_name VARCHAR (30) NOT NULL,
                email VARCHAR (30) NOT NULL 
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone (
                phone_id SERIAL PRIMARY KEY,
                phone VARCHAR (15) UNIQUE,
                client_id INTEGER NOT NULL REFERENCES clients (client_id) ON DELETE CASCADE
            );
            """)
        return conn.commit()

def new_client (first_name, llast_name, email):
    
    conn = psycopg2.connect(database = "customer_base", user = 'postgres', password = "Mb20041995", host = 'localhost' )
    with conn.cursor() as cur:
        cur.execute(""" 
            INSERT INTO clients (first_name, llast_name, email)
            VALUES (%s, %s, %s)
            RETURNING client_id, first_name, llast_name, email
            """, (first_name, llast_name, email)
        )
    conn.commit()

def new_phone (phone, client_id):
    
    conn = psycopg2.connect(database = "customer_base", user = 'postgres', password = "Mb20041995", host = 'localhost' )
    with conn.cursor() as cur:
        cur.execute(""" 
            INSERT INTO phone (phone, client_id)
            VALUES (%s, %s)
            RETURNING phone_id, phone, client_id
            """, (phone, client_id)
        )
    conn.commit()

def edit_data(client_id, first_name=None, llast_name=None, email=None):
    conn = psycopg2.connect(database="customer_base", user='postgres', password="Mb20041995", host='localhost')
    
    try:
        with conn.cursor() as cur:
            updates = []
            values = []

            if first_name is not None:
                updates.append("first_name = %s")
                values.append(first_name)

            if llast_name is not None:
                updates.append("llast_name = %s")
                values.append(llast_name)

            if email is not None:
                updates.append("email = %s")
                values.append(email)

            if updates:
                sql = f"""
                    UPDATE clients
                    SET {', '.join(updates)}
                    WHERE client_id = %s
                    RETURNING client_id, first_name, llast_name, email
                """
                values.append(client_id)
                cur.execute(sql, tuple(values))
                updated_client = cur.fetchone()
                return updated_client
    finally:
        conn.commit()
        conn.close()

def del_phone (client_id):
    
    conn = psycopg2.connect(database = "customer_base", user = 'postgres', password = "Mb20041995", host = 'localhost' )
    with conn.cursor() as cur:
        cur.execute(""" 
            DELETE FROM phone 
            WHERE client_id = %s
            RETURNING phone_id, phone, client_id
            """, (client_id)
        )
    conn.commit()

def del_client (client_id):
    
    conn = psycopg2.connect(database = "customer_base", user = 'postgres', password = "Mb20041995", host = 'localhost' )
    with conn.cursor() as cur:
        cur.execute(""" 
            DELETE FROM clients
            WHERE client_id = %s
            RETURNING client_id, first_name, llast_name, email
            """, (client_id)
        )
    conn.commit()

def search_client(first_name=None, llast_name=None, email=None, phone=None):
    conn = psycopg2.connect(database="customer_base", user='postgres', password="Mb20041995", host='localhost')
    with conn.cursor() as cur:
        try:
            conditions = []
            values = []

            if first_name is not None:
                conditions.append("c.first_name = %s")
                values.append(first_name)

            if llast_name is not None:
                conditions.append("c.llast_name = %s")
                values.append(llast_name)

            if email is not None:
                conditions.append("c.email = %s")
                values.append(email)

            if phone is not None:
                conditions.append("p.phone = %s")
                values.append(phone)

            sql = """
                SELECT c.client_id, c.first_name, c.llast_name, c.email, p.phone
                FROM clients c
                LEFT JOIN phone p ON c.client_id = p.client_id
            """
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            cur.execute(sql, tuple(values))
            return cur.fetchall() 
        finally:
            conn.close()

print(search_client(phone='89651239585'))


#if __name__ == "__main__":
    #creat_db()
    #new_client("Иван", "Петров", "petr@ya.ru")
    #new_phone('89651239585', 5)
    #edit_data(llast_name = 'Сергеич', client_id = 2)
    #del_phone('2')
    #del_client('3')
    