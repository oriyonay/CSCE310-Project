'''
generate_insert_commands.py: given a CSV, generate SQL 'INSERT INTO' commands to
load it into a database table.
'''

import os.path

# CSV file to parse:
CSV_PATH = os.path.dirname(__file__) + '/../data/books.csv'

# ---------- UNUSED CONSTANTS ---------- #
# (they're here to make it easier to run the isnert commands from 
# this script directly)

# actually execute these commands on a database if this is true:
EXECUTE = False

# database info, if executing on a real database:
DB_NAME = 'dbname'
DB_USER = 'username'
DB_PASS = 'password'
DB_HOST = 'localhost'

import csv

def generate_insert_commands(table_name):
    '''
    if EXECUTE:
        import psycopg2

        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                                    (DB_NAME, DB_USER, DB_HOST, DB_PASS))
            cur = conn.cursor()
        except:
            print('unable to connect to the database.')
    '''

    rows = []
    commands = []
    with open(CSV_PATH) as f:
        r = csv.reader(f, delimiter=',')

        # store the row names:
        rows = next(r)

        # parse (and validate) entries in the file. use only valid entries:
        for entry in r:
            # ignore invalid entries:
            if len(entry) != len(rows): continue

            # add literal quotation marks around every element of the entry (that is not numeric):
            entry_with_quotation_marks = ['"{}"'.format(x) if not x.replace('.','',1).isdigit() else x for x in entry]

            # output (or execute) the final command:
            command = 'INSERT INTO %s VALUES (%s);' % (table_name, ', '.join(entry_with_quotation_marks))

            if EXECUTE:
                cur.execute(command)
            else:
                commands.append(command)

    return commands