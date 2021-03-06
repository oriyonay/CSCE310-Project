from flask import Flask, request, render_template
import os
import psycopg2
import requests

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
    return render_template('table.html', render_table=False, attributes=[], data=[])

@app.route('/search', methods=['POST'])
def search():
    update_cursors()
    name = request.form.get('name')

    search_result = search_book(name)
    found_any = search_result is not None

    if found_any:
        recommendations = get_recommendation(search_result[1])
    else:
        recommendations = None

    return render_template('book.html',
        book=search_result,
        found_any=found_any,
        recommendations=recommendations
    )

@app.route('/library')
def library():
    return render_template('library_search.html')

@app.route('/library_search', methods=['POST'])
def library_search():
    update_cursors()
    name = request.form.get('name')

    search_result = search_library(name)
    found_any = search_result is not None

    return render_template('library.html',
        library=search_result,
        found_any=found_any
    )

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    update_cursors()
    email = request.form.get('email')
    password = request.form.get('password')

    # NOTE: NEVER EVER EVER EVER EVER DO THIS!!! SO MANY THINGS WRONG WITH THIS
    # we don't care because we have 2 hours to do this lol
    query = "SELECT * FROM USERS WHERE EMAIL=%s AND PASSWORD=%s"
    cur.execute(query, (email, password,))
    user = cur.fetchone()
    found = user is not None

    return render_template('user_home.html',
        found=found,
        user=user
    )

def update_cursors():
    global conn
    global cur
    try:
        conn.close()
        cur.close()
    except:
        pass

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

# ------------------------------ UTILS ------------------------------ #
#return information in array
# https://towardsdatascience.com/starting-with-sql-in-python-948e529586f2

def search_book(book):
    query = "SELECT * FROM BOOKS WHERE title LIKE %(like)s ESCAPE '='"
    cur.execute(query, dict(like= '%'+book+'%'))

    result = cur.fetchone()

    return result

def search_library(library):
    query = "SELECT * FROM LIBRARIES WHERE Library LIKE %(like)s ESCAPE '='"
    cur.execute(query, dict(like= '%'+library+'%'))

    result = cur.fetchone()

    return result


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

# -------------------- RECOMMENDATION FUNCTIONS -------------------- #
def get_genre(ISBN):
  ##### GET GENRE #####

	url = 'https://www.goodreads.com/search?utf8=%E2%9C%93&query=' + ISBN

	book_page = requests.get(url)
	page_source = (book_page.text)

	idx = page_source.find('class="actionLinkLite bookPageGenreLink" href="/genres/') + 55

	genre = ''
	while page_source[idx] != '"':
		genre += page_source[idx]
		idx += 1

	return genre

def get_recommendation_isbn(ISBN):
	##### GET RECOMMENDATION ISBN #####

	url = 'https://www.goodreads.com/search?utf8=%E2%9C%93&query=' + ISBN

	book_page = requests.get(url)
	page_source = (book_page.text)

	rec_idx = page_source.find('Readers also enjoyed')
	url_idx = page_source.find('<a href="', rec_idx) + 9

	recommendation_url = ''
	while page_source[url_idx] != '"':
		recommendation_url += page_source[url_idx]
		url_idx += 1

	recommendation_page = requests.get(recommendation_url)
	recommendation_source = (recommendation_page.text)

	isbn_idx = recommendation_source.find("property='books:isbn'") - 15
	isbn = ''
	while recommendation_source[isbn_idx] != "'":
		isbn += recommendation_source[isbn_idx]
		isbn_idx += 1

	return isbn

def get_recommendation(book):
	book = search_book(book)

	#isbn from book into recommendation functions:
	#assuming search_book returns a 1-dimensional array (one book with each value in the array being bookID, title, authors, etc.)
	book_isbn = book[5]

	recommended_ISBN = get_recommendation_isbn(book_isbn)

	#sql statement LIKE or CONTAINS
	query = "SELECT * FROM BOOKS WHERE isbn13=%s;"
	cur.execute(query, (recommended_ISBN,))

	result = cur.fetchall()
	return result
