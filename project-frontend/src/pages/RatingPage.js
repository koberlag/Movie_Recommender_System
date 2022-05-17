import React, { Component } from 'react'
import Container from '@material-ui/core/Container';

import { FormLabel } from '@material-ui/core';
import { Input } from '@material-ui/core';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import { setCookie, getCookie } from './../utils';

const getLocalStorage = (key) => {
  try {
    const value = window.localStorage.getItem(key)
    return value;
  } catch {
    return null;
  }
}

function getLocalStorageWithExpiry(key) {
	const itemStr = localStorage.getItem(key)
	// if the item doesn't exist, return null
	if (!itemStr) {
		return null
	}
	const item = JSON.parse(itemStr)
	const now = new Date()
	// compare the expiry time of the item with the current time
	if (now.getTime() > item.expiry) {
		// If the item is expired, delete the item from storage
		// and return null
		localStorage.removeItem(key)
		return null
	}
	return item.value
}

function setLocalStorageWithExpiry(key, value, ttl) {
	const now = new Date()

	// `item` is an object which contains the original value
	// as well as the time when it's supposed to expire
	const item = {
		value: value,
		expiry: now.getTime() + ttl,
	}
	localStorage.setItem(key, JSON.stringify(item))
}

class RatingPage extends Component {

  constructor(props){
    super(props);
    this.state = {
      username: getCookie('username') || '',
      movieId: '',
      title: ''
    }
  }

  setSkippedMovieIdsInLocalStorage(skipKey, movieId){
    const ttl = 24*60*60 // 24 hrs in seconds
    const skippedMovieIds = getLocalStorageWithExpiry(skipKey) || []
    if(!skippedMovieIds.includes(movieId)){
      skippedMovieIds.push(movieId)
      setLocalStorageWithExpiry(skipKey, skippedMovieIds, ttl)
    }
  }

  submitVote = (rating) => {
    const { movieId, username } = this.state;
    const params = new URLSearchParams({
      username,
      rating,
      movieId
    })
    fetch('http://localhost:8000/vote/?' + params)
    .then(response => response.json())
    .then(data => {
      if(data.success){
        const skipKey = `${username}_skipped_movie_ids`
        // Add skipped movie to local storage
        if(rating == 0){
          this.setSkippedMovieIdsInLocalStorage(skipKey, movieId)
        }
        const skippedMovieIds = getLocalStorageWithExpiry(skipKey)
        this.fetchRecommendation(skippedMovieIds);
      }
    });
  }

  fetchRecommendation(skippedMovieIds) {
    skippedMovieIds = skippedMovieIds || []
    const { username } = this.state;
    fetch('http://localhost:8000/recommendation/?' + (new URLSearchParams({
      username,
      skippedMovieIds
    })))
    .then(response => response.json())
    .then(data => {
      if(data.success){
        this.setState({
          movieId: data.movie.movieId,
          title: data.movie.title,
          posterUrl: data.movie.posterUrl
        });
      }
    });
  }

  componentDidMount() {
    this.fetchRecommendation();
  }

  render(){
    return (
      <Container maxWidth="sm" style={{marginTop: '48px'}}>
        <Box display="flex" p={1} flexDirection="column" justifyContent="center" alignContent="center" alignSelf="center" >

          <h3><FormLabel>{this.state.title}</FormLabel></h3>
          <img 
            style={{alignSelf: 'center'}}
            height={500}
            width={350}
            src={this.state.posterUrl} 
          />
          <Box mt={4} width={'100%'} display="flex" alignSelf="center" justifyContent="space-between">
            <Box>
              <Button onClick={() => this.submitVote(-1)} variant="contained"> Dislike 👎 </Button>
            </Box>
            <Box>
              <Button onClick={() => this.submitVote(0)} variant="contained"> Skip ⛔ </Button>
            </Box> 
            <Box>
              <Button onClick={() => this.submitVote(1)} variant="contained"> Like 👍 </Button>
            </Box>
          </Box>
        </Box>
      </Container>
    );
  }
}

export default RatingPage