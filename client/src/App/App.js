// didn't found instruction
import "materialize-css/dist/css/materialize.min.css";
import "materialize-css/dist/js/materialize.min.js";

import React from 'react';
import logo from '../logo.svg';
import './App.css';
import NewsPanel from '../NewsPanel/NewsPanel';

class App extends React.Component {
    render() {
        return (
            <div>
                <img src={logo} className="App-logo" alt="logo" />
                <div className="container">
                    <div>
                        <NewsPanel/>
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
