from dbo.dbo import DBO

class Model(DBO):

    @classmethod
    def find(cls, query_obj = {} ,**query):
        query_obj.update(query)
        sql = cls.sql.find(cls.__name__, query_obj)
        return sql

    @classmethod
    def insert(cls, query_obj = {} ,**query):
        query_obj.update(query)
        sql = cls.sql.insert(cls.__name__, query_obj)
        return sql
        

    @classmethod
    def update(cls, values, query_obj = {}, **query):
        query_obj.update(query)
        sql = cls.sql.update(cls.__name__, values, query_obj)
        return sql

    @classmethod
    def delete(cls, query_obj = {}, **query):
        query_obj.update(query)
        sql = cls.sql.delete(cls.__name__, query_obj)
        return sql

    def get_subclasses(self):
        classes =  self.__class__.__subclasses__()
        classes_attributes = [cls.get_attributes() for cls in classes]
        print(classes_attributes)
    
    @classmethod
    def get_attributes(cls):
        return (cls.__name__, dict(filter(lambda attr: "_" not in attr[0], cls.__dict__.items())))


