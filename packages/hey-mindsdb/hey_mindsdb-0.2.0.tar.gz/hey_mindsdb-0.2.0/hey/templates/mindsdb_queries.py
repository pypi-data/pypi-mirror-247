from string import Template

SQL_ASK_QUERY = Template('''
SELECT response
FROM mindsdb.gpt_model
WHERE author_username = "$user"
AND text = "$ask";
''')
