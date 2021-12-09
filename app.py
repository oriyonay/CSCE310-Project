from flask import Flask, request, render_template
import os
import psycopg2

# ---------- DATABASE CONSTANTS ---------- #

# connect to the database with *the same* connection:
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

'''
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
'''

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

    search_results = search_book(name)
    found_any = (len(search_results) != 0)

    recommendations = ['a', 'b', 'c']

    # print(search_results)

    return render_template('book.html',
        name=name,
        found_any=found_any,
        recommendations=recommendations
    )

# ------------------------------ UTILS ------------------------------ #
#return information in array
# https://towardsdatascience.com/starting-with-sql-in-python-948e529586f2

def search_book(book):
    #cur = DBconnection()
    #sql statement LIKE or CONTAINS
    query = "SELECT * FROM BOOKS WHERE title LIKE %(like)s ESCAPE '='"
    cur.execute(query, dict(like= '%'+book+'%'))

    results = cur.fetchone()

    for x in results:
        print(x)

    return results


# ---------- author search query ---------- #
def search_author(author_name):
    #mycursor = DBconnection()

    query = "SELECT title, author, isbn, average_rating FROM BOOKS WHERE author SIMILAR TO \'" + author_name + "%\';"

    cur.execute(query)

    results = cur.fetchall()

    for x in results:
        print(x)


# ---------- insert book query ---------- #
def insert_book(title,authors,isbn,language_code):
    #mycursor = DBconnection()

    query = "INSERT INTO BOOKS(title, authors, isbn, language_code) VALUES ( '" + title + "', '" + authors  + "', '" + isbn  + "', '" + language_code  + "');"

    cur.execute(query)
    #mydb.commit()


# ---------- get all books in table ---------- #
def get_all_books():
    #mycursor = DBconnection()

    query = "SELECT title, author, isbn, average_rating FROM BOOKS;"

    cur.execute(query)

    results = cur.fetchall()

    for x in results:
        print(x)

    return results



# ---------- get rating of a book ---------- #
def get_rating_book(book):
    #mycursor = DBconnection()

    query = "SELECT title, average_rating FROM BOOKS WHERE title SIMILAR TO \'" + book + "%\';"

    cur.execute(query)

    results = cur.fetchall()

    for x in results:
        print(x)

    return results

# ---------- get book by isbn ---------- #
def get_book_isbn(isbn):
    #mycursor = DBconnection()

    query = "SELECT title, author, isbn, average_rating FROM BOOKS WHERE isbn = " + isbn +  ";"

    cur.execute(query)

    results = cur.fetchall()

    for x in results:
        print(x)

    return results


# ---------- find books in library  ---------- #
def get_library_book(library):
    #assume library name is spelled correctly
    libID = "SELECT ID FROM Libraries WHERE name = " + library + ";"
    query = "SELECT title, author, isbn, average_rating FROM BOOKS INNER JOIN INCLUDES ON " + libID + " = books.ID ;"

    cur.execute(query)

    results = cur.fetchall()

    for x in results:
        print(x)

    return results
