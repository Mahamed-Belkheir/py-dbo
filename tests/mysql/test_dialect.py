import dbo.dialects.mysql as mysql

single_dict_query = {
    "name": "Bob",
    "age": 20
}

two_operator_queries = [
    ("AND", ('age', '<', '30')),
    ("OR", ('salery', '>', '5000'))
]

many_dicts = [
    { "name": "Bob", "age": 50},
    { "name": "Shirley", "age": 32},
    { "name": "Chris", "age": 18},
    { "name": "Elena", "age": 21},
]

def test_helper_functions():
    dict_sep_result = mysql.dict_sep(" AND ", single_dict_query)
    assert dict_sep_result == "name='Bob' AND age='20'"

    and_query_result = mysql.and_query(single_dict_query)
    assert and_query_result == " WHERE (name='Bob' AND age='20')"

    where_query_result = mysql.where_query(two_operator_queries)
    assert where_query_result == " WHERE  (age<30) OR (salery>5000)"

    update_sep_result = mysql.update_sep(single_dict_query)
    assert update_sep_result == "`name`='Bob', `age`='20'"

    values_get_result = mysql.values_get(many_dicts)
    assert values_get_result == "('Bob','50'),('Shirley','32'),('Chris','18'),('Elena','21')"

def test_column_types():
    varchar_result = mysql.Dialect_Mysql.types['varchar'](100)
    assert varchar_result == "VARCHAR(100)"

    text_result = mysql.Dialect_Mysql.types['text'](100)
    assert text_result == "TEXT(100)"

    int_result = mysql.Dialect_Mysql.types['integer'](100)
    assert int_result == "INT(100)"

    float_result = mysql.Dialect_Mysql.types['float'](100)
    assert float_result == "FLOAT(100)"

    boolean_result = mysql.Dialect_Mysql.types['boolean']()
    assert boolean_result == "BOOL"

    datetime_result = mysql.Dialect_Mysql.types['datetime']()
    assert datetime_result == "DATETIME"
