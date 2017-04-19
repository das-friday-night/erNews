import "materialize-css/dist/css/materialize.min.css";
import "materialize-css/dist/js/materialize.min.js";

import React from 'react';
import logo1 from '../er.svg';
import logo2 from '../wen.svg';
import './App.css';
import NewsPanel from '../NewsPanel/NewsPanel';

class App extends React.Component {
    render() {
        return (
            <div>
                <div className="App-logo">
                    <img src={logo1} className="logo" alt="logo" />
                    <img src={logo2} className="logo" alt="logo" />
                </div>

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
