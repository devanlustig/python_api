import psycopg2

def conn(user="postgres", password="postgres", host="localhost", dbname="python"):
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=dbname
    )
    return conn

def select(query, values, conn):
    mycursor = conn.cursor()
    try:
        mycursor.execute(query, values)
        row_headers = [x[0] for x in mycursor.description]
        myresult = mycursor.fetchall()
        json_data = []
        for result in myresult:
            json_data.append(dict(zip(row_headers, result)))
        return json_data
    except Exception as e:
        print("Error executing SELECT query:", e)
        return []

def insert(query, values, conn):
    mycursor = conn.cursor()
    try:
        mycursor.execute(query, values)
        conn.commit()
        return True
    except Exception as e:
        print("Error executing INSERT query:", e)
        conn.rollback()
        return False
    finally:
        mycursor.close()
