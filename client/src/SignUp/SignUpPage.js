import React, { PropTypes } from 'react';

import SignUpForm from './SignUpForm';

class SignUpPage extends React.Component {
    constructor(prop, context) {
        super(prop, context);

        this.state = {
            errors: {},
            user: {
                email: '',
                password: '',
                confirm_password: ''
            }
        };

        this.processForm = this.processForm.bind(this);
        this.changeUser = this.changeUser.bind(this);
    }

    processForm(event) {
        event.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;
        const confirm_password = this.state.user.confirm_password;

        // TODO: what happens if two are not the same
        if (password!==confirm_password) return;

        fetch('http://localhost:3000/auth/signup', {
            method: 'POST',
            cache: false,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }).then(res => {
            if(res.status === 200){
                this.setState({
                    errors: {}
                });

                // change the current URL to /login
                this.context.router.replace('login');
            } else {
                res.json().then( res =>{
                    const errors = res.errors ? res.errors : {};
                    errors.summary = errors.message;
                    this.setState({errors});
                });
            }
            
        }) 
    }

    changeUser(event) {
        // get name property of dom element that trigger this function
        const field = event.target.name;
        const user = this.state.user;
        user[field] = event.target.value;
        this.setState({ user });

        if(this.state.user.password!==this.state.user.confirm_password){
            const errors = this.state.errors;
            errors.password = "Password and Confirm Password don't match.";
            this.setState({errors});
        } else {
            // to clear the errors from last time
            const errors = this.state.errors;
            errors.password = "";
            this.setState({errors});
        }
    }

    render() {
        return (
            <SignUpForm
                onSubmit={this.processForm} onChange={this.changeUser}
                errors={ this.state.errors } user={this.state.user}
            />
        );
    }

}

// To make react-router work
SignUpPage.contextTypes = {
  router: PropTypes.object.isRequired
};

export default SignUpPage;
