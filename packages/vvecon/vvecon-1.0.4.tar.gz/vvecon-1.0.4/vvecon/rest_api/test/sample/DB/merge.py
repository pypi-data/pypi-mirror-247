from vvecon.rest_api.connections import get_connection
import re
from dotenv import load_dotenv
from os import environ, listdir

global columns

# load ENV
load_dotenv('../.env')
# initialize database connection
server_name = environ.get("SERVER")
database = environ.get("DATABASE")
user_name = environ.get("USER_NAME")
password = environ.get("PASSWORD")
db = get_connection(server_name, database, user_name, password)

folder = "Tables"
local = "Local"

files = listdir(folder)
local_files = listdir(local)


def table_exists(cursor, table):
    cursor.execute("""
    SHOW TABLES
    LIKE '{table}';
    """.format(table=table))
    return False if len(cursor.fetchall()) == 0 else True


def column_exists(cursor, table, column):
    cursor.execute("""
    SHOW COLUMNS
    FROM `{table}`
    LIKE '{column}';
    """.format(table=table, column=column))
    return False if len(cursor.fetchall()) == 0 else True


def create(query, table):
    try:
        with db as con:
            cursor = con.cursor()
            if not table_exists(cursor, table):
                print("'"+table+"' TABLE DOES NOT EXISTS.")
                cursor.execute(query)
                con.commit()
                print("'"+table+"' TABLE CREATED.")
    except Exception as e:
        print(e)


def alter(line, table):
    global columns
    try:
        with db as con:
            cursor = con.cursor()
            column = re.search(r"`(.*?)`", line).group(1)
            columns.append(column)
            if not column_exists(cursor, table, column):
                print("'"+column+"' COLUMN DOES NOT EXISTS ON TABLE '"+table+"'.")
                cursor.execute("""
                ALTER TABLE `{table}`
                ADD COLUMN {line};
                """.format(table=table, line=line[:-1]))
                print("'"+column+"' COLUMN CREATED")
            else:
                cursor.execute("""
                ALTER TABLE `{table}`
                MODIFY COLUMN {line};
                """.format(table=table, column=column, line=line[:-1]))
            con.commit()
    except Exception as e:
        print(e)


def primary(line, table):
    try:
        with db as con:
            cursor = con.cursor()
            column = re.search(r"`([^`]+)`", line).group(1)
            if column_exists(cursor, table, column):
                cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                cursor.execute("""
                ALTER TABLE `{table}`
                DROP PRIMARY KEY,
                ADD PRIMARY KEY (`{column}`);
                """.format(table=table, column=column))
                cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    except Exception as e:
        print(e)


def route(line, query, table):
    line = line.strip()
    if line.startswith('CREATE'):
        create(query, table)
    if line.startswith("`"):
        alter(line, table)
    if line.startswith('PRIMARY'):
        primary(line, table)


def remove(cursor, con, table, column):
    global columns
    print("INVALID '"+column+"' COLUMN ON TABLE '"+table+"'.")
    cursor.execute("""
    ALTER TABLE `{table_name}`
    DROP COLUMN `{column_name}`;
    """.format(table_name=table, column_name=column))
    con.commit()
    print("'" + column + "' COLUMN REMOVED")


def remove_false_columns(table):
    global columns
    with db as con:
        cursor = con.cursor()
        cursor.execute("""
        SHOW COLUMNS
        FROM `{table_name}`;
        """.format(table_name=table))
        result = cursor.fetchall()
        table_columns = [column_data[0] for column_data in result]
        for column in table_columns:
            if column not in columns:
                remove(cursor, con, table, column)


def truncate(table):
    with db as con:
        cursor = con.cursor()
        cursor.execute("TRUNCATE `{table_name}`".format(table_name=table))
        con.commit()


def merge(query):
    with db as con:
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()


if __name__ == "__main__":
    print("CHECKING TABLES")
    for file in files:
        if file.endswith('.sql'):
            with open(f"{folder}/{file}", 'r') as File:
                query = File.read().strip()
                lines = query.split('\n')
                table_match = re.search(r"CREATE TABLE `([^`]+)`", lines[0])
                if table_match:
                    table = table_match.group(1)
                    columns = []
                    for line in lines:
                        route(line, query, table)
                    remove_false_columns(table)

    print("UPDATING DATA ON LOCAL BACKUP")
    for file in local_files:
        with open(f"{local}/{file}", 'r') as File:
            query = File.read().strip()
            lines = query.split('\n')
            table_match = re.search(r"`([^`]+)`", lines[1])
            if table_match:
                table = table_match.group(1)
                truncate(table)
                merge(query)
