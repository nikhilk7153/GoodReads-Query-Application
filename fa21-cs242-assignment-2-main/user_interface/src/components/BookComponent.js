import '../App.css';
import axios from 'axios';
import React from 'react';

/**
* The following class maintains all of the information about Book Components for the front end with a list of
* all books and a front end component. Code was referred to from https://www.youtube.com/watch?v=57PpSudAzJM and
* https://www.youtube.com/watch?v=msEmUtYqVV0
*/

class BookComponent extends React.Component {

   /*
   * Constructs an BookComponent object which creates the default values for the form and the list of books to print
   */
   constructor(props) {
      super(props);
      this.state =
      {
         books: [],
         book_id: 0,
         ISBN: 0,
         book_url: '',
         title: '',
         author_url: [],
         author: [],
         rating: 0,
         rating_count: 0,
         review_count: 0,
         image_url: '',
         similar_books: [],
         server_result: '',
         query_server_result: '',
         query:''
      }
   }

   /**
   * Renders the page to print all of the books from the database and defaults all the values in the form to
   * empty string, None, or 0.
   */
   componentDidMount() {
      fetch('http://localhost:5000/book/list_all')
      .then((resp) => resp.json())
      .then((data) => {
        this.setState({
         books: data,
         book_id: 0,
         ISBN: 0,
         book_url: 'None',
         title: 'None',
         author_url: 'None',
         author: 'None',
         rating: 0,
         rating_count: 0,
         review_count: 0,
         image_url: 'None',
         similar_books: 'None',
         server_result: '',
         query_server_result: '',
         query:''
        })
      })
    .catch(error => {
      console.log("Error from server")
      console.log(error)}
     );
   }

   /**
   * The following code will set the title for the book object to what is typed in the form
   */
   titlechange = event => {
        this.setState({
            title: event.target.value
        })
   }

   /**
   * The following code will set the ISBN for the book object to what is typed in the form
   */
   ISBNchange = event => {
        this.setState({
            ISBN: event.target.value
        })
   }

   /**
   * The following code will set the bookID for the book object to what is typed in the form
   */
   bookIDChange = event => {
        this.setState({
           book_id: event.target.value
        })
   }

   /**
   * The following code will set the book for the book object to what is typed in the form
   */
   bookUrlChange = event => {
        this.setState({
           book_url: event.target.value
        })
   }

   /**
   * The following code will set the author url for the book object to what is typed in the form
   */
   authorUrlChange = event => {
        this.setState({
           author_url: event.target.value
        })
   }

   /**
   * The following code will set the image url for the book object to what is typed in the form
   */
   imageUrlChange = event => {
        this.setState({
           image_url: event.target.value
        })
   }

   /**
   * The following code will set the author name for the book object to what is typed in the form
   */
   authorChange = event => {
        this.setState({
           author: event.target.value
        })
   }

   /**
   * The following code will set the rating value for the book object to what is typed in the form
   */
   ratingChange = event => {
        this.setState({
           rating: event.target.value
        })
   }

   /**
   * The following code will set the rating count value for the book object to what is typed in the form
   */
   ratingCountChange = event => {
        this.setState({
           rating_count: event.target.value
        })
   }

   /**
   * The following code will set the review count value for the book object to what is typed in the form
   */
   reviewCountChange = event => {
        this.setState({
           review_count: event.target.value
        })
   }

   /*
   * The following code will set the similar books value for the book object to what is typed in the form
   */
   similarBooksChange = event => {
        this.setState({
           similar_books: event.target.value
        })
   }

