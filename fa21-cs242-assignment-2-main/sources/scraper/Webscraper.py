import requests
from Book import Book
from Author import Author

class Webscraper:
    '''
     The following class is meant initiate the database for the authors and books based on the author. It also
     validates the user input from the terminal.
    '''

    url_ = None # starting url
    totalAuthor_ = 0 # number of authors
    totalBooks_ = 0 # number of books
    bookDatabase_ = None # book object which represents the book database
    authorDatabase_ = None # book object which represents the author database

    def __init__(self, link, numAuthor, numBooks, outputFile):
        '''
        :param link: the starting link for webscraping
        :param numAuthor: the number of authors to be web scraped
        :param numBooks: the number of books to be web scraped
        :param outputFile: the output file to report all JSON files
        '''

        if self.isValidLink(link):
            self.url_ = link

            if self.isValidNum(numAuthor, numBooks):
                self.totalAuthor_ = numAuthor
                self.totalBooks_ = numBooks

                self.bookDatabase_ = Book(self.url_, self.totalBooks_, outputFile)
                self.authorDatabase_ = Author(self.url_, self.totalAuthor_, outputFile)


    def isValidLink(self, url):
        '''
            Checks if the input for the number of authors and books is a valid numbers
            :param url: the starting url to be scraped from
            :return: a boolean to tell whether or not the scraping was successful
        '''

        startingForm = "https://www.goodreads.com/book/show/"

        for i in range(len(startingForm)):
            if startingForm[i] != url[i]:
                raise ValueError("Sorry the link you have entered is not one that can get to a book")
                return False

        r = requests.get(url)
        if r.status_code == 404 or r.status_code >= 500:
            raise ValueError("Sorry the link that you have not entered is to a ")
            return False

        return True

    def isValidNum(self, numAuthor, numBooks):
        '''
        Checks if the input for the number of authors and books is a valid numbers
        :param numAuthor: the number of authors to be scraped
        :param numBooks: the number of books to be scraped
        :return:
        '''

        if (not isinstance(numBooks, int) or numBooks < 0) or (not isinstance(numAuthor, int) or numAuthor < 0):
            raise ValueError("Please enter a valid integer")
            return False


        if numAuthor > 50 or numBooks > 200:
            print("Warning: you are going to scrape from a large number of links")

        return True

    def getBookDatabase(self):
        '''
        Returns the book database object
        :return: the author database for web scraping
        '''
        return self.bookDatabase_


    def getAuthorDatabase(self):
        '''
        Returns the author database that can be manipulated
        :return: the author database for web scraping
        '''
        return self.authorDatabase_
