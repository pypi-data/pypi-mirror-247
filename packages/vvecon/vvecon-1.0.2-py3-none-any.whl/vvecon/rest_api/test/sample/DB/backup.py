import os.path
from os import environ
from dotenv import load_dotenv
from vvecon.rest_api.connections import get_connection

# load ENV
load_dotenv('../.env')
# initialize database connection
server_name = environ.get("SERVER")
database = environ.get("DATABASE")
user_name = environ.get("USER_NAME")
password = environ.get("PASSWORD")
db = get_connection(server_name, database, user_name, password)

folder = "Backup"
tables = []


def backup(table):
    with db as con:
        cursor = con.cursor()
        query = """INSERT INTO\n`{table_name}`\n""".format(table_name=table)

        cursor.execute(f"SELECT * FROM {table}")
        columns = [column_data[0] for column_data in cursor.description]
        query += """({columns})\nVALUES\n""".format(
            columns=", ".join(["`{column}`".format(column=column) for column in columns])
        )
        result = cursor.fetchall()
        query += ",\n".join(["({record})".format(
            record=", ".join(["'{data}'".format(data=data) for data in record])) for record in result]
        )
        query += ";"
        print(query)
        if len(result) > 0:
            if not os.path.isfile(f"{folder}/{table}.sql"):
                with open(f"{folder}/{table}.sql", 'x', encoding='utf-8') as File:
                    File.write(query)
            else:
                with open(f"{folder}/{table}.sql", 'w', encoding='utf-8') as File:
                    File.write(query)


if __name__ == "__main__":
    with db as con:
        cursor = con.cursor()
        cursor.execute("""
        SHOW TABLES;
        """)
        result = cursor.fetchall()
        tables = [table_data[0] for table_data in result]

    for table in tables:
        backup(table)
