from dbo.dbo import DBO, Model
import mysql.connector

DBO('mysql',
    host='localhost',
    user='dbman',
    passwd='',
    database='test_db'
    )

print(DBO.connection)

class Person(Model):
    name = Model.varchar(255)
    age = Model.integer(100)



print(Person.insert({'name': "bob", 'age': 19}))
print(Person.find())
print(Person.update({'age': 10}, name="bob"))
print(Person.find())

# print(Person.createTable())
# print(Person.insert({'name': "John", 'age': 19}))
# print(Person.insert({'name': "adam", 'age': 19}))
# print(Person.insert({'name': "bobby", 'age': 19}))
# print(Person.insert({'name': "Nick", 'age': 19}))
# print(Person.find())
# print(Person.delete(name = 'bob'))
# print(Person.find())
# print(Person.delete())
# print(Person.find())
# print(Person.update({'name': "adam"}, name="john"))
# print(Person.createTable())