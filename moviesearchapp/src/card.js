import React,{useState} from 'react';

export default function Card(props){
    const info=props.movie;
    return (
        <div className="card" >
            <img className="card--image"
                 src={`https://image.tmdb.org/t/p/w185_and_h278_bestv2/${info.poster_path}`}
                 alt={info.title + ' poster'}
            />
            <div className="card--content">
                <h2 className="card--title">{info.title}</h2>
                <p><small>RELEASE DATE: {info.release_date}</small></p>
                <p><small>RATING: {info.vote_average}</small></p>
                <p className="card--desc">{info.overview}</p>

            </div>

        </div>
    );

}