from dbo.model import Model


class Person(Model):
    pass


print(Person.find({'name': "john"}))
print(Person.insert({'name': "john", 'age': 19}))
print(Person.delete())
print(Person.delete(name = 'bob'))
print(Person.update({'name': "adam"}, name="john"))
