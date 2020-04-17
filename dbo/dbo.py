from dbo.dialects import dialects
from dbo.querybuilder import QueryBuilder


class DBO:

    connection = None

    def __init__(self, dialect, **connection):
        Model_class = DBO.__subclasses__()[0]
        Model_class.sql = dialects[dialect]
        self.extender(Model_class, Model.sql.types)
        Model_class.sql.c = self.connector_initializer(dialect, connection)
        
        

    def connector_initializer(self, dialect, connection):
        if (dialect == 'mysql'):
            import dbo.db_wrappers.mysql as connector
            return connector.MysqlConnector(connection)
        else:
            raise Exception("Unsupported SQL Dialect!")
    
    @classmethod
    def execute(cls, query):
        cursor = DBO.connection.cursor(buffered=True)
        cursor.execute(query)
        DBO.connection.commit()
        return cursor

    def extender(self, sub_class, super_class):
        for item in super_class.__dict__.items():
            if('inhr_' in item[0]):
                setattr(sub_class, item[0][5:], item[1])


    @classmethod
    def executeIt(cls):
        pass



class Model(DBO):


    def __init__(self, data):
        attr = ["id", *self.__class__.get_key_attributes()]
        for key, value in zip(attr, data):
            self.__dict__[key] = value 

    @classmethod
    def find(cls, query_obj = None ,**query):
        if (query_obj is None):
            query_obj = {}
        query_obj.update(query)
        builder = QueryBuilder(
            cls.__name__,
            "select",
            cls.sql,
            cls.factory,
            conditions = query_obj
        )
        return builder
        # sql = cls.sql.find(cls.__name__, query_obj)
        # return cls.factory(cls.execute(sql).fetchall())

    @classmethod
    def insert(cls, query_obj = None ,**query):
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

        # sql = cls.sql.insert(cls.__name__, query_obj)
        # return cls.execute(sql)

        

    @classmethod
    def update(cls, values, query_obj = None, **query):
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

        # sql = cls.sql.update(cls.__name__, values, query_obj)
        # return cls.execute(sql)


    @classmethod
    def delete(cls, query_obj = None, **query):
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
        # sql = cls.sql.delete(cls.__name__, query_obj)
        # return cls.execute(sql)
        

    @classmethod
    def createTable(cls):
        sql = cls.sql.createTable(cls.__name__, cls.get_attributes())
        return cls.execute(sql)

    @classmethod
    def get_subclasses(cls):
        classes =  cls.__subclasses__()
        classes_attributes = [item.get_attributes() for item in classes]
        print(classes_attributes)
    
    @classmethod
    def get_attributes(cls):
        return dict(filter(lambda attr: "_" not in attr[0], cls.__dict__.items()))

    @classmethod
    def get_key_attributes(cls):
        return filter(lambda attr: "_" not in attr, cls.__dict__.keys())

    @classmethod
    def factory(cls, data):
        return [cls(item) for item in data]
