class Dialect_Mysql:

    @staticmethod
    def find(table):
        return f"SELECT * FROM {table}"

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
    def and_query(**kawrgs):
        return " AND ".join([item[0]+'='+str(item[1]) for item in kawrgs.items()])





dialects = {
    "mysql": Dialect_Mysql
}

