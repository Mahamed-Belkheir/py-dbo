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
    await Person.sync()


if __name__ == "__main__":
    asyncio.run(main())