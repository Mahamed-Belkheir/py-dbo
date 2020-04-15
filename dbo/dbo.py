from dbo.dialects import dialects



class DBO:


    def __init__(self, dialect):
        Model = DBO.__subclasses__()[0]
        Model.sql = dialects[dialect]
        self.extender(Model, Model.sql.types)

    def execute(self):
        pass

    def extender(self, sub_class, super_class):
        for item in super_class.__dict__.items():
            if('inhr_' in item[0]):
                setattr(sub_class, item[0][5:], item[1])


    @classmethod
    def executeIt(cls):
        pass



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

    @classmethod
    def createTable(cls):
        return cls.sql.createTable(cls.__name__, cls.get_attributes())

    @classmethod
    def get_subclasses(cls):
        classes =  cls.__subclasses__()
        classes_attributes = [item.get_attributes() for item in classes]
        print(classes_attributes)
    
    @classmethod
    def get_attributes(cls):
        return dict(filter(lambda attr: "_" not in attr[0], cls.__dict__.items()))


