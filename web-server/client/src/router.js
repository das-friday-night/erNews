import Base from './Base/Base';
import App from './App/App';
import Auth from './Auth/Auth';
import LoginPage from './Login/LoginPage';
import SignUp from './SignUp/SignUpPage';
import StatsPanel from './Stats/StatsPanel';


// TODO: understand this component style router
const routes = {
    component: Base,
    childRoutes: [
        {
            path: '/',
            getComponent: (location, callback) => {
                if (!Auth.isUserAuthenticated()) {
                    callback(null, LoginPage);
                } else {
                    callback(null, App);
                }
            }
        },
        {
            path: '/stats',
            getComponent: (location, callback) => {
                if (!Auth.isUserAuthenticated()) {
                    callback(null, LoginPage);
                } else {
                    callback(null, StatsPanel);
                }
            }
        },
        {
            path: '/login',
            component: LoginPage
        },
        {
            path: '/logout',
            // TODO: understand this onEnter and replace
            onEnter: (nextState, replace) => {
                Auth.deauthenticateUser();

                // change the current URL to /
                replace('/');
            }
        },
        {
            path: '/signup',
            component: SignUp
        }
    ]
};

export default routes;
