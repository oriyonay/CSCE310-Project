from flask import Flask, request, render_template
import psycopg2

# ---------- DATABASE CONSTANTS ---------- #

TABLE_NAME = 'books'

# connect to the database with *the same* connection:
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

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

'''
@app.route('/<some_param>')
def get_data():
    # example of getting data from the database:
    # (replace attributes with attribute names and fetch data from actual database)
    # (also note that we can use <some_param>, which is passed into this function from the url.
    # we'll probably use this to tailor the query)
    attributes = ['a1', 'a2']
    data = [['c1', 'c2'], ['c3', 'c4']]
    return render_template('table.html', render_table=False, attributes=attributes, data=data)
'''
