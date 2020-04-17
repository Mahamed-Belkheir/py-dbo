from dbo.dbo import DBO, Model
from dbo.dialects import Dialect_Mysql
from dbo.querybuilder import QueryBuilder
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
    x = await Person.find()
    print(x[0].greet())


if __name__ == "__main__":
    asyncio.run(main())