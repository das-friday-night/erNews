import React, { PropTypes } from 'react';
import './Base.css';
import Auth from '../Auth/Auth';
import { Link } from 'react-router';
import { Dropdown, Button, NavItem, Navbar } from 'react-materialize';
const Base = ({ children }) => (
    <div>
        <div className="navbar-fixed">
            <Navbar brand='ErNews' right className="grey darken-4">
                {
                    Auth.isUserAuthenticated() ?
                    (<div>
                        <NavItem>{Auth.getEmail()}</NavItem>
                        <NavItem>
                            <Dropdown className="teal accent-4" trigger={<Button className="grey darken-1">Profile</Button>}>
                                <NavItem><Link to="/stats">Stats</Link></NavItem>
                                <NavItem divider />
                                <NavItem><Link to="/logout">Log out</Link></NavItem>
                            </Dropdown>
                        </NavItem>
                    </div>)
                    :
                    (<div>
                        <NavItem><Link className="waves-effect waves-light" to="/login">Log in</Link></NavItem>
                        <NavItem><Link className="waves-effect waves-light" to="/signup">Sign up</Link></NavItem>
                    </div>)
                }
            </Navbar>
        </div>

        {children}
    
    </div>
);

// Reast propTypes: used for type check 
// https://facebook.github.io/react/docs/typechecking-with-proptypes.html
Base.propTypes = { children: PropTypes.object.isRequired };
export default Base;
