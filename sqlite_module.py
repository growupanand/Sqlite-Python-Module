import sqlite3

class database:

    def __init__(self, database_name):
        self.database_name = database_name
        self.conn = sqlite3.connect(self.database_name)


    def create_table(self, table_name, table_colums):
        self.table_name = table_name
        self.table_colums = table_colums
        self.conn.execute("CREATE TABLE " + self.table_name +
                          "(ID INTEGER PRIMARY KEY AUTOINCREMENT," +
                          self.table_colums +
                          ");")


    def check_table(self, table_name):
        self.table_name = table_name
        self.c = self.conn.cursor()
        # get the count of tables with the name
        self.c.execute("SELECT count(name) FROM sqlite_master  WHERE type='table' AND name='" + self.table_name + "'")

        # if the count is 1, then table exists
        if self.c.fetchone()[0] == 1:
            return True
        else:
            return False


    def insert_data(self, table_name, table_data):
        self.table_name = table_name
        self.table_data = table_data
        for item in self.table_data:
            try:
                self.conn.execute("INSERT INTO " + self.table_name + " (" + ', '.join(item.keys()) + ") VALUES (" + str(', '.join("'" + i + "'" for i in item.values())) + ")")
                self.conn.commit()
                return True
            except sqlite3.Error as e:
                return e

    def select_data(self, table_name, colums, condition=None):
        self.table_name = table_name
        self.colums = colums
        self.condition = condition
        if self.condition == None:
            self.condition = ''
        self.query_colums = ', '.join(self.colums)
        self.data = self.conn.execute("SELECT " + self.query_colums + " from " + self.table_name + " " + self.condition)
        self.data_names = [description[0] for description in self.data.description]
        self.new_row = []
        r = 0
        for row in self.data:
            v = 0
            new_data = {}
            for names in self.data_names:
                new_data[names] = row[v]
                v += 1
            self.new_row.append(new_data)
            r += 1
        return self.new_row

    def delete_data(self, table_name, id=None):
        self.table_name = table_name
        self.id = id
        if self.id == None:
            print('id not provided')
        else:
            for item in self.id:
                self.conn.execute("DELETE from " + self.table_name + " where ID = " + str(item))
                self.conn.commit()
