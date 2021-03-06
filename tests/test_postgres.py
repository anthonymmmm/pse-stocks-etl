from pandas import DataFrame
from utils.postgres import creds
from utils.postgres import read_sql_file, template_query, query

    
def test_db_endpoint_defined():
    assert creds['db_endpoint'] is not None
    
def test_db_username_defined():
    assert creds['db_username'] is not None
    
def test_db_password_defined():
    assert creds['db_password'] is not None
    
def test_db_port_defined():
    assert creds['db_port'] is not None
    
def test_db_name_defined():
    assert creds['db_name'] is not None
    
def test_read_sql_file():
    sql_stmt = 'SELECT 1 AS col;'
    assert sql_stmt == read_sql_file('tests/sample_sql_file.sql')

def test_template_query():
    raw_stmt = """
        SELECT
              '{{string_value}}' AS {{string_column}}
            , {{int_value}} AS {{int_column}}
            
        FROM {{schema}}.{{table}};
    """
    
    templated_stmt = """
        SELECT
              'sample_string' AS my_str_col
            , 10 AS my_int_col
            
        FROM my_schema.my_table;
    """
    
    params = {
        'schema':'my_schema',
        'table':'my_table',
        'string_value':'sample_string',
        'string_column':'my_str_col',
        'int_value':10,
        'int_column':'my_int_col'
    }
    
    assert templated_stmt == template_query(raw_stmt, params)
    
def test_query_stmt():
    stmt = 'SELECT 1 AS col;'
    assert query(stmt).to_dict('records') == [{'col':1}]
    
def test_query_sql_file():
    stmt = read_sql_file('tests/sample_sql_file.sql')
    assert query(stmt).to_dict('records') == [{'col':1}]
    
def test_query_parameters():
    stmt = 'SELECT {{value}} AS {{colname}};'
    params = {'value':1, 'colname':'col'}
    assert query(stmt, parameters=params).to_dict('records') == [{'col':1}]
    
def test_query_retrieve_result_true():
    stmt = 'SELECT 1 AS col;'
    assert query(stmt, retrieve_result=True).to_dict('records') == [{'col':1}]
    
def test_query_retrieve_result_false():
    stmt = 'SELECT 1 AS col;'
    assert query(stmt, retrieve_result=False) == True