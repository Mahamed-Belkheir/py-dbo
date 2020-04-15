from dbo.dbo import DBO, Model
DBO('mysql')


class Person(Model):
    name = Model.varchar(255)
    age = Model.integer(100)


print(Person.find({'name': "john"}))
print(Person.insert({'name': "john", 'age': 19}))
print(Person.delete())
print(Person.delete(name = 'bob'))
print(Person.update({'name': "adam"}, name="john"))
print(Person.createTable())