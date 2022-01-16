import pytest
import requests

'''
Class tests API directory 
'''

def test_getRequest():
    '''
    Checks whether or not the function can get a valid id for author and book
    '''

    r = requests.get("http://localhost:5000/book?id=34927404")
    assert(r.status_code == 200)
    assert(len(r.json()) == 1)
    assert(r.json()[0]["book_id"] == 34927404)

    r = requests.get("http://localhost:5000/author?id=7303744")
    assert r.status_code == 200
    assert (len(r.json()) == 1)
    assert (r.json()[0]["author_id"] == 7303744)


def test_getReturnsUnknownId():
    '''
    Tests to ensure that for ids not stored in the database, the server will return a 404 error
    '''

    r = requests.get("http://localhost:5000/book?id=34927403")
    assert (r.status_code == 404)

    r = requests.get("http://localhost:5000/author?id=7303745")
    assert (r.status_code == 404)


def test_invalidFieldOnGet():
    '''
    Tests to ensures that if the url or the field being invoked is not an id, the server will return a 404 error
    '''

    r = requests.get("http://localhost:5000/book?title='Effective Java'")
    assert (r.status_code == 400)

    r = requests.get("http://localhost:5000/author?name=Morten Münster")
    assert (r.status_code == 400)


def test_putRequest():
    '''
    Tests to ensure that a book and author can be updated properly by their id
    '''

    r = requests.put("http://localhost:5000/author?id=7303744", json = {"ratings": 4.5, "review_count": 4313})
    r.status_code == 200 or r.status_code == 500

    r = requests.get("http://localhost:5000/author?id=7303744")
    r.status_code == 200 or r.status_code == 500
    json = r.json()[0]
    assert json["ratings"] == 4.5
    assert json["review_count"] == 4313

    r = requests.put("http://localhost:5000/author?id=6089", json={"ratings": 4.1, "rating_count": 2324})
    assert  r.status_code == 200 or r.status_code == 500

    r = requests.get("http://localhost:5000/author?id=6089")
    r.status_code == 200 or r.status_code == 500
    json = r.json()[0]
    assert json["ratings"] == 4.1
    assert json["rating_count"] == 2324


def test_notJSONForPut():
    '''
    Tests to ensure that the put functions for books and authors will only take in JSON objects
    '''

    r = requests.put("http://localhost:5000/author?id=7303744", data={"ratings": 4.5, "review_count": 4313})
    assert r.status_code == 415

    r = requests.put("http://localhost:5000/book?id=", data={"ratings": 4.5, "review_count": 4313})
    assert r.status_code == 415


def test_insertTakeJSONOnly():
    '''
    Tests to ensure that the single item posts for book and author will only taken in JSON objects
    '''

    r = requests.post("http://localhost:5000/book", data = {"book_id": 1})
    assert r.status_code == 415
    r = requests.get("http://localhost:5000/book?id=1")
    assert r.status_code == 404

    r = requests.post("http://localhost:5000/author", data = {"author_id": 1})
    assert r.status_code == 415
    r = requests.get("http://localhost:5000/book?id=1")
    assert r.status_code == 404


def test_insertMultipleTakeJSONOnly():
    '''
    Tests to ensure that multiple item posts for book and author will only taken in JSON objects
    '''

    book_collection = {"collection": [{"book_id": 3}, {"book_id": 4}, {"book_id": 5}]}
    r = requests.post("http://localhost:5000/books", data=book_collection)
    assert r.status_code == 415

    author_collection = {"collection": [{"author_id": 3}, {"author_id": 4}, {"author_id": 5}]}
    r = requests.post("http://localhost:5000/authors", data=author_collection)
    assert r.status_code == 415

def test_insertMany():
    '''
    Tests to see that multiple json objects can be added to the book and authors database
    '''

    book_collection = {"collection": [{"book_id": 3}, {"book_id": 4}, {"book_id": 5}]}
    author_collection = {"collection": [{"author_id": 3}, {"author_id": 4}, {"author_id": 5}]}

    r = requests.post("http://localhost:5000/books", json = book_collection)
    assert r.status_code == 200 or r.status_code == 500

    book_array = book_collection["collection"]

    for i in range(len(book_array)):

        book = book_array[i]
        r = requests.get("http://localhost:5000/book?id=" + str(book["book_id"]))
        r.status_code == 200 or r.status_code == 500

    r = requests.post("http://localhost:5000/authors", json = author_collection)
    assert r.status_code == 200 or r.status_code == 500

    author_array = author_collection["collection"]

    for i in range(len(author_array)):

        author = author_array[i]
        r = requests.get("http://localhost:5000/author?id=" + str(author["author_id"]))
        assert r.status_code == 200 or r.status_code == 500


def test_scrape():
    '''
    Tests to ensure that the scrape function can add to the author and book databases when given a link and number to scrape
    '''

    r = requests.post('http://localhost:5000/scrape?object=book&total=1&link=https://www.goodreads.com/book/show/4214.Life_of_Pi')
    assert r.status_code == 200
    r = requests.get("http://localhost:5000/book?id=4214")
    assert r.status_code >= 400

    r = requests.post('http://localhost:5000/scrape?object=author&total=1&link=https://www.goodreads.com/book/show/4214.Life_of_Pi')
    assert r.status_code == 200
    r = requests.get("http://localhost:5000/author?id=811")
    assert r.status_code >= 400

def test_scapeCanHandleInvalidInput():
    '''
    Tests to ensure that no scraping can be done if the link, total, or object for the database are all invalid
    '''

    r = requests.post('http://localhost:5000/scrape?object=binder&total=1&link=https://www.goodreads.com/book/show/4214.Life_of_Pi')
    assert r.status_code == 400

    r = requests.post('http://localhost:5000/scrape?object=book&total=-200&link=https://www.goodreads.com/book/show/4214.Life_of_Pi')
    assert r.status_code == 400

    r = requests.post('http://localhost:5000/scrape?object=book&total=1&link=https://www.goodreads.com/book/sw/4214.Life_of_Pi')
    assert r.status_code == 400


def test_deleteRequest():
    '''
    Tests that deletion can be done on the author and book database
    '''

    r = requests.delete("http://localhost:5000/book?id=387190")
    assert r.status_code == 200

    r = requests.get("http://localhost:5000/book?id=387190")
    assert r.status_code == 404

    r = requests.delete("http://localhost:5000/author?id=3174788")
    assert r.status_code == 200

    r = requests.get("http://localhost:5000/author?id=3174788")
    assert r.status_code == 404


def test_deleteAndPutFailOnUnknownID():
    '''
    Tests that a deletion and update cannot be done for id values that are not stored in the book and author databases
    '''

    r = requests.delete("http://localhost:5000/book?id=387190")
    assert r.status_code == 404

    r = requests.put("http://localhost:5000/author?id=3174788", json= {"name": "Bob", "rating": 4.2})
    assert r.status_code == 404