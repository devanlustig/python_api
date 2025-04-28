from database import conn, select, insert
import psycopg2.extras

class Karyawan:
    def __init__(self):
        self.mydb = conn()

    def get_data(self, query, values=None):
        
        return select(query, values, self.mydb)

    def insert_data(self, query, values=None):
        
        return insert(query, values, self.mydb)

    def execute_query(self, query, values=None):
        cursor = None
        try:
            cursor = self.mydb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(query, values)
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.mydb.commit()
        except Exception as e:
            self.mydb.rollback()
            raise e
        finally:
            if cursor is not None:
                cursor.close()
