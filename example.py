from dbo import DBO, Model

import asyncio

# You only need to initialize the ORM by creating a new object
DBO('mysql',
    host='localhost',
    user='dbman',
    passwd='',
    database='test_db'
    )


# an entity class is defined by extending Model
class Person(Model):
    name = Model.varchar(255)
    age = Model.integer(100)

    def greet(self):
        return f"Hello, my name is {self.name}"



async def main():
    # create the Person table
    await Person.delete()

    await Person.sync()
    
    #insert multiple Peron entities
    await Person.insert([
        {'name': 'Adam', 'age': 23},
        {'name': 'John', 'age': 19},
        {'name': 'Bob', 'age': 42},
        {'name': 'Rick', 'age': 37},
    ])

    #retrieve all Persons
    people = await Person.find()
    
    #loop through all results, and invoke the method defined in the Person class
    for person in people:
        print(person.greet())

    #find bv dictionary
    adam = await Person.find({"name":"Adam"}).first()
    print(f"Hello There!\n {adam.greet()}")

    #queries using logical operators
    age_group = await Person.find(('age', '>', 30)).orwhere(('age', '<', '40'))
    for person in age_group:
        print(person.greet())

    #delete all
    await Person.delete()

    #upsert while there's no entities
    await Person.upsert({'name': 'Adam', 'age': 23})
    adam = await Person.find(name="Adam").first()
    print(adam.greet())

    #upsert the same intance to update it
    await Person.upsert({'id': adam.id, 'name': 'John'})
    adam = await Person.find(id=adam.id).first()
    print(adam.greet())

    #count how many persons there are
    list_of_persons = await Person.find()
    print(f'we have {len(list_of_persons)}')

    #delete one item after retrieving it
    await list_of_persons[0].delete_self()

    #count how many exist now
    list_of_persons = await Person.find()
    print(f'we have {len(list_of_persons)}')
    
    #save a new person into the DB after manually instantiating them
    new_guy = Person({'name': "new guy", 'age': 1000})
    await new_guy.save()
    
    #counting how many exist
    list_of_persons = await Person.find()
    print(f'we have {len(list_of_persons)}')

   

if __name__ == "__main__":
    asyncio.run(main())