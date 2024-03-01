from database import conn, select, insert

class Data:
    def __init__(self):
        self.mydb = conn()

    def get_data(self, query, values=None):
        
        return select(query, values, self.mydb)

    def insert_data(self, query, values=None):
        
        return insert(query, values, self.mydb)
