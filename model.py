from database import conn, select, insert

class Karyawan:
    def __init__(self):
        self.mydb = conn()

    def get_data(self, query, values=None):
        
        return select(query, values, self.mydb)

    def insert_data(self, query, values=None):
        
        return insert(query, values, self.mydb)

    def execute_query(self, query, values=None):
        try:
            cursor = self.mydb.cursor(dictionary=True)
            cursor.execute(query, values)
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()  # Mengambil hasil query SELECT
            else:
                self.mydb.commit()  # Jika bukan SELECT, melakukan commit untuk operasi DML (INSERT, UPDATE, DELETE)
        except Exception as e:
            self.mydb.rollback()  # Menggagalkan transaksi jika terjadi error
            raise e
        finally:
            cursor.close()
