import requests

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

def get_recommendation(book)

	book = search_book(book)

	#isbn from book into recommendation functions:
	#assuming search_book returns a 1-dimensional array (one book with each value in the array being bookID, title, authors, etc.)
	book_isbn = book[5]

	recommended_ISBN = get_recommendation_isbn(book_isbn):

	mycursor = DBconnection()

	#sql statement LIKE or CONTAINS
	query = "SELECT * FROM BOOKS WHERE isbn13=" + recommended_ISBN + ";"
	mycursor.execute(query)

	result = mycursor.fetchall()
	return result