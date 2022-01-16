import json
import requests
from bs4 import BeautifulSoup
import time
import re
from bson import json_util
from pymongo import MongoClient
import os

# sets up the information for MongoDB server that will hold author information
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# sets up the database for maintaining book information
mongo = client = MongoClient("mongodb+srv://nikhilk5:fluffy63@cluster0.pj5mb.mongodb.net/GoodReadsDatabase?retryWrites=true&w=majority")
db = mongo["GoodReadsDatabase"]
serverStatusResult = db.command("serverStatus")
collection = db.author

class Author:
    '''
    The purpose of this class is to web scrape and store the information for that Author database
    Specifically, the class will maintain information about the author's name, their url link, their average rating,
    the number of ratings and reviews that they have received, the list of books that they have written, and the authors
    who are similar to then. This class also supports returning a JSON of all the author information into a JSON file.
    Additionally, this class allows the user to update the database for any author of their and also insert new authors.
    '''

    url_ = None # starting author link
    totalAuthors_ = 0 # number of authors needed to be added to the database
    outputFile_ = None # the JSON file for outputing all of the author information into the database

    def __init__(self, starterLink, authorCount, outputFile):
        '''
        :param starterLink: the link for starting the web scraping
        :param authorCount: the number of authors to scrape
        :param outputFile: the name of the output file that will be used for outputing all of the authors' information
        '''

        if outputFile:
            self.outputFile_ = outputFile

        if starterLink is not None:
            requests_session = requests.Session()
            urlHtml = requests_session.get(starterLink, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(urlHtml.text, 'lxml')
            self.url_ = self.getAuthorUrlFromBook(soup)

        self.totalAuthors_ = authorCount

    def scrapeAuthors(self):
        '''
        Iteratively keeps on web scraping until there is no more things to web scrape
        '''

        urlList = []
        urlList.append(self.url_)
        requests_session = requests.Session()
        index = 0
        authorList = []

        while (1):

            if index >= len(urlList):
                break

            url = urlList[index]

            urlHtml = requests_session.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(urlHtml.text, 'lxml')

            name = self.getName(soup)
            authorList.append(name)

            authorID = self.getAuthorID(url)
            authorUrl = url
            rating = self.getRating(soup)
            rating_count = self.getRatingCount(soup)
            review_count = self.getReviewCount(soup)
            image_url = self.getImageUrl(soup, name)
            related_authors = self.getRelatedAuthors(soup, urlList, authorList)
            author_books = self.getAuthorBooks(soup)

            if name:
                collection.insert_one({"name": name, "author_url": authorUrl, "author_id": authorID, "rating": rating,
                 "rating_count": rating_count, "review_count": review_count, "image_url": image_url,
                 "related_authors": related_authors, "author_books": author_books})

            index += 1

    def getAuthorUrlFromBook(self, soup):
        '''
        Returns the author url from the initial starting book link
        :param soup: the object that will be used for web scraping
        :return: The author who was written the book based off the book url
        '''

        try:
            link = soup.find("a", {"class": "authorName"}, href=True)
            return link['href']
        except:
            pass


    def getName(self, soup):
        '''
        Returns the name of the author from the HTML page
        :param soup: the object that will be used for web scraping
        :return: the name of the author
        '''

        try:
            for element in soup("a", {"class": "authorName"}):
                return element.text
        except:
            pass

    def getAuthorID(self, url):
        '''
        :param url: The url of the author
        :return:
        '''

        time.sleep(1)
        authorId = ""
        url = url.replace("https://www.goodreads.com/author/show/", "")

        for i in range(len(url)):

            if url[i].isdigit():
                authorId += url[i]
            else:
                break

        int(authorId)
        return authorId

    def getRating(self, soup):
        '''
        Returns the average rating for the authors
        :param soup: is the object that will do the web scraping
        :return: the name of the rating
        '''

        try:
            element = soup.find("span", {"itemprop": "ratingValue"})
            if element is not None:
                return element.text
        except:
            pass


    def getRatingCount(self, soup):
        '''
        Returns the number of the ratings
        :param soup: the web scraping object
        :return: the number of people who have rated the author
        '''

        try:
            element = soup.find("meta", {"itemprop": "ratingCount"})
            if element is not None:
                return element["context"]
        except:
            pass

    def getReviewCount(self, soup):
        '''
        Returns the number of reviews
        :param soup: the object for web scraping
        :return: the count of reviews that are given
        '''

        try:
            element = soup.find("span", {"itemprop": "reviewCount"})
            return int(element["title"])
        except:
            pass


    def getImageUrl(self, soup, name):
        '''
        :param soup: the object that will be used for web-scraping
        :param name: the name of the author
        :return: the image url
        '''

        try:
            element = soup.find("img", {"alt": name})
            return str(element['src'])
        except:
            pass


    def getRelatedAuthors(self, soup, urlList, authorList):
        '''
        :param soup: the object that will be used for parsing
        :param urlList: the list of urls that have been
        :param authorList: the list of authors that are the authors which will get added to for future web scraping
        :return: the list of authors that are related to the author in question
        '''

        relatedAuthorlink = soup.find(href=re.compile("/author/similar/"))
        link = "https://www.goodreads.com" + relatedAuthorlink['href']
        similarAuthorLinkHTML = requests.get(link).text
        soupy = BeautifulSoup(similarAuthorLinkHTML, features="html.parser")
        elements = soupy.find_all(class_ = "gr-h3 gr-h3--serif gr-h3--noMargin")

        relatedAuthorsList = []
        for element in elements:

            link = element['href']

            urlSet = set(urlList)
            authorSet = set(authorList)

            authorName = element.text

            if authorName not in authorSet and link not in urlSet and len(urlList) <= 2000 \
                    and len(urlList) <= self.totalAuthors_:

                urlList.append(link)

            relatedAuthorsList.append(element.text)

        return relatedAuthorsList


    def getAuthorBooks(self, soup):
        '''
        :param soup: the object that will be used for web scraping
        :return: the object of all the author books
        '''

        authorBookslink = soup.find(href=re.compile("/author/list/"))

        link = "https://www.goodreads.com" + authorBookslink['href']
        authorBookslinkHTML = requests.get(link).text

        soupy = BeautifulSoup(authorBookslinkHTML, features = "html.parser")
        elements = soupy.find_all(class_ = "u-anchorTarget")
        authorBooksList = []

        for element in elements:
            authorBooksList.append(element.title)

        return authorBooksList

    def returnJSONFile(self):
        '''
        Function iterates through entire database and returns a JSON file of all the authors
        :return: the output file for the list of all authors as a JSON file
        '''

        with open(self.outputFile_, 'w') as outFile:
            for document in collection.find():
                json.dump(json.loads(json_util.dumps(document)), outFile)

