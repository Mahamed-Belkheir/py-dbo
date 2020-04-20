

class Dialect_Mysql:
    
    types = {
        'varchar': lambda length: f'VARCHAR({length})',
        'text': lambda length: f'TEXT({length})',
        'integer': lambda length: f'INT({length})',
        'float': lambda length: f'FLOAT({length})',
        'boolean': lambda length: f'BOOL',
        'datetime': lambda length: f'DATETIME',
    }

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

    @classmethod
    def upsert(cls, table, values):
        return cls.insert(table, values) + " ON DUPLICATE KEY UPDATE "+ ','.join([key + f' = VALUES({key})' for key in values[0].keys()])

    @staticmethod
    def createtable(table, attributes):
        sql = f"""CREATE TABLE IF NOT EXISTS {table} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {','.join([item[0]+" "+item[1] for item in attributes.items()])}
            )"""
        return sql


    


def and_query(query):
    return " WHERE (" + dict_sep('AND', query) +")"

def where_query(queries):
    sql = ""
    for query in queries:
        if type(query[1]) == list or tuple:
            sql += " "+query[0] +" (" + ''.join([ str(op) for op in query[1] ]) +")"
        else:
            sql += " "+query[0] +" (" + dict_sep(", ", query[1])+")"
    return ' WHERE ' + sql[4:]

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

