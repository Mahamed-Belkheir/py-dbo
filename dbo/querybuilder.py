
class QueryBuilder:

    
    queries = {
        "select": lambda o: o.sql.find(o.table, o.conditions),
        "insert": lambda o: o.sql.insert(o.table, o.values),
        "update": lambda o: o.sql.update(o.table, o.values[0], o.conditions),
        "delete": lambda o: o.sql.delete(o.table, o.conditions)
    }

    def __init__(self,
    table:str, query_type:str, sql, factory=None,
    conditions:dict=None, values=None, targets:list=None
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
        if targets:
            self.targets = targets

    def orwhere(self, conditions=None, **conds):
        if(conditions is None):
            conditions = conds
        self.conditions.append(("OR", conditions))
        return self
    
    def andwhere(self, conditions, **conds):
        if(conditions is None):
            conditions = conds
        self.conditions.append(("AND", conditions))
        return self


    async def execute(self):
        sql = self.queries[self.query_type](self)
        result = await self.sql.c.invoke(sql)
        if (self.query_type == "select"):
            result = self.factory(result.fetchall())
        return result

    def __await__(self):
        return self.execute().__await__()