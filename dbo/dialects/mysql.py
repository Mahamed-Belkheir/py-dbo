

class Dialect_Mysql:
    """MySQL dialect SQL code generator
    
    Handles converting QueryBuilders into MySQL dialect SQL code
    Includes the column types that Models use to define attributes
    
    """  
    

    types = {
        'varchar': lambda length: f'VARCHAR({length})',
        'text': lambda length: f'TEXT({length})',
        'integer': lambda length: f'INT({length})',
        'float': lambda length: f'FLOAT({length})',
        'boolean': lambda: f'BOOL',
        'datetime': lambda: f'DATETIME',
    }

    @classmethod
    def set_connector(cls, conn):
        """embeds the mysql connection wrapper into the class"""

        cls.c = conn

    @staticmethod
    def find(table, queries=None, include=None):
        """generate SELECT query code and returns it as string"""

        if include is None:
            include = '*'
        else:
            include = ','.join(include)
        sql = f"SELECT {include} FROM {table}"
        if (queries):
            sql += where_query(queries)
        return sql

    @staticmethod
    def insert(table, values):
        """generates INSERT query code and returns it as string"""
        sql = f"INSERT INTO `{table}` ({','.join(map(lambda x: '`'+x+'`', values[0].keys()))})  VALUES {values_get(values)}"
        return sql

    @staticmethod
    def delete(table, query=None):
        """generates DELETE query code and returns it as string"""
        sql = f"DELETE FROM {table}"
        if (query):
            sql += where_query(query)
        return sql

    @staticmethod
    def update(table, values, query):
        """generates UPDATE query code and returns it as string"""
        return f"UPDATE {table} SET {update_sep(values)} {where_query(query)}"

    @classmethod
    def upsert(cls, table, values):
        """ generates an upsert query

        generates INSERT query code and adds an on duplicate key update clause,
        returns an upsert equivalent query as string
        """
        
        return cls.insert(table, values) + " ON DUPLICATE KEY UPDATE "+ ','.join([key + f' = VALUES({key})' for key in values[0].keys()])

    @classmethod
    def inquery(cls, query, inquery, col):
        """generate an IN query using two queries and the column used to query

        starter is the keyword used to connect the two queries, if the first query has no conditions, then we must use WHERE

        """
        starter = "AND"
        if len(query.conditions) == 0:
            starter = "WHERE"
        return f"{query.sql_code()} {starter} {col} IN ({inquery.sql_code()})"



    @staticmethod
    def createtable(table, attributes):
        """generates table creation SQL code based on class attributes"""
        sql = f"""CREATE TABLE IF NOT EXISTS {table} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {','.join([item[0]+" "+item[1] for item in attributes.items()])}
            )"""
        return sql


    


def and_query(query):
    """helper function that turns a query dictionary into a string of where clauses"""
    return " WHERE (" + dict_sep(' AND ', query) +")"

def where_query(queries):
    """helper function that generates a where statement, based on multiple queries of different types
    
    the queries array is an array of tuples, the first element is the condition type, either OR or AND
    the second is the query itself, either another tuple of conditions with an operator or a dictionary

    if the query is of type tuple, it simply joins it together
    if the query is a dictionary, it uses the dict_sep helper function

    queries are joined together by their type, either OR or AND
    
    """
    sql = ""
    for query in queries:
        if type(query[1]) == list or type(query[1]) == tuple:
            sql += " "+query[0] +" (" + ''.join([ str(op) for op in query[1] ]) +")"
        else:
            sql += " "+query[0] +" (" + dict_sep(", ", query[1])+")"
    sql = ' WHERE ' + sql[4:]
    return sql

def dict_sep(seperator, dictionary):
    """join a dictionary element together with a specified seperator (OR or AND)"""
    return seperator.join([item[0]+'=\''+str(item[1])+'\'' for item in dictionary.items()])

def update_sep(values):
    """like dict_sep, but adds backticks to columns due to UPDATE statements requiring them in MySQL"""
    return ', '.join(['`'+item[0]+'`'+'=\''+str(item[1])+'\'' for item in values.items()])

def values_get(values):
    """takes an array of value dictionaries and returns them in INSERT values format"""
    sql = []
    for item in values:
        sql.append('(' + ','.join([ '\'' + str(x) + '\'' for x in item.values()]) + ')')
    return ",".join(sql)
    


