import React, { PropTypes } from 'react';
import './Base.css';
import Auth from '../Auth/Auth';
import { Link } from 'react-router';

const Base = ({ children }) => (
    <div>
        <div className="navbar-fixed">
            <nav className="nav-bar grey darken-4">
                <div className="nav-weapper z-depth-2">
                    <Link to="/" className="brand-logo">ErNews</Link>
                    <ul id="nav-mobile" className="right">
                        {
                            Auth.isUserAuthenticated() ?
                            (<div>
                                <li>{Auth.getEmail()}</li>
                                <li><Link to="/logout">Log out</Link></li>
                            </div>)
                            :
                            (<div>
                                <li><Link className="waves-effect waves-light" to="/login">Log in</Link></li>
                                <li><Link className="waves-effect waves-light" to="/signup">Sign up</Link></li>
                            </div>)
                        }
                    </ul>
                </div>
            </nav>
        </div>

        {children}
    
    </div>
);

// Reast propTypes: used for type check 
// https://facebook.github.io/react/docs/typechecking-with-proptypes.html
Base.propTypes = { children: PropTypes.object.isRequired };
export default Base;
