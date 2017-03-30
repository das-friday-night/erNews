import React from 'react';
import NewsCard from '../NewsCard/NewsCard';


class NewsPanel extends React.Component{
    constructor(){
        super();
        this.state = {
            news: null
        };
    }

    componentDidMount(){
        this.loadMoreNews();
    }

    loadMoreNews(){
        fetch('http://localhost:3000/news', {
            method: 'GET',
            mode: 'cors',
            headers: new Headers({'Content-Type': 'application/json'}),
            cache: 'no-cache'
        }).then((res) =>  res.json())
            .then((res) => {
                this.setState( {news: this.state.news ? this.state.news.concat(res.news):res.news} );
            });
    }

    renderNews(){
        let news_list = this.state.news.map((news) => {
            return (
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
            return (<div>Loading</div>);
        }

    }

}

export default NewsPanel;