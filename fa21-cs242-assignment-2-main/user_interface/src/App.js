import './App.css';
import {useState, useEffect} from 'react';
import BookComponent from './components/BookComponent.js';
import AuthorComponent from './components/AuthorComponent.js';
import axios from 'axios';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import Container from 'react-bootstrap/Container';

/**
* The following class is meant be the interface where the books and author information will both meet. It will help
with displaying the tabs. I used some code from the following site: https://www.w3schools.com/howto/howto_js_tabs.asp.
*/

class App extends React.Component {

   constructor(props) {
      super(props);
   }

   openTab(event, tabChoice) {

      var i, tabcontent, tablinks;

      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }
      tablinks = document.getElementsByClassName("tablinks");

      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }

      document.getElementById(tabChoice).style.display = "block";
      event.currentTarget.className += " active";
   }


   render() {
     return(
         <div>
             <h1> Welcome to GoodRead Database! </h1>
             <div class="tab">
                 <button class="tablinks" onClick={e=>{this.openTab(e, 'Books')}}>Books</button>
                 <button class="tablinks" onClick={e=>{this.openTab(e, 'Authors')}}>Authors</button>
             </div>

            <div id="Books" class="tabcontent">
              <BookComponent />
            </div>

            <div id="Authors" class="tabcontent">
              <AuthorComponent />
            </div>

        </div>
     )
   }
}

export default App;


