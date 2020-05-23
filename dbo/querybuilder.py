
class QueryBuilder:
    """The query constructing class
    
    Handles creating and executing queries, and allow chaining methods to generate queries

    queries attribute is a strategy pattern object, handles calling the proper sql dialect sql generator
    based on the type of query is being made, passing in the values

    queries are executed through using await on the object, until then, no queries are made to the database
    
    """
    
    queries = {
        "select": lambda o: o.sql.find(o.table, o.conditions, o.include),
        "insert": lambda o: o.sql.insert(o.table, o.values),
        "upsert": lambda o: o.sql.upsert(o.table, o.values),
        "update": lambda o: o.sql.update(o.table, o.values[0], o.conditions),
        "delete": lambda o: o.sql.delete(o.table, o.conditions),
        "create": lambda o: o.sql.createtable(o.table, o.columns)
    }

    def __init__(self,
    table:str, query_type:str, sql, factory=None,
    conditions:dict=None, values=None, targets:list=None,
    columns=None, include=None
    ):
        """create a new query builder object

        arguments:
        table:string -- the model's name, which is also the table name
        query_type:string -- the type of query made
        sql:DialectClass -- the SQL dialect class  
        factory:callable -- the model's factory method
        conditions:dict -- the queries WHERE clauses
        values:dict|list -- the values to INSERT or UPDATE queries
        columns:list -- the table's column
        include:list -- columns to include in the result (not used)

        """
        self.table = table
        self.query_type = query_type
        self.sql = sql
        self.factory = factory
        self.conditions = []
        self.values = []
        self.one = False
        if conditions:
            self.conditions.append(("AND", conditions))
        if values:
            if type(values) == list:
                self.values = values
            else:
                self.values.append(values)
        self.columns = columns
        self.include = include

    def orwhere(self, conditions=None, **conds):
        """adds OR conditions to query"""
        if(conditions is None):
            conditions = conds
        self.conditions.append(("OR", conditions))
        return self
    
    def andwhere(self, conditions=None, **conds):
        """adds AND condition to query"""
        if(conditions is None):
            conditions = conds
        self.conditions.append(("AND", conditions))
        return self

    def includecolumns(self, *include):
        """set which columns to include in result"""
        self.include = include
        return self

    def first(self):
        self.one = True;
        return self

    def sql_code(self):
        """returns the queries' sql code"""
        return self.queries[self.query_type](self)

    async def execute(self):
        """asynchronously execute the query
        
        this function is used by the __await__ method, since it can't be an aysnc function

        it generates the query code uing the sql_code method and passes it to the Dialect Class's embedded
        DB connection wrapper. which executes the query and return the result

        incase of a select query, we use the model's factory method to create instances of the model

        """
        sql = self.sql_code()
        result = await self.sql.c.invoke(sql)
        if (self.query_type == "select"):
            result = self.factory(result.fetchall())
            if self.one:
                result = result[0]
        return result

    def __await__(self):
        """executes the query on an await statement"""
        return self.execute().__await__()