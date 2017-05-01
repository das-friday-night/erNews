import React, { PropTypes } from 'react';
import './Base.css';
import Auth from '../Auth/Auth';
import { Link } from 'react-router';

const Base = ({ children }) => (
    <div>
        <nav className="nav-bar indigo lighten-1">
            <div className="nav-weapper">
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
                            <li><Link to="/login">Log in</Link></li>
                            <li><Link to="/signup">Sign up</Link></li>
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
