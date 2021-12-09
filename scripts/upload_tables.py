'''
UPLOAD_TABLES.PY: uploads the tables to the heroku database
'''

import psycopg2
import csv
import os.path

# -------------------- CONNECT TO THE DATABASE -------------------- #

DB_NAME = 'd5rhvjkii4gu67'
DB_USER = 'dvalsdjgojotpb'
DB_PASS = 'dd1096e917e04d51125d1f74ee9d64858db26fb73cb66ad4c437a430fe0f2a92'
DB_HOST = 'ec2-18-210-159-154.compute-1.amazonaws.com'
PRINT_EVERY = 100

# connect to the database:
try:
    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                (DB_NAME, DB_USER, DB_HOST, DB_PASS))
    cur = conn.cursor()
    print('successfully connected to heroku database.')
except:
    # log the error (will show up on log)
    print('unable to connect to the database.')

# -------------------- CONNECTED TO THE DATABASE -------------------- #

def best_type(x):
    if x.isdigit(): return int(x)
    if x.replace('.','',1).isdigit(): return float(x)
    return x

def upload_table(create_command, csv_path, table_name):
    # execute the commands:
    cur.execute(create_command, ())
    print('successfully created table %s' % table_name)

    # CSV file to parse:
    CSV_PATH = os.path.dirname(__file__) + csv_path

    rows = []
    commands = []
    with open(CSV_PATH) as f:
        r = csv.reader(f, delimiter=',')

        # store the row names:
        rows = next(r)

        PLACEHOLDER = ','.join(['%s'] * len(rows))

        # parse (and validate) entries in the file. use only valid entries:
        for i, entry in enumerate(r):
            # ignore invalid entries:
            if len(entry) != len(rows): continue

            # add literal quotation marks around every element of the entry (that is not numeric):
            args = [best_type(x) for x in entry]

            # hard-coding this because there's no real need to get too complicated:
            if table_name == 'BOOKS':
                args[4], args[5] = str(args[4]), str(args[5])

            args = tuple(args)

            # the final command:
            command_template = 'INSERT INTO ' + table_name + ' VALUES ({});'.format(PLACEHOLDER)
            cur.execute(command_template, args)

            # print every few insertions:
            if (i+1) % PRINT_EVERY == 0:
                print('successfully inserted %d rows to %s' % (i+1, table_name))
                conn.commit()

    print('successfully inserted all %d rows to %s' % (len(insert_commands), table_name))

    print('committing changes to database...')
    conn.commit()

    print('successfully set up table %s' % table_name)

if __name__ == '__main__':
    # upload the books table:
    books_table_name = 'BOOKS'
    books_csv = '/../data/books.csv'

    # (NOTE: isbn and isbn13 are VARCHAR beause INT type removes leading zeros)
    books_create_command = 'CREATE TABLE %s ('\
        'bookID INT PRIMARY KEY,'\
        'title VARCHAR,'\
        'authors VARCHAR,'\
        'average_rating DECIMAL,'\
        'isbn VARCHAR,'\
        'isbn13 VARCHAR,'\
        'language_code VARCHAR,'\
        'num_pages INTEGER,'\
        'ratings_count INTEGER,'\
        'text_reviews_count INTEGER,'\
        'publication_date DATE,'\
        'publisher VARCHAR'\
        ');' % (books_table_name)

    libraries_table_name = 'LIBRARIES'
    libraries_csv = '/../data/libraries.csv'

    libraries_create_command = 'CREATE TABLE %s ('\
        'LibID INT PRIMARY KEY,'\
        'Library VARCHAR,'\
        'Address VARCHAR,'\
        'Phone VARCHAR'\
        ');' % (libraries_table_name)

    users_table_name = 'USERS'
    users_csv = '/../data/users.csv'

    create_command = 'CREATE TABLE %s ('\
        'UserID INT PRIMARY KEY,'\
        'FIRST_NAME VARCHAR,'\
        'LAST_NAME VARCHAR,'\
        'EMAIL VARCHAR'\
        'PASSWORD VARCHAR'\
        ');' % (users_table_name)

    # upload the tables:
    upload_table(books_create_command, books_csv, books_table_name)
    upload_table(libraries_create_command, libraries_csv, libraries_table_name)
    upload_table(users_create_command, users_csv, users_table_name)

    # close the connection:
    cur.close()
    conn.close()
