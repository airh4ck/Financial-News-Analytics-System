import os

import psycopg2


def create_connection(dbFile):
    connection = None
    try:
        connection = psycopg2.connect(dbFile)
    except Exception as error:
        print(error)

    return connection


def create_row(connection, row, pair):
    cursor = connection.cursor()
    cursor.execute(
        f'''INSERT INTO {pair} ({', '.join(list(row.keys()))})
            VALUES ({', '.join(f'${i}' for i in range(len(list(row.values()))))})''',
        list(row.values())
    )

    connection.commit()


def update_row(row):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'database/database.db')
    connection = create_connection(filename)

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
            SET {', '.join(f"{key} = ${i}" for i, key in enumerate(row))}
            WHERE link = \'{row['link']}\'''',
        list(row.values())
    )

    connection.commit()
