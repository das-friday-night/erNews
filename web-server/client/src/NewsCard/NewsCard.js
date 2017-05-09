import React from 'react';
import Auth from '../Auth/Auth';
import './NewsCard.css';

class NewsCard extends React.Component {
    sendLog(){
        let url = 'http://localhost:3000/news/userID/' + Auth.getEmail();
        fetch(url, {
            method: 'POST',
            mode: 'cors',
            headers: new Headers({
                'Authorization': 'bearer ' + Auth.getToken(),
                'Content-Type': 'application/json'
            }),
            cache: 'no-cache',
            body: JSON.stringify({newsID: this.props.news.digest})
        });
    }

    redirectUrl(url){
        this.sendLog();
        window.open(url,'_blank');
    }
    
    render(){
        return (
            <div className="news-container" onClick={() => {this.redirectUrl(this.props.news.url)}}>
                <div className="row">
                    <div className="col s4 fill">
                        <img src={this.props.news.urlToImage} alt="news"/>
                    </div>
                    <div className="col s8">
                        <div className="news-intro-panel">
                            <h4>{this.props.news.title}</h4>
                            <div className="news-description">
                                <p>{this.props.news.description}</p>
                                <div>
                                    {this.props.news.source != null && <div className='chip light-blue news-chip'>{this.props.news.source}</div>}
                                    {this.props.news.reason != null && <div className='chip light-green news-chip'>{this.props.news.reason}</div>}
                                    {this.props.news.publishedAt != null && <div className='chip amber lighten-1 news-chip'>{this.props.news.publishedAt}</div>}
                                    {this.props.news.class != null && <div className='chip amber lighten-4 news-chip'>{this.props.news.class}</div>}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default NewsCard;