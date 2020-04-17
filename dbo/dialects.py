class Mysql_Types:

    @staticmethod
    def inhr_varchar(length):
        return f"VARCHAR({length})"

    @staticmethod
    def inhr_text(length):
        return f"TEXT({length})"

    @staticmethod
    def inhr_integer(length):
        return f"INT({length})"

    @staticmethod
    def inhr_date():
        return "DATETIME"



class Dialect_Mysql:

    types = Mysql_Types

    @staticmethod
    def find(table, queries=None):
        sql = f"SELECT * FROM {table}"
        if (queries):
            sql += where_query(queries)
        return sql

    @staticmethod
    def insert(table, values):
        return f"INSERT INTO `{table}` ({','.join(map(lambda x: '`'+x+'`', values[0].keys()))})  VALUES {values_get(values)}"

    @staticmethod
    def delete(table, query=None):
        sql = f"DELETE FROM {table}"
        if (query):
            sql += where_query(query)
        return sql

    @staticmethod
    def update(table, values, query):
        return f"UPDATE {table} SET {update_sep(values)} {where_query(query)}"



    @staticmethod
    def createTable(table, attributes):
        sql = f"""CREATE TABLE IF NOT EXISTS {table} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {','.join([item[0]+" "+item[1] for item in attributes.items()])}
            )"""
        return sql


    


def and_query(query):
    return " WHERE (" + dict_sep('AND', query) +")"

def where_query(queries):
    sql = " WHERE (" + dict_sep(", ", queries[0][1]) +")"
    for query in queries[1:]:
        sql += " "+query[0] +" (" + dict_sep(", ", query[1])+")"
    return sql

def dict_sep(seperator, dictionary):
    return seperator.join([item[0]+'=\''+str(item[1])+'\'' for item in dictionary.items()])

def update_sep(values):
    return ', '.join(['`'+item[0]+'`'+'=\''+str(item[1])+'\'' for item in values.items()])

def values_get(values):
    sql = []
    for item in values:
        sql.append('(' + ','.join([ '\'' + str(x) + '\'' for x in item.values()]) + ')')
    return ",".join(sql)
    

dialects = {
    "mysql": Dialect_Mysql,
}

