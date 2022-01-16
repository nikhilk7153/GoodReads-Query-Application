# fa21-cs242-assignment-2.2

The purpose of this assignment was to develop the front end component of the application allow the user to perform the 
CRUD operations. Specifically, using JavaScript, the database information stored in the backend would get called and will get showed to the user on a page.
To run this application, the user will first need to install Flask and use python version 3.9. In a terminal, they should type
do python3.9 run -m flask. From here, on a separate terminal should be used to run react to display the page by typing
npm start. This is run on local host 3000. The front page will simply display two tabs for the user to click on: the first one being a tab for seeing the information about books.
The second tab will be used to click for getting information about authors. Upon clicking on one of the tabs, the user 
will see a box for querying based on the syntax used in assignment 2.1. They will then click to get the information 
for all the relevant matches if there are any, along with a message indicating whether the object was found or not. 
There will also be a form such that if a user fills it out, they will be able to insert a new book or author. Under 
each book and author, there is an update and delete button. If one clicks on the update button, the author or books
information will fill up the page and they can click the submit button and refresh the page to see the updated information.
There is a deletion of books and authors and if one clicks on this, the authors and books will go away upon reloading 
the page. Should a user remove the author or book name or just type in None, an error message will come saying that the
update or insert could not be performed. 