# PyDBO

This project is a learning attempt at writing a simple, limited ORM
Heavily inspired by Node JS's Objection ORM in API design, I aim to keep
the API simpler at the expense of higher code complexity,
as this will also force me to learn more about the obscure parts of Python.

### Features

You can easily define entity model classes, and have a basic API for CRUD operations through your class, currently the find method also constructs instances of your class, any methods you define on your class would be available on objects you retrieve from the database.

All the methods are also Async, using await is how you execute queries

### How to use:

 - Import the DBO and Model classes
 - Initialize a DBO Object with the dialect (currently only mysql) and connection details (you don't need to save it)
 - Define your entity class and extend the Model class
 - Define properties in your class Using the Model's inherited types (found in dialects.py types class)


### TODO:

There's still a lot left to do here, this is nowhere near useable for production, unless you're feeling adventurous.
Things left to do in the near future:
 - Rename variables and methods to be more self explanatory, resture some of the classes
 - Validate queries against the model before they are executed
 - Add more complex query generation
 - Improve on the naive implementation for query execution

###### Things to do in the far future (if ever):

- Implementing naive Model Relationships and their queries
- Implementing naive Transaction Support



### Project Structure

The structure is currently a mess, and will require refactoring, but as it stands now:

###### DBO Class

This is the central class, and it mostly exists for holding other objects, and for initializing a database connection.
On initialization, it picks the chosen sql dialect from the dialects.py classes,
and attaches it to the Model class. It also retrieves the Dialect Types class and extends its attributes directly to the Model class, this is done so that users have a faster access to types while initializing their entity models.

###### Dialect and Dialect Type Classes

These classes hold all the SQL dialect specific functions, for SQL code generation, and are currently the biggest source of code smell, the folder also holds some generic helper functions that should be moved elsewhere. The Type Classes might turn into a dictionary of functions instead, it was originally a class in hopes of extending the Model class post definition, but that was not feasible(if I redefine the Model class, that would not change the already defined entity models that already have extended the old Model class)

###### Model

This is the class that is extended by any user defined entity classes, and therefore it is the class responsible for exposing the majority of the ORM API.
The class has a 'has a' relationship with the sql dialect class, infact, it has THE class itself, (the code base makes extensive use of class methods to reduce the need of intiailization of objects and managing initialization order).
The CRUD API it exposes return a QueryBuilder instance, which is passed the class's name, the sql dialect class chosen on intialization and the type of query made, alongside the arguments passed to the method itself.

###### QueryBuilder

This class is responsible for putting together your query, and to only execute on an await statement, it's responsible for constructing the query through the sql dialect class it is passed on construction, the table name, the query type(select, insert, etc...) and the query parameters. the query is also extendable through the exposed methods, currently `orwhere` and `andwhere`, these add more conditions for the query, and then return the object itself, so they're chainable.
The class also implements an await method, making it awaitable, and that is the correct wait to execute queries, you could also call the `execute` method directly but that would be ignoring all the pain I've went through to have it work this nicely.

###### DB wrappers

Currently just a naive class that wraps over the mysql.connector, and offering an async method to execute queries
