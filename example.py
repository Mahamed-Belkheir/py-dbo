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
    print(adam[0].greet())

    await Person.upsert({'id': adam[0].id, 'name': 'John'})
    adam = await Person.find()
    print(adam[0].greet())


    list_of_persons = await Person.find()
    print(f'we have {len(list_of_persons)}')

    await list_of_persons[0].delete_self()

    list_of_persons = await Person.find()
    print(f'we have {len(list_of_persons)}')
    
    new_guy = Person({'name': "new guy", 'age': 1000})
    await new_guy.save()
    
    list_of_persons = await Person.find()
    print(f'we have {len(list_of_persons)}')

if __name__ == "__main__":
    asyncio.run(main())