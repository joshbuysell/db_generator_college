import json

def load_schema(path="schema.json"):
    with open(path, "r") as f:
        return json.load(f)

def create_mysql_database_if_not_exists(uri, db_name):
    import pymysql
    from sqlalchemy.engine.url import make_url

    url = make_url(uri)
    conn = pymysql.connect(
        host=url.host,
        user=url.username,
        password=url.password,
        port=url.port or 3306,
        database=None
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET 'utf8mb4';")
    cursor.close()
    conn.close()