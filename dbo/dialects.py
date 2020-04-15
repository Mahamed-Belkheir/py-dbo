class Mysql_Types:

    @staticmethod
    def varchar(length):
        return f"VARCHAR({length})"

    @staticmethod
    def text(length):
        return f"TEXT({length})"

    @staticmethod
    def integer(length):
        return f"INT({length})"

    @staticmethod
    def date():
        return "DATETIME"



class Dialect_Mysql:

    types = Mysql_Types

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
    def createTable(table, attributes):
        return f"""CREATE TABLE {table} (
            id BIGINT,
            {','.join([item[0]+" "+item[1] for item in attributes.items()])},
            PRIMARY KEY (id)
            )"""


    


def and_query(query):
    return " WHERE (" + dict_sep('AND', query) +")"
def dict_sep(seperator, dictionary):
    return seperator.join([item[0]+'='+str(item[1]) for item in dictionary.items()])

dialects = {
    "mysql": Dialect_Mysql,
}