  /**
  * Upon completing a form and a user clicks the submit button, this function will reset the form. If an update
  * button was clicked for one of the forms, then a PUT request will be made, else an insert with a POST will be
  * made with an ID.
  */
   submit(event, id) {

    if ((this.state.title === '' || this.state.title === 'None')) {

           this.setState({
             book_id: 0,
             ISBN: 0,
             book_url: 'None',
             title: 'None',
             author_url: 'None',
             author: 'None',
             rating: 0,
             rating_count: 0,
             review_count: 0,
             image_url: 'None',
             similar_books: 'None',
             server_result: 'Please reload the page and enter a title'
          }
        )
        return
    }

    if (id === 0) {

        event.preventDefault()
        axios.post('http://localhost:5000/book', {'ISBN': this.state.ISBN, 'title': this.state.title, 'book_id': 2125323,
        'author': this.state.author, 'author_url': this.state.author_url,
        'book_url': this.state.book_url, 'image_url': this.state.image_url, 'rating': this.state.rating,
        'rating_count': this.state.rating_count, 'review_count': this.state.review_count, 'similar_books':
        this.state.similar_books})
        .then((result) => {
            if (result.status === 200) {
                 this.setState({
                     book_id: 0,
                     ISBN: 0,
                     book_url: 'None',
                     title: 'None',
                     author_url: 'None',
                     author: 'None',
                     rating: 0,
                     rating_count: 0,
                     review_count: 0,
                     image_url: 'None',
                     similar_books: 'None',
                     server_result: 'Insertion Successful, please reload the page'
                 })
            }
        })

    } else {
        axios.put(`http://localhost:5000/book?id=${id}`,
        {'ISBN': this.state.ISBN, 'title': this.state.title, 'book_id':
        id, 'author': this.state.author, 'author_url': this.state.author_url,
        'book_url': this.state.book_url, 'image_url': this.state.image_url, 'rating': this.state.rating,
        'rating_count': this.state.rating_count, 'review_count': this.state.review_count, 'similar_books':
         this.state.similar_books})
        .then((result) => {
                this.setState({
                     server_result: 'Update Successful, please reload the page'
                })
        })
      }
   }

   /**
   * Deletes a book based on the ID passed in and makes a request to the backend
   */
   deleteBook(book_id) {
        axios.delete(`http://localhost:5000/book?id=${book_id}`)
        .then(() => {
           this.setState({server_result: 'Deletion successful, please reload the page'})
        })
   }

   /**
   * Updates a book based on the book parameter by populating the fields with the values that were given to them
   */
   updateBook(book) {

       this.state.ISBN = book.ISBN
       this.state.title = book.title
       this.state.author_url = book.author_url
       this.state.author = book.author
       this.state.rating = book.rating
       this.state.rating_count = book.rating_count
       this.state.review_count = book.review_count
       this.state.image_url = book.image_url
       this.state.similar_books = book.similar_books
       this.state.book_id = book.book_id

       document.getElementById('ISBN').value = book.ISBN
       document.getElementById('title').value = book.title
       document.getElementById('book_url').value = book.book_url
       document.getElementById('author_url').value = book.author_url
       document.getElementById('rating').value = book.rating
       document.getElementById('rating_count').value = book.rating_count
       document.getElementById('review_count').value = book.review_count
       document.getElementById('image_url').value = book.image_url
       document.getElementById('similar_books').value = book.similar_books
       document.getElementById('book_id').value = book.book_id

   }

  /**
  * Sets the query to what the user set it to
  */
   queryChange = event => {
        this.setState({
            query: event.target.value
        })
   }

   /**
   * Makes a request upon getting the query and displays the result with a status message
   */
   submitQuery(e, query) {

     this.query_server_result = ''
     axios.get(`http://localhost:5000/search?q=${query}`)
     .then((resp) => {

         if (resp.status === 200) {
                this.state.books = resp.data

                if (this.state.books.length > 0) {
                    this.setState({
                        books: resp.data,
                        query_server_result: 'Query Successful'
                    })
                } else {
                    this.setState({
                        books: resp.data,
                        query_server_result: 'No matching results for your query'
                    })
                }
                this.render();
         }
     }).catch(error => {
         this.setState({
             query_server_result: 'Incorrect query syntax',
             books: []
         })
        this.render();
     })
   }

