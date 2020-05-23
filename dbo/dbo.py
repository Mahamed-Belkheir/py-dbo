from dbo.dialects import dialects
from dbo.querybuilder import QueryBuilder
from dbo.relationships import Mapper
from dbo.db_wrappers import connectors

class DBO:
    """The ORM entry point
    
    This class handle initializing the connection and SQL dialect for the Model class
    
    """

    def __init__(self, dialect, **connection):
        """Initialize the ORM

        arguments:
        dialect -- the SQL dialect chosen, currently only "mysql" is a valid choice
        connection -- the rest of the keyword arguments are passed to the DB connector configuration

        Chooses the correct connection wrapper and SQL dialect class
        Embeds the connection wrapper into the dialect class
        Embeds the dialect into the Model class
        Embeds the dialect class's DB Column type functions directly into the Model class

        The last part allows for a simpler API while defining model attributes
        
        """

        connector = self.connector_initializer(dialect, connection)

        dialect_class = dialects[dialect]
        dialect_class.set_connector(connector)

        Model.set_dialect(dialect_class)
        self.extender(Model, dialect_class.types)
        
        
        

    def connector_initializer(self, dialect, connection):
        """Finds the proper database connector and returns an instance"""

        if not connectors[dialect]:
            raise Exception(f"Did not find a valid DB connector for dialect: {dialect}")
        return connectors[dialect](connection)
            
    
    def extender(self, model_class, dialect_types):
        """Loops through the dialect type and embeds them into the model class"""

        for key, value in dialect_types.items():
            setattr(model_class, key, value)



class Model(DBO, metaclass=Mapper):
    """The M in the ORM
    
    This class is extended by all ORM Models and its methods serve as the API to access the ORM

    """

    def __init__(self, data):
        """Constructs instances of the Model Class
        
        If Data is a tuple, it came from the connector without attributes, we retrieve said attributes 
        from the class and attach them to the newly constructed object

        Dict data comes with the attributes so we do not need to retrieve the attributes

        TODO: validate inputted data

        """

        if (type(data) == tuple):
            attr = ['id', *self.__class__.get_key_attributes()]
            for key, value in zip(attr, data):
                self.__dict__[key] = value 
        elif (type(data) == dict):
            for key, value in data.items():
                self.__dict__[key] = value
        else:
            raise Exception(f"{self.__class__.__name__} Model Constructor recieved invalid data, only accepts tuples or dictionaries")

    @classmethod
    def set_dialect(cls, sql):
        """Sets the sql attribute with an SQL Dialect Class (internally used by ORM)"""
        cls.sql = sql

    @classmethod
    def find(cls, query_obj = None ,**query):
        """retrieve instances of the model

        accepts both an dict object, tuple or keyword arguments as a search query
        returns a QueryBuilder object with the set query, can be awaited to execute 

        """

        if (query_obj is None):
            query_obj = {}
            query_obj.update(query)


        builder = QueryBuilder(
            cls.__name__,
            "select",
            cls.sql,
            cls.factory,
            conditions = query_obj,
        )
        return builder


    @classmethod
    def insert(cls, query_obj = None ,**query):
        """insert one or many intances of the model

        accepts either an object, keyword arguments or an array of object to be inserted into the database
        returns a query object that you can execute with an await statement

        TODO: Add schema validation
        """

        if (query_obj is None):
            query_obj = {}
            query_obj.update(query)
        
        builder = QueryBuilder(
            cls.__name__,
            "insert",
            cls.sql,
            values = query_obj
        )
        return builder

    @classmethod
    def upsert(cls, query_obj = None ,**query):
        """insert or update instances of the model

        Works exactly like insert, except it updates models with uniqueness constraints

        returns a query object that can be awaited to execute
        """

        if (query_obj is None):
            query_obj = {}
            query_obj.update(query)
        
        builder = QueryBuilder(
            cls.__name__,
            "upsert",
            cls.sql,
            values = query_obj
        )
        return builder

        

    @classmethod
    def update(cls, values, query_obj = None, **query):
        """update intances of the model in the database

        accepts values as a dict that contains the attribute and the new values,
        and queries are either a dict with queries, a tuple or keyword arguments


        TODO: add schema validation
        """
        if (query_obj is None):
            query_obj = {}
            query_obj.update(query)
        
        builder = QueryBuilder(
            cls.__name__,
            "update",
            cls.sql,
            values = values,
            conditions = query_obj
        )
        return builder



    @classmethod
    def delete(cls, query_obj = None, **query):
        """deletes intances of the model from the database

        works exactly the same as the find or update method, needs an await to execute, returns nothing
        
        """

        if (query_obj is None):
            query_obj = {}
            query_obj.update(query)

        builder = QueryBuilder(
            cls.__name__,
            "delete",
            cls.sql,
            conditions = query_obj
        )
        return builder


    @classmethod
    def sync(cls):
        """creates a table representing the model
        
        Uses the model attributes as columns for the database schema
        return a query builder object, await to execute

        TODO: more elaborate table syncing 
        """
        builder = QueryBuilder(
            cls.__name__,
            "create",
            cls.sql,
            columns = cls.get_attributes()
        )
        return builder



    @classmethod
    def get_attributes(cls):
        """gets all attributes of Model that are of type string
        
        currently they represent the model columns, and are used in creating databases, also used with get key attribute

        TODO: give model attributes their own class so they are easily identifiable
        """
        return dict(filter(lambda attr: ("_" not in attr[0] and type(attr[1]) is str), cls.__dict__.items()))

    @classmethod
    def get_key_attributes(cls):
        """get all keys of model attributes, used in creating new model instances"""
        return list(cls.get_attributes().keys())

    @classmethod
    def factory(cls, data):
        """creates an array of model instances from an array of dicts"""
        return [cls(item) for item in data]



    def get_values(self):
        """gets the intance object values, used with the save method"""
        return dict(filter(lambda attr: ("_" not in attr[0] and callable(attr[1]) is not True), self.__dict__.items()))


    async def save(self):
        """updates the database record of the instance with changes made to its attributes"""
        await self.__class__.upsert(self.get_values())

    def delete_self(self):
        """deletes the intance from the database"""
        return self.__class__.delete(id=self.id) 