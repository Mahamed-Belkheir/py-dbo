class Dialect_Mysql:

    @staticmethod
    def find(table, query={}):
        sql = f"SELECT * FROM {table}"
        if (query):
            sql += and_query(query)
        return sql

    @staticmethod
    def insert(table, values):
        return f"INSERT ({','.join(values.keys())}) INTO {table} VALUES ({','.join([str(x) for x in values.values()])})"

    @staticmethod
    def delete(table, query={}):
        sql = f"DELETE FROM {table}"
        if (query):
            sql += and_query(query)
        return sql

    @staticmethod
    def update(table, values, query):
        return f"UPDATE {table} SET {dict_sep(',', values)}{and_query(query)}"



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
    



def and_query(query):
    return " WHERE (" + dict_sep('AND', query) +")"
def dict_sep(seperator, dictionary):
    return seperator.join([item[0]+'='+str(item[1]) for item in dictionary.items()])

dialects = {
    "mysql": Dialect_Mysql
}

