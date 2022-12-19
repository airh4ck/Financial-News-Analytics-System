import os

import psycopg2
import numpy
from psycopg2.extensions import register_adapter, AsIs

def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

register_adapter(numpy.int64, adapt_numpy_int64)

def create_connection(pg_database):
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=pg_database,
            user=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"),
            host="host.docker.internal"
        )
    except Exception as error:
        print(error)

    return connection


def create_row(connection, row, pair):
    cursor = connection.cursor()
    cursor.execute(
        f'''INSERT INTO {pair} ({', '.join(list(row.keys()))})
            VALUES ({', '.join(f'%s' for i in range(len(list(row.values()))))})''',
        list(row.values())
    )

    connection.commit()


def update_row(row):
    connection = create_connection("pg_database")

    cursor = connection.cursor()

    pair = row.pop('pair')
    print(f"SELECT link from {pair} where link = '{row['link']}'")

    cursor.execute(
        f"SELECT link from {pair} where link = '{row['link']}'")
    if len(cursor.fetchall()) == 0:
        create_row(connection, row, pair)
        return

    cursor.execute(
        f'''UPDATE {pair}
            SET {', '.join(f"{key} = %s" for i, key in enumerate(row))}
            WHERE link = \'{row['link']}\'''',
        list(row.values())
    )

    connection.commit()
