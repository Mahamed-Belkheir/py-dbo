from dbo import DBO

class Model(DBO):



    @classmethod
    def find(cls, query_obj = None ,**query):
        sql = cls.sql.find(cls.__name__)
        if (query):
            sql += cls.sql.and_query(**query)
        elif (query_obj):
            sql += cls.sql.and_query(**query_obj)
        return sql

    @classmethod
    def insert(cls, query_obj = {} ,**query):
        sql = cls.sql.insert(cls.__name__, **query_obj, **query)
        return sql
        

    @classmethod
    def update(clf):
        pass

    @classmethod
    def delete(clf):
        pass

    def get_subclasses(self):
        classes =  self.__class__.__subclasses__()
        classes_attributes = [cls.get_attributes() for cls in classes]
        print(classes_attributes)
    
    @classmethod
    def get_attributes(cls):
        return (cls.__name__, dict(filter(lambda attr: "_" not in attr[0], cls.__dict__.items())))


class Person(Model):
    pass


print(Person.find({'name': "john"}))
print(Person.insert(name='john', age=10))