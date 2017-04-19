import React, { PropTypes } from 'react';
import './Base.css';
import Auth from '../Auth/Auth'

const Base = ({ children }) => (
    <div>
        <nav className="nav-bar indigo lighten-1">
            <div className="nav-weapper">
                <a href="/" className="brand-logo">ErNews</a>
                <ul id="nav-mobile" className="right">
                    {
                        Auth.isUserAuthenticated() ?
                        (<div>
                            <li>{Auth.getEmail()}</li>
                            <li><a href="/logout">Log out</a></li>
                        </div>)
                        :
                        (<div>
                            <li><a href="/login">Log in</a></li>
                            <li><a href="/signup">Sign up</a></li>
                        </div>)
                    }
                </ul>
            </div>
        </nav>
        <br />

        {children}
    
    </div>
);

// Reast propTypes: used for type check 
// https://facebook.github.io/react/docs/typechecking-with-proptypes.html
Base.propTypes = { children: PropTypes.object.isRequired };
export default Base;
