from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def hello():
    return 'welcome to booksmart!'
