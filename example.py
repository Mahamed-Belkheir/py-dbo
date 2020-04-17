from dbo.dbo import DBO, Model
from dbo.dialects import Dialect_Mysql
from dbo.querybuilder import QueryBuilder

import mysql.connector


# query = QueryBuilder(
#     "Person", "select", Dialect_Mysql,
#     {'job': 'HR'}
# )
# print(query.orwhere({'job': 'programmer'}).execute())
# print(QueryBuilder("Person", "insert", Dialect_Mysql, values = [{"name": "bob", "age": 40},{"name": "bob", "age": 40}]).execute())
# print(
#     QueryBuilder("Person", "delete", Dialect_Mysql)
#     .andwhere({'name': "adam"})
#     .execute()
# )
# print(
#     QueryBuilder("Person", "update", Dialect_Mysql, values=[{'age':23}], conditions={'name': 'bob'})
#     .execute()
# )














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

    def greet(self):
        return f"Hello, my name is {self.name}"



print(Person.insert([{'name': "bob", 'age': 19},{'name': "john", 'age': 23}]).execute())
print(Person.find(name='bob').orwhere(age=52).execute())
print(Person.update({'age': 10}, name="bob", job="worker").execute())
print(Person.delete().execute())
# print(Person.find())

# print(Person.createTable())
# print(Person.insert({'name': "John", 'age': 19}))
# print(Person.insert({'name': "adam", 'age': 19}))
# print(Person.insert({'name': "bobby", 'age': 19}))
# print(Person.insert({'name': "Nick", 'age': 19}))
# print(Person.find())
# print(Person.find())
# print(Person.delete())
# print(Person.find())
# print(Person.update({'name': "adam"}, name="john"))
# print(Person.createTable())