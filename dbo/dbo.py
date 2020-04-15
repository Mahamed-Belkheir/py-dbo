from dbo.dialects import dialects



class DBO:


    def __init__(self, dialect):
        DBO.sql = dialects[dialect]

    def generate_class_sql(self):
        pass
    
    def execute(self):
        pass


    @classmethod
    def executeIt(cls):
        pass



class TestClass(DBO):
    name = 'string'
    password = 'number'


