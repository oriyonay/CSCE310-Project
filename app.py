from flask import Flask, request, render_template
import psycopg2

# ---------- DATABASE CONSTANTS ---------- #

TABLE_NAME = 'books'

# connect to the database with *the same* connection:
'''
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
'''

# ---------- END OF DATABASE CONSTANTS ---------- #

app = Flask(__name__)

@app.route('/')
def hello():
    # probably display the home page here

    # to be run only once to set the table up:
    # setup(table_name=TABLE_NAME)

    # for now, just return the dummy page:
    return get_data()

@app.route('/search', methods=['POST'])
def search():
    name = request.form.get('name')

    return render_template('book.html', name=name)

@app.route('/<some_param>')
def get_data():
    # example of getting data from the database:
    # (replace attributes with attribute names and fetch data from actual database)
    # (also note that we can use <some_param>, which is passed into this function from the url.
    # we'll probably use this to tailor the query)
    attributes = ['a1', 'a2']
    data = [['c1', 'c2'], ['c3', 'c4']]
    return render_template('table.html', render_table=False, attributes=attributes, data=data)

# setup: function to set the database up
def setup(table_name):
    # the CREATE TABLE command:
    # (NOTE: isbn and isbn13 are VARCHAR beause INT type removes leading zeros
    create_command = 'CREATE TABLE %s ('\
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
        ');' % (table_name)

    # generate the insert commands:
    from scripts import generate_insert_commands as gic
    insert_commands = gic.generate_insert_commands(table_name=table_name)

    # execute the commands:
    cur.execute(create_command)
    print('successfully created table %s' % table_name)

    for insert_command in insert_commands:
        cur.execute(insert_command)
    print('successfully inserted all %d rows to %s' % (len(insert_commands), table_name))

    print('successfully set up table %s' % table_name)
    return True
