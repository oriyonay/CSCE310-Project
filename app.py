from flask import Flask, request, render_template
import psycopg2

# ---------- DATABASE CONSTANTS ---------- #

# connect to the database with *the same* connection:
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# ---------- END OF DATABASE CONSTANTS ---------- #

app = Flask(__name__)

@app.route('/')
def hello():
    attributes = ['a1', 'a2']
    data = [['c1', 'c2'], ['c3', 'c4']]
    return render_template('table.html', render_table=False, attributes=attributes, data=data)

@app.route('/search', methods=['POST'])
def search():
    name = request.form.get('name')

    return render_template('book.html', name=name)
