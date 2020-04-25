from dbo import DBO, Model

import asyncio

DBO('mysql',
    host='localhost',
    user='dbman',
    passwd='',
    database='test_db'
    )


class School(Model):
    name = Model.varchar(255)
    budget = Model.integer(100)


class Person(Model):
    name = Model.varchar(255)
    age = Model.integer(100)
    school_id = Model.integer(100)

    def greet(self):
        return f"Hello, my name is {self.name}"

    def relmap(self=None):
        return {
           'school': {
                'model': School,
                'from_col': 'school_id',
                'to_col': 'id' 
           }
        }

async def main():
    await Person.sync()
    await School.sync()
    person_query = Person.find(('age', '<', 18))
    school_query = School.delete(('budget', '<', 1000))
    print(Person.school(query=school_query).for_(query=person_query).sql_code())

if __name__ == "__main__":
    asyncio.run(main())