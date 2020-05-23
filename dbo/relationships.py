from dbo.querybuilder import QueryBuilder


class Mapper(type):
    """The model's metaclass

    Every entity model has this class as its metaclass by virtue of extending the Model class
    It's only purpose is extending each newly defined class with an attribute with the relationship
    name and a newly constructed realtion query builder intance

    TODO: WIP, only generates the SQL code for select queries, does not execute, nor support other queries yet

    """
    def __new__(cls, name, bases, attr):
        """invoked after every new model class is defined

        if it includes a relmap relation, extend the new class definition with a relationship
        """

        newclass = super().__new__(cls, name, bases, attr)
        if 'relmap' in attr:
            for rel, relmap in attr['relmap']().items():
                setattr(newclass, rel, RelQueryBuilder(table = newclass, **relmap))

        return newclass


class RelQueryBuilder():
    """Relational query building class

    This class is responsible for structuring cross model queries between two related Models

    the queries attribute is another strategy pattern dictionary, currently only supporting select queries

    TODO: execution is WIP, currently generates the proper SQL query code
    """

    queries = {
        'select': lambda o: o.table.sql.inquery(o.main_query, o.side_query, o.to_col)
    }

    def __init__(self, table, target_table, from_col, to_col):
        """create a new relational querybuilder instance

        arguments:

        table:ModelClass -- the left side model in the relation
        target_table:ModelClass -- the right side model in the relation
        from_col:str -- the leftside foreign key
        to_col:tr -- the rightside foreign key 
        """
        self.table = table
        self.target_table = target_table
        self.from_col = from_col
        self.to_col = to_col
        self.query_type = 'select'
        

    def __call__(self, query=None, *args, **kwargs):
        """query is invocable to setup right side of the query

        keyword argument:
        query:QueryBuilder -- a pre-made query, used as is if passed in

        arguments:
        any other argument is used to generate a new QueryBuilder object from the target model
        """
        if query is None:
            self.main_query = self.target_table.find(*args, **kwargs)
        else:
            self.main_query = query
        return self


    def for_(self, query=None, *args, **kwargs):
        """query to set the left side of the query

        identical to the __call__ method, except if used without invoking the __call__ method,
        the main query would be null, so it is to set a query for the right side too
        """
        if query is None:
            self.side_query = self.table.find(*args, **kwargs)
        else:
            self.side_query = query
        
        if getattr(self, 'main_query', None) is None:
            self.main_query = self.target_table.find()
        return self

    def sql_code(self):
        """generates the sql code"""
        return self.queries[self.query_type](self)

    async def execute(self):
        pass

    def __await__(self):
        return self.execute.__await__()