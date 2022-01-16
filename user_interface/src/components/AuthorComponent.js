import '../App.css';
import {useState, useEffect} from 'react';
import axios from 'axios';
import React from 'react';

/**
* The following class maintains all of the information about Author Components for the front end with a list of
* all books and a front end component. Code was referred to from https://www.youtube.com/watch?v=57PpSudAzJM and
* https://www.youtube.com/watch?v=msEmUtYqVV0
*/

class AuthorComponent extends React.Component {

   /*
   * Constructs an AuthorComponent object which creates the default values for the form and the list of books to print
   */
   constructor(props) {
      super(props);
      this.state =
      {
         authors: [],
         name: 'None',
         author_id: 0,
         author_books: 'None',
         author_url: 'None',
         rating: 0,
         rating_count: 0,
         review_count: 0,
         image_url: 'None',
         related_authors: 'None',
         server_result: '',
         query_server_result: '',
         query:''
      }
   }

   /**
   * Renders the page to print all of the authors from the database and defaults all the values in the form to
   * empty string, None, or 0.
   */
   componentDidMount() {

      fetch('http://localhost:5000/author/list_all')
      .then((resp) => resp.json())
      .then((data) => {
        this.setState({
             authors: data,
             name: 'None',
             author_id: 0,
             author_books: 'None',
             author_url: 'None',
             rating: 0,
             rating_count: 0,
             review_count: 0,
             image_url: 'None',
             related_authors: 'None',
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
   * The following code will set the name for the author object to what is typed in the form
   */
   nameChange = event => {
        this.setState({
            name: event.target.value
        })
   }

   /**
   * The following code will set the authorID for the author object to what is typed in the form
   */
   authorIDChange = event => {
        this.setState({
            author_id: event.target.value
        })
   }

   /**
   * The following code will set the authorUrl for the author object to what is typed in the form
   */
   authorUrlChange = event => {
        this.setState({
            author_url: event.target.value
        })
   }

   /**
   * The following code will set the rating for the author object to what is typed in the form
   */
   ratingChange = event => {
        this.setState({
           rating: event.target.value
        })
   }

   /**
   * The following code will set the rating count for the author object to what is typed in the form
   */
   ratingCountChange = event => {
        this.setState({
           rating_count: event.target.value
        })
   }

   /**
   * The following code will set the review count for the author object to what is typed in the form
   */
   reviewCountChange = event => {
        this.setState({
           review_count: event.target.value
        })
   }

  /**
   * The following code will set the image url for the author object to what is typed in the form
   */
   imageUrlChange = event => {
        this.setState({
            image_url: event.target.value
        })
   }

   /**
   * The following code will set the related authors for the author object to what is typed in the form
   */
   relatedAuthorsChange = event => {
        this.setState({
            related_authors: event.target.value
        })
   }

   /**
   * The following code will set the author books for the author object to what is typed in the form
   */
   authorBooksChange = event => {
        this.setState({
            author_books: event.target.value
        })
   }

  /**
  * Upon completing a form and a user clicks the submit button, this function will reset the form. If an update
  * button was clicked for one of the forms, then a PUT request will be made, else an insert with a POST will be
  * made with an ID.
  */

   submit(event, id) {

        if (this.state.name === '' || this.state.name === 'None') {
               this.setState({
                 name:'None',
                 author_id: 0,
                 author_books: 'None',
                 author_url: 'None',
                 rating: 0,
                 rating_count: 0,
                 review_count: 0,
                 image_url: 'None',
                 related_authors: 'None',
                 server_result: 'Please enter a valid name and reload the page'
              })
            return
        }

        if (id == 0) {

            event.preventDefault()
            axios.post('http://localhost:5000/author', {'name': this.state.name, 'author_url': this.state.author_url,
             'author_id': 23478324,'image_url': this.state.image_url,'rating': this.state.rating,
             'rating_count': this.state.rating_count, 'review_count': this.state.review_count, 'author_books': this.state.author_books,
             'related_authors': this.state.related_authors}).
            then((result) => {
                this.setState({server_result: 'Insert Successful, please reload the page'})
            })
        } else {

            axios.put(`http://localhost:5000/author?id=${id}`, {'name': this.state.name, 'author_url': this.state.author_url,
             'author_id': id,'image_url': this.state.image_url,'rating': this.state.rating,
             'rating_count': this.state.rating_count, 'review_count': this.state.review_count, 'author_books': this.state.author_books,
             'related_authors': this.state.related_authors})
            .then((result) => {
                    this.setState({server_result: 'Update Successful, please reload the page'})
            })
        }

   }

   /**
   * Deletes a author based on the ID passed in and makes a request to the backend
   */
   deleteAuthor(author_id) {
        axios.delete(`http://localhost:5000/author?id=${author_id}`)
        .then(() => {
           this.setState({server_result: 'Deletion successful, please reload the page'})
        })
   }

   /**
   * Updates an author based on the book parameter by populating the fields with the values that were given to them
   */
   updateAuthor(author) {
       this.state.image_url = author.image_url
       this.state.name = author.name
       this.state.related_authors = author.related_authors
       this.state.author_id = author.author_id
       this.state.rating_count = author.rating_count
       this.state.review_count = author.review_count
       this.state.rating = author.rating
       this.state.author_books = author.author_books
       this.state.related_books = author.review_authors

       document.getElementById('image_url').value = author.image_url
       document.getElementById('name').value = author.name
       document.getElementById('related_authors').value = author.related_authors
       document.getElementById('author_id').value = author.author_id
       document.getElementById('author_url').value = author.author_url
       document.getElementById('review_count').value = author.review_count
       document.getElementById('rating_count').value = author.rating_count
       document.getElementById('rating').value = author.rating
       document.getElementById('author_books').value = author.author_books
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
                this.state.authors = resp.data

                if (this.state.authors.length > 0) {
                    this.setState({
                        authors: resp.data,
                        query_server_result: 'Query Successful'
                    })
                } else {
                    this.setState({
                        authors: resp.data,
                        query_server_result: 'No matching results for your query'
                    })
                }
                this.render()
         }
         console.log(this.state)
     })
     .catch(error => {
         this.setState({
             authors: [],
             query_server_result: 'Incorrect query syntax'
         })
        this.render()
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
                <h3> Please Enter a query for an Author </h3>
                <br></br>

                <div className = "form-group">
                    <input type = "text" onChange={(e)=>{this.queryChange(e)}} className = "form-control"
                      autocomplete = "off" placeholder = "Query" id = "author_field"/>
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

                <h2> Enter Author Information </h2>
                <br></br>
                <div className = "form-group">
                    <label> Name
                    <input type = "text" onChange={(e)=>{this.nameChange(e)}} className = "form-control" id = "name"
                    autocomplete = "off" value = {this.state.name}/>
                    </label>
                </div>
                <br></br>
                <div className = "form-group">
                    <label> Author Url
                        <input type = "text" onChange={(e)=>{this.authorUrlChange(e)}} className = "form-control" id = "author_url"
                        autocomplete = "off" value = {this.state.author_url}/>
                    </label>
                </div>
                <br></br>
                <div className = "form-group">
                    <label> Author ID
                        <input type = "number" onChange={(e)=>{this.authorIDChange(e)}} className = "form-control" id = "author_id"
                        autocomplete = "off" value = {this.state.author_id}/>
                    </label>
                </div>
                <br></br>
                <div className = "form-group">
                    <label> Rating
                        <input type = "number" onChange={(e)=>{this.ratingChange(e)}} className = "form-control" id = "rating"
                        autocomplete = "off" value = {this.state.rating}/>
                    </label>
                </div>
                <br></br>
                <div className = "form-group">
                    <label> Rating Count
                        <input type = "number" onChange={(e)=>{this.ratingCountChange(e)}} className = "form-control" id = "rating_count"
                        autocomplete = "off" value = {this.state.rating_count}/>
                    </label>
                </div>
                <br></br>
                <div className = "form-group">
                    <label> Review Count
                        <input type = "number" onChange={(e)=>{this.reviewCountChange(e)}} className = "form-control" id = "review_count"
                        autocomplete = "off" value = {this.state.review_count}/>
                    </label>
                </div>
                <br></br>
                <div className = "form-group">
                    <label> Image Url
                        <input type = "text" onChange={(e)=>{this.imageUrlChange(e)}} className = "form-control" id = "image_url"
                        autocomplete = "off" value = {this.state.image_url}/>
                    </label>
                </div>
                <br></br>
                <div className = "form-group">
                    <label> Related Authors
                        <input type = "text" onChange={(e)=>{this.relatedAuthorsChange(e)}} className = "form-control" id = "related_authors"
                        autocomplete = "off" value = {this.state.related_authors}/>
                    </label>
                </div>
                <br></br>
                 <div className = "form-group">
                    <label> Author Books
                        <input type = "text" onChange={(e)=>{this.authorBooksChange(e)}} className = "form-control" id = "author_books"
                        autocomplete = "off" value = {this.state.related_authors}/>
                    </label>
                </div>
                <br></br>
                <button onClick={(e)=>{this.submit(e, this.state.author_id)}} className = "btn btn-block btn-primary"> Submit </button>
                <br></br>
                <br></br>
                <h3> Server Result: {this.state.server_result} </h3>

        </div>
        <div className = "container mt-5">
                <div className = "row mt-5">
                    <h1> List of Authors from GoodReads Database </h1>
                    <br></br>
                    <br></br>
                    {this.state.authors.map((Author) => {
                        return(
                            <div className = "container">
                                <br></br>
                                <br></br>
                                <h3> {Author.name} </h3>
                                <p> Author ID: {Author.author_id}  </p>
                                <p> Image Url = {Author.image_url}  </p>
                                <p> Author Url: {Author.author_url}  </p>

                                <p> Rating Count: {Author.rating_count} </p>
                                <p> Review Count: {Author.review_count} </p>
                                <p> Author Books: {Author.author_books} </p>
                                <p> Related Authors: {Author.related_authors} </p>
                                <div className = "row mt-5">
                                    <div className = "col-md-1 mt-5">
                                        <button onClick={(e)=>this.updateAuthor(Author)}  className = "btn btm-sm btn-primary">Update</button>
                                    </div>
                                    <div className = "col-md-1 mt-5">
                                        <button onClick={(e)=>{this.deleteAuthor(Author.author_id)}} className = "btn btm-sm btn-primary">Delete
                                          <i className = "fa fa-trash"></i> </button>
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

export default AuthorComponent;