   /**
   * Uses the HTML to display the page on the site
   */
   render() {
     return (
     <div className = "row mt-5">
        <div className = "form mt-5">

                <h2> Query </h2>
                <br></br>
                <h3> Please Enter a query for a book </h3>
                <br></br>

                <div className = "form-group">
                    <input type = "text" onChange={(e)=>{this.queryChange(e)}} className = "form-control"
                      autocomplete = "off" placeholder = "Query" id = "book_field"/>
                </div>
                <br></br>
                <h3> Server Result: {this.state.query_server_result} </h3>

                <br></br>
                <br></br>

                <button onClick={(e)=>{this.submitQuery(e, this.state.query)}}
                className = "btn btn-block btn-primary"> Submit </button>

                <br></br>
                <br></br>
                <br></br>
                <br></br>

                <h2> Enter Book Information </h2>
                <br></br>

                <div className = "form-group">
                    <label> Title:
                    <input type = "text" onChange={(e)=>{this.titlechange(e)}} className = "form-control" id = "title"
                     autocomplete = "off" value = {this.state.title}/>
                     </label>
                </div>
                <br></br>
                 <div className = "form-group">
                   <label> ISBN:
                    <input type = "number" onChange={(e)=>{this.ISBNchange(e)}} className = "form-control" id = "ISBN"
                    autocomplete = "off" value = {this.state.ISBN}/>
                  </label>
                </div>
                <br></br>
                 <div className = "form-group">
                   <label> Author:
                    <input type = "text" onChange={(e)=>{this.authorChange(e)}} className = "form-control"
                    id = "author" autocomplete = "off" value = {this.state.author}/>
                   </label>
                </div>
                <br></br>
                <div className = "form-group">
                   <label> Author Url:
                    <input type = "text" onChange={(e)=>{this.authorUrlChange(e)}} className = "form-control"
                    id = "author_url" autocomplete = "off" value = {this.state.author_url}/>
                   </label>
                </div>
                <br></br>
                <div className = "form-group">
                  <label> Book Url:
                    <input type = "text" onChange={(e)=>{this.bookUrlChange(e)}} className = "form-control" id = "book_url"
                    autocomplete = "off" value = {this.state.book_url}/>
                  </label>
                </div>
                <br></br>
                <div className = "form-group">
                 <label> Rating:
                    <input type = "number" onChange={(e)=>{this.ratingChange(e)}} className = "form-control" id = "rating"
                    autocomplete = "off" value = {this.state.rating}/>
                 </label>
                </div>
                <br></br>
                <div className = "form-group">
                   <label> Rating Count:
                    <input type = "number" onChange={(e)=>{this.ratingCountChange(e)}} className = "form-control"
                    id = "rating_count" autocomplete = "off" value = {this.state.rating_count}/>
                   </label>
                </div>
                <br></br>
                <div className = "form-group">
                   <label> Review Count:
                    <input type = "number" onChange={(e)=>{this.reviewCountChange(e)}} className = "form-control"
                    id = "review_count" autocomplete = "off" value = {this.state.review_count}/>
                    </label>
                </div>
                <br></br>
                <div className = "form-group">
                   <label> Book ID:
                    <input type = "number" onChange={(e)=>{this.bookIDChange(e)}} className = "form-control"
                    id = "book_id" autocomplete = "off" value = {this.state.book_id}/>
                    </label>
                </div>
                <br></br>
                <div className = "form-group">
                   <label> Image Url
                    <input type = "text" onChange={(e)=>{this.imageUrlChange(e)}} className = "form-control"
                    id = "image_url" autocomplete = "off" value = {this.state.image_url}/>
                   </label>
                </div>
                 <div className = "form-group">
                   <label> Similar Books:
                    <input type = "text" onChange={(e)=>{this.similarBooksChange(e)}} className = "form-control"
                    id = "similar_books" autocomplete = "off" value = {this.state.similar_books}/>
                   </label>
                </div>
                <button onClick={(e)=>{this.submit(e, this.state.book_id)}} className = "btn btn-block btn-primary"> Submit </button>
                <br></br>
                <br></br>
                <h3> Server Result: {this.state.server_result} </h3>

        </div>
        <div className = "container mt-5">
                <div className = "row mt-5">
                    <h1> List of Books from GoodReads Database </h1>
                    <br></br>
                    <br></br>
                    {this.state.books.map((Book) => {
                        return(
                            <div>
                                <br></br>
                                <br></br>
                                <h3> {Book.title} </h3>
                                <p> Book ID: {Book.book_id} </p>
                                <p> ISBN: {Book.ISBN} </p>
                                <p> Book Url: {Book.book_url} </p>
                                <p> Author: {Book.author} </p>
                                <p> Author Url: {Book.author_url} </p>
                                <p> Rating: {Book.rating} </p>
                                <p> Rating Count: {Book.rating_count} </p>
                                <p> Review Count: {Book.review_count} </p>
                                <p> Image Url: {Book.image_url} </p>
                                <p> Similar Books: {Book.similar_books} </p>
                                <div className = "row mt-5">
                                    <div className = "col-md-1 mt-5">
                                        <button onClick={(e)=>this.updateBook(Book)}  className = "btn btm-sm btn-primary">Update</button>
                                    </div>
                                    <div className = "col-md-1 mt-5">
                                        <button onClick={(e)=>{this.deleteBook(Book.book_id)}} className = "btn btm-sm btn-primary">Delete
                                          </button>
                                    </div>
                                    <br></br>
                                    <br></br>
                                </div>
                          </div>
                      )
                    })}
                </div>
        <br></br>
        <br></br>
        <br></br>
        <br></br>
        </div>
        </div>
      )

   }
}

export default BookComponent;


