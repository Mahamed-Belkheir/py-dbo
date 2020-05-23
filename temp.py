import dbo.dialects.mysql as mysql

many_queries = [
    ("AND", ('age', '<', '30')),
    ("OR", ('salery', '>', '5000'))
]

single_dict_query = {
    "name": "Bob",
    "age": 20
}

many_dicts = [
    { "name": "Bob", "age": 50},
    { "name": "Shirley", "age": 32},
    { "name": "Chris", "age": 18},
    { "name": "Elena", "age": 21},
]
result = mysql.Dialect_Mysql.types['varchar'](100)

print(result)