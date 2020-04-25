
class QueryBuilder:

    
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
        self.table = table
        self.query_type = query_type
        self.sql = sql
        self.factory = factory
        self.conditions = []
        self.values = []
        if conditions:
            self.conditions.append(("AND", conditions))
        if values:
            if type(values) == list:
                self.values = values
            else:
                self.values.append(values)
        self.targets = targets
        self.columns = columns
        self.include = include

    def orwhere(self, conditions=None, **conds):
        if(conditions is None):
            conditions = conds
        self.conditions.append(("OR", conditions))
        return self
    
    def andwhere(self, conditions=None, **conds):
        if(conditions is None):
            conditions = conds
        self.conditions.append(("AND", conditions))
        return self

    def includecolumns(self, *include):
        self.include = include
        return self

    def sql_code(self):
        return self.queries[self.query_type](self)

    async def execute(self):
        sql = self.sql_code()
        result = await self.sql.c.invoke(sql)
        if (self.query_type == "select"):
            result = self.factory(result.fetchall())
        return result

    def __await__(self):
        return self.execute().__await__()