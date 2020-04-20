from dbo.dbo import DBO, Model

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
    await Person.insert({"name": "Adam", "age": 90})
    x = await Person.find()
    print(x[0].greet())
    await Person.update({"age": 21}, name="Adam")
    x = await Person.find()
    print(x[0].__dict__)
    await Person.delete()
    x = await Person.find()
    print(Person.get_key_attributes())


if __name__ == "__main__":
    asyncio.run(main())