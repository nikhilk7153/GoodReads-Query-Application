from bs4 import BeautifulSoup
import requests
import json
from bson import json_util
from pymongo import MongoClient
import os

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# sets up the database for maintaining book information
mongo = client = MongoClient("mongodb+srv://nikhilk5:fluffy63@cluster0.pj5mb.mongodb.net/GoodReadsDatabase?retryWrites=true&w=majority")
db = mongo["GoodReadsDatabase"]
serverStatusResult = db.command("serverStatus")
collection = db.book

class Book:
    '''
    The following class performs the actions of web scraping book information and gets the book information and stores
    this information into a database. Specifically, this class web scrapes information about book's author, the author's
    Good Read's url, the book's image, the reviews and ratings for the books, and the names of books which are similar to the
    book. Lastly, this class maintains the database for storing book information. One can get a JSON file for all of the
    books information that are stored inside the database. Additionally, using a JSON file, one can update the the list of books
    in the database.
    '''

    url_ = None # the starting url link
    totalBooks_ = 0 # the total books that need to be scraped
    outputFile_ = None # the output file giving the

    def __init__(self, starterLink, bookCount, outputJSon):
        '''
        :param starterLink: the starting link for web scraping
        :param bookCount: the total number of books that should web scraped
        :param outputJSON: the name of the file for outputting the book information
        :param inputJSON: updates and inserts book information
        '''

        if outputJSon:
            self.file_output = outputJSon
        if starterLink is not None:

            self.url_ = starterLink
        if bookCount < 0:
            raise ValueError("Please enter a valid number of books")
        self.totalBooks_ = bookCount

    def scrapeBooks(self):

        dict_ = {"book_url": "", "title": "", "book_id": 0, "ISBN": 0,
                 "author_url": "", "author": "", "rating": 0,
                 "rating_count": 0, "review_count": 0, "image_url": None,
                 "similar_books": None}

        urlList = []
        urlList.append(self.url_)

        index = 0
        requests_session = requests.Session()
        while(1):

            if index == len(urlList):
                break

            url = urlList[index]
       
            urlHtml = requests_session.get(url, headers={"User-Agent":"Mozilla/5.0"})
            soup = BeautifulSoup(urlHtml.text, 'lxml')

            book_url = url
            title = self.getBookTitle(soup)
            book_id = self.getBookId(url)
            isbn = self.getISBN(soup)
            author_url = self.getAuthorURL(soup)
            author = self.getAuthor(soup)
            rating = self.getRating(soup)
            rating_count = self.getRatingCount(soup)
            review_count = self.getReviewCount(soup)
            image_url = self.getImageUrl(soup)
            similar_books = self.getSimilarBooks(soup, urlList)

            if title:

                collection.insert_one({"book_url": book_url, "title": title, "book_id": book_id, "ISBN": isbn,
                 "author_url": author_url, "author": author, "rating": rating,
                 "rating_count": rating_count, "review_count": review_count, "image_url": image_url,
                 "similar_books": similar_books})

            index += 1


    def getBookTitle(self, soup):
        '''
        Returns the title of a book from an HTML page
        :param soup: The object used for web scraping from an HTML page
        :return: The title of the book
        '''

        for element in soup("h1", {"id": "bookTitle"}):
            title = (element.text).strip()
            return title

    def getBookId(self, url):
        '''
        :param url: the url of the book from Good Reads
        :return: the ID of the book from the url
        '''
        bookId = ""
        url = url.replace("https://www.goodreads.com/book/show/", "")

        for i in range(len(url)):

            if url[i].isdigit():
                bookId += url[i]
            else:
                break

        int(bookId)
        return bookId

    def getISBN(self, soup):
        '''
        Returns the ISBN of a book from an HTML page
        :param soup: object used for web scraping
        :return: the ISBN of the book
        '''

        try:
            ISBN = ""
            index = 0

            for element in soup("div", {"class": "infoBoxRowItem"}):

                if index == 1:
                    fullISBN = element[index].text
                    break

                index += 1

            for i in range(len(fullISBN)):

                if fullISBN[i] == "\n" or fullISBN[i] == " ":
                    continue
                elif fullISBN[i] != "(":
                    ISBN += fullISBN[i]
                else:
                    return ISBN
        except:
            pass

    def getAuthorURL(self, soup):
        '''
        Returns the author URL from an HTML page
        :param soup: a web scraper object which will be used for getting information off an HTML page
        :return: returns the author url from the HTML page
        '''

        authorUrlList = []
        for link in soup("a", {"class": "authorName"}, href = True):

           authorUrlList.append(link['href'])

        if len(authorUrlList) == 0:
            pass

        return authorUrlList


    def getAuthor(self, soup):
        '''
        Returns the author(s) names
        :param soup: the web scraper object which will be used for getting information
        :return: the author name from the webpage
        '''

        nameList = []

        for element in soup("a", {"class": "authorName"}):

            nameList.append(element.text)

        if len(nameList) == 0:
            pass

        return nameList


    def getRating(self, soup):
        '''
        :param soup: the web scraper object for getting data from a HTML page
        :return: the average rating for a book
        '''

        try:
            element = soup.find("span", {"itemprop": "ratingValue"})
            if element is not None:
                return element.text
        except:
            pass


    def getRatingCount(self, soup):
        '''
        Function returns the total number of ratings
        :param soup: the web scraper object which will get the data from an HTML page
        :return: the total number of ratings
        '''

        try:
            element = soup.find("meta", {"itemprop": "ratingCount"})
            if element is not None:
                return element["context"]
        except:
           pass

    def getReviewCount(self, soup):
        '''
        :param soup: a web scraper object to get data from an HTML page
        :return: the total number of reviews
        '''

        try:
            element = soup.find("span", {"itemprop": "reviewCount"})
            return element["context"]
        except:
            pass

    def getImageUrl(self, soup):
        '''
        :param soup: is web scraping object that will be used for an HTML page
        :return: the image url of the book
        '''
        if len(soup("div", {"class": "bookCoverPrimary"}, src = True)):
            pass

        for link in soup("div", {"class": "bookCoverPrimary"}, src = True):
            return str(link.img['src'])


    def getSimilarBooks(self, soup, urlList):
        '''
        :param soup: a web scraper object to get data from an HTML page
        :param urlList: is a list of urls that will be scraped from
        :return: a list of all similar books to the book that will become scraped
        '''

        if len(soup("a", {"class": "actionLink right seeMoreLink"}, href = True)):
            pass

        for link in soup("a", {"class": "actionLink right seeMoreLink"}, href = True):

            similarBookLinkHTML = requests.get(link['href']).text
            soupy = BeautifulSoup(similarBookLinkHTML, features = "html.parser")
            elements = soupy.find_all(class_ = "responsiveBook__media")

            similarBookList = []
            urlSet = set(urlList)

            for element in elements:

                goodReadUrl = str("https://www.goodreads.com") + element.a['href']

                if goodReadUrl not in urlSet and len(urlList) <= 2000 and len(urlList) <= self.totalBooks_:
                    urlList.append(goodReadUrl)

                similarBookList.append(element.img['alt'])

            return similarBookList

    def returnJSONFile(self):
        '''
        :return: a JSON file of all the books and their information stored inside the database
        '''

        outputName = "Book Collection " + str(self.outputFile_)

        count = 0

        with open(outputName, 'w') as outFile:

            for document in collection.find():
                json.dump(json.loads(json_util.dumps(document)), outFile, indent = 4, separators=(", ", ": "))

                if count == 10:
                    break

                count += 1


