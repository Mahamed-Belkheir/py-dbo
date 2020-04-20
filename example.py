from dbo import DBO, Model

import asyncio

DBO('mysql',
    host='localhost',
    user='dbman',
    passwd='',
    database='test_db'
    )


class Person(Model):
    name = Model.varchar(255)
    age = Model.integer(100)

    def greet(self):
        return f"Hello, my name is {self.name}"


async def main():
    await Person.sync()
    await Person.insert([
        {'name': 'Adam', 'age': 23},
        {'name': 'John', 'age': 19},
        {'name': 'Bob', 'age': 42},
        {'name': 'Rick', 'age': 37},
    ])
    people = await Person.find()
    for person in people:
        print(person.greet())
    youngsters = await Person.find(('age', '<', 30)).orwhere(('age', '>', '40'))
    for person in youngsters:
        print(person.greet())
    await Person.delete()
    await Person.upsert({'name': 'Adam', 'age': 23})
    adam = await Person.find()
    print(adam[0].id)
    await Person.upsert({'id': adam[0].id, 'name': 'John'})
    adam = await Person.find()
    print(adam[0].id)

if __name__ == "__main__":
    asyncio.run(main())