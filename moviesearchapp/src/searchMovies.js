import React, {useState} from "react";
import Card from "./card.js";
import "./style.css";
import TvCard from "./tvcard";
export default function SearchMovies(){

    //states- input query, movies
    const [query, setQuery] = useState('');
    //create the state for movies, and update that state appropriate
    const [movies, setMovies] = useState([]);
    const [mode,setMode]= useState("movie")
    const towrite= mode=== "movie" ? "Movie Name" : "TV Show Name";
    const searchMovies = async (e) => {
        e.preventDefault();

        const url = `https://api.themoviedb.org/3/search/${mode}?api_key=5dcf7f28a88be0edc01bbbde06f024ab&language=en-US&query=${query}&page=1&include_adult=false`;

        try {
            const res = await fetch(url);
            const data  = await res.json();
            setMovies(data.results);
            console.log(data.results)
        }catch(err){
            console.error(err);
        }
    }
    const handleClick=()=>{
        setMode(mode === "movie" ? "tv" : "movie");
        setMovies([]);

    }
    if (mode==="movie"){
    return (
        <>
            <button className="button1" type="button" onClick={handleClick}> Switch Mode</button>
            <form className="form" onSubmit={searchMovies}>
                <label className="label" htmlFor="query">{towrite}</label>
                <input className="input" type="text" name="query"
                       placeholder="i.e. Jurassic Park"
                       value={query} onChange={(e) => setQuery(e.target.value)}
                />
                <button className="button" type="submit">Search</button>

            </form>
            <div className="card-list">
                {movies.filter(movie => movie.poster_path).map(movie => (
                    <Card key={movie.id}
                          movie={movie}
                    />

                ))}
            </div>
        </>
    )}
    else{
        return (
            <>
                <button className="button1" type="button" onClick={handleClick}> Switch Mode</button>
                <form className="form" onSubmit={searchMovies}>
                    <label className="label" htmlFor="query">{towrite}</label>
                    <input className="input" type="text" name="query"
                           placeholder="i.e. Jurassic Park"
                           value={query} onChange={(e) => setQuery(e.target.value)}
                    />
                    <button className="button" type="submit">Search</button>

                </form>
                <div className="card-list">
                    {movies.filter(movie => movie.poster_path).map(movie => (
                        <TvCard key={movie.id}
                                movie={movie}
                        />

                    ))}
                </div>
            </>
        )
    }
}