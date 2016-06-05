from datetime import datetime


def create_table(db_connection, name, columns):
    cursor = db_connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(name, columns)
    cursor.execute(query)
    db_connection.commit()


def insert_into(db_connection, name, values):
    cursor = db_connection.cursor()
    marks = ','.join(['?'] * len(values))
    query = 'INSERT INTO {} VALUES ({})'.format(name, marks)
    cursor.execute(query, values)
    db_connection.commit()


def save_coil(db_connection, instrument, name, address):
    response = instrument.read_coil(int(address))
    values = (datetime.utcnow(), response)

    columns = 'date DATETIME, {} BOOL'.format(name)
    create_table(db_connection, name, columns)
    insert_into(db_connection, name, values)


def save_registers(db_connection, instrument, name, address, n):
    response = instrument.read_holding_registers(int(address), n)
    values = [datetime.utcnow()] + response

    columns = 'date DATETIME, ' + \
              ', '.join('{}_{} DOUBLE'.format(name, i) for i in range(n))
    create_table(db_connection, name, columns)
    insert_into(db_connection, name, values)


def print_db(db_connection, tree):
    cursor = db_connection.cursor()
    for section, tables in tree.items():
        print('============= %s ==============' % section)
        for name in tables.keys():
            print('--- %s ---' % name)
            for row in cursor.execute('SELECT * FROM %s ORDER BY date' % name):
                print(row)
    db_connection.commit()
