class Dialect_Mysql:

    @staticmethod
    def find(table):
        return f"SELECT * FROM {table}"

    @staticmethod
    def insert(table, **values):
        return f"INSERT ({','.join(values.keys())}) INTO {table} VALUES ({','.join([str(x) for x in values.values()])})"

    @staticmethod
    def varchar(self, length):
        return f"VARCHAR(${length}),"

    @staticmethod
    def text(self, length):
        return f"TEXT(${length}),"

    @staticmethod
    def integer(self, length):
        return f"INT(${length}),"

    @staticmethod
    def date(self):
        return "DATETIME,"
    
    @staticmethod
    def and_query(**query):
        return " WHERE (" + " AND ".join([item[0]+'='+str(item[1]) for item in query.items()]) +")"





dialects = {
    "mysql": Dialect_Mysql
}

