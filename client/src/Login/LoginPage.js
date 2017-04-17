import React, {PropTypes} from 'react';

import Auth from '../Auth/Auth';
import LoginForm from './LoginForm';

var DEBUGMODE = true;

class LoginPage extends React.Component {

  constructor(props, context) {
    super(props, context);

    this.state = {
        errors: {},
        user: {
            email:'',
            password: ''
        }
    };

    // This binding is necessary to make `this` work in the callback
    // http://reactkungfu.com/2015/07/why-and-how-to-bind-methods-in-your-react-component-classes/
    this.processForm = this.processForm.bind(this);
    this.changeUser = this.changeUser.bind(this);
  }

  processForm(event) {
      // prevent default action. in this case, action is the form submission event
      event.preventDefault();

      const email = this.state.user.email;
      const password = this.state.user.password;
      
      if(email !== '' && password !== ''){
        fetch('http://localhost:3000/auth/login', {
            method: 'POST',
            mode: 'cors',
            cache: false,
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: JSON.stringify({
                email: email,
                password: password
            })
        }).then(res => {
            if(res.status === 200){
                this.setState({errors : {}});
                res.json().then( res => {
                    if(DEBUGMODE) console.log(res);
                    Auth.authenticateUser(res.token, this.state.user.email);

                    // route to home after authenicate ok
                    this.context.router.replace('/');
                });
            } else {
                res.json().then( res => {
                    const errors = res.errors ? res.errors : {};
                    errors.summary = res.message;
                    this.setState({errors});
                });
            }
        });
      }
  }

  changeUser(event){
      // get name property of dom element that trigger this function
      const field = event.target.name;
      const user = this.state.user;
      user[field] = event.target.value;
      this.setState({user});
  }

  render(){
      return (
          <LoginForm
            onSubmit={this.processForm} onChange={this.changeUser}
            errors={this.state.errors} user={this.state.user} />
      );
  }

}


LoginPage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default LoginPage;
