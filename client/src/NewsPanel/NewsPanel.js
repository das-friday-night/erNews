import React from 'react';
import _ from 'lodash';
import NewsCard from '../NewsCard/NewsCard';
import Auth from '../Auth/Auth';


class NewsPanel extends React.Component{
    constructor(){
        super();
        this.state = {
            news: null
        };
    }

    componentDidMount(){
        this.loadMoreNews();
        
        // debounce effect every 1 sec
        this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
        window.addEventListener('scroll', ()=>{
            let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
            // scrollY: current scroll height from to the top of entire web page.
            // window.innerHeight: height of current window, not the entire web page height
            // document.body.offsetHeight: the entire web page height
            if ((window.innerHeight + scrollY) >= (document.body.offsetHeight)) {
                // console.log('Loading more news');
                this.loadMoreNews();
            }
        });
    }

    loadMoreNews(){
        fetch('http://localhost:3000/news', {
            method: 'GET',
            mode: 'cors',
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': 'bearer ' + Auth.getToken()
            }),
            cache: 'no-cache'
        }).then((res) =>  res.json())
            .then((res) => {
                this.setState( {news: this.state.news ? this.state.news.concat(res.news):res.news} );
            });
    }

    renderNews(){
        let news_list = this.state.news.map((news) => {
            return (
                // <li className="collection-item" key={news.digest}>
                <li className="collection-item">
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
            return (<div>Loading</div>);
        }

    }

}

export default NewsPanel;