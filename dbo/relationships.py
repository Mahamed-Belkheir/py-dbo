from dbo.querybuilder import QueryBuilder


class Mapper(type):
    def __new__(cls, name, bases, attr):
        newclass = super().__new__(cls, name, bases, attr)
        if 'relmap' in attr:
            for rel, relmap in attr['relmap']().items():
                setattr(newclass, rel, RelQueryBuilder(table = newclass, **relmap))

        return newclass


class RelQueryBuilder():

    queries = {
        'select': lambda o: o.table.sql.inquery(o.main_query, o.side_query, o.to_col)
    }

    def __init__(self, table, model, from_col, to_col):
        self.table = table
        self.target_table = model
        self.from_col = from_col
        self.to_col = to_col
        self.query_type = 'select'
        

    def __call__(self, query=None, *args, **kwargs):
        if query is None:
            self.main_query = self.target_table.find(*args, **kwargs)
        else:
            self.main_query = query
        return self

    def for_(self, query=None, *args, **kwargs):
        if query is None:
            self.side_query = self.table.find(*args, **kwargs)
        else:
            self.side_query = query
        if getattr(self, 'main_query', None) is None:
            self.main_query = self.target_table.find()
        return self

    def sql_code(self):
        return self.queries[self.query_type](self)

    async def execute(self):
        pass

    def __await__(self):
        return self.execute.__await__()