import pytest
import requests

'''
Tests QueryParser.py class and makes sures that all operators of this class are properly implemented
'''

def test_NOTOperator():
    '''
    Tests the NOT operator's functionality to ensure that the field with a specific value is not included in the query
    '''

    r = requests.get("http://localhost:5000/search?q=book.book_id: NOT 34927404")
    assert r.status_code == 200
    for json in r.json():
        if 'book_id' in r.json() and json["book_id"] == 34927404:
            assert False
    assert True

def test_GreaterThanOperator():
    '''
    Tests the greater than operator to ensure that items greater than a specific value will get included
    '''

    r = requests.get("http://localhost:5000/search?q=book.rating: > 4.9")
    assert r.status_code == 200
    for json in r.json():
       if json["rating"] < 4.9:
           assert False
    assert True

def test_LessThanOperator():
    '''
    Tests the greater than operator to ensure that items less than a specific value will get included
    '''

    r = requests.get("http://localhost:5000/search?q=book.rating: < 2.5")
    assert r.status_code == 200
    for json in r.json():
       if json["rating"] >= 2.5:
        assert False
    assert True

def test_quotesOperator():
    '''
    Tests to ensure that the quotes operator will look for exact values for strings and not regexes
    '''

    r = requests.get("http://localhost:5000/search?q=author.name: " + "\"Martin Kleppmann\"" )
    assert r.status_code == 200
    for json in r.json():
       if json["name"] != "Martin Kleppmann":
        assert False
    assert True

    r = requests.get("http://localhost:5000/search?q=author.review_count: " + "\"4942\"" )
    for json in r.json():
        if json["review_count"] != 4942:
            assert False
    assert True

def test_noOperator():
    '''
    Tests to ensure that regexes of string values are passed and that for ints the exact values are passed
    '''

    r = requests.get("http://localhost:5000/search?q=book.title: Java")
    assert r.status_code == 200
    for json in r.json():
       if "Java" not in json["title"]:
        assert False
    assert True

    r = requests.get("http://localhost:5000/search?q=author.rating_count: 795")
    assert(len(r.json()) == 1)
    for json in r.json():
        if json["rating_count"] != 795:
            assert False
    assert True

def test_orOperator():
    '''
    Tests to ensure that the or operator works for queries
    '''

    r = requests.get("http://localhost:5000/search?q=book.rating: > 3 OR book.review_count: < 519")
    assert r.status_code == 200
    for json in r.json():
       if (json["rating"] <= 3 and json["review_count"] >= 519):
        assert False
    assert True

def test_andOperator():
    '''
    Tests to ensure that the and operator works for queries
    '''

    r = requests.get("http://localhost:5000/search?q=book.rating: > 3 AND book.review_count: < 519")
    assert r.status_code == 200
    for json in r.json():
       if (json["rating"] <= 3 or json["review_count"] >= 519):
        assert False
    assert True

def test_detectQueryLanguageErrors():
    '''
    Tests to ensure that operators can only be invoked where they should be invoked, and that values and fields
    are kept where they should be in an appropriate manner
    '''

    r = requests.get("http://localhost:5000/search?q=book.title: > 'Java'")
    assert r.status_code == 400

    r = requests.get("http://localhost:5000/search?q=book.review_count: 3.4")
    assert r.status_code == 400

    r = requests.get("http://localhost:5000/search?q=author.review_count: AND 4.3 AND author.rating > 2.1")
    assert r.status_code == 400

if __name__ == '__main__':
    pytest.main()


