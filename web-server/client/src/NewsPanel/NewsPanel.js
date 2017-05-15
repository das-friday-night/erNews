import React from 'react';
import _ from 'lodash';
import NewsCard from '../NewsCard/NewsCard';
import './NewsPanel.css';
import Auth from '../Auth/Auth';
import {Preloader} from 'react-materialize';

class NewsPanel extends React.Component{
    constructor(){
        super();
        this.state = {
            news: null,
            pageID: 0,
            loadedAll: false
        };
    }

    componentDidMount(){
        this.loadMoreNews();
        
        // debounce effect every 1 sec
        this.loadMoreNews = _.debounce(this.loadMoreNews, 700);
        window.addEventListener('scroll', this.onScrollBottom.bind(this));
    }

    componenWillUnMount() {
        window.removeEventListener('scroll', this.onScrollBottom);
    }

    onScrollBottom() {
        let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        // scrollY: current scroll height from to the top of entire web page.
        // window.innerHeight: height of current window, not the entire web page height
        // document.body.offsetHeight: the entire web page height
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight)) {
            this.loadMoreNews();
        }
    }

    loadMoreNews(){
        let url = 'http://localhost:3000/news/userID/' + Auth.getEmail() + "/pageID/" + this.state.pageID;
        fetch(url, {
            method: 'GET',
            mode: 'cors',
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': 'bearer ' + Auth.getToken()
            }),
            cache: 'no-cache'
        }).then((res) => { 
            return res.json();
        }).then((res) => {
            if(!res || res.news.length === 0) {
                this.setState({loadedAll : true});
            } else {
                this.setState({
                    news: this.state.news ? this.state.news.concat(res.news):res.news,
                    pageID: this.state.pageID + 1,
                    loadedAll: false
                });
            }  
        });
    }

    renderNews(){
        let news_list = this.state.news.map((news) => {
            return (
                // <li className="collection-item">
                <li className="collection-item" key={news.digest}>
                    <NewsCard news={news}/>
                </li>
            );
        });

        return (
            <ul className="collection">
                {news_list}
            </ul>
        );
    }

    render(){
        if(this.state.news){
            return (
                <div>
                    {this.renderNews()}
                </div>
            );
        } else {
            return (<Preloader flashing size='big'/>);
        }

    }

}

export default NewsPanel;