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

const setLocalStorage = (key, value) => {
  try {
    const value = window.localStorage.setItem(key, value)
    return value;
  } catch {
    return null;
  }
}

class HomePage extends Component {

  handleUsername = (e) => {
    const username = e.target.value;
    setLocalStorage('username',username);
    setCookie('username', username, 7);
  }
  redirectToRating = () => {
    this.props.onChangeRoute('rating');
  }

  render(){
    return (
      <Container maxWidth="sm" style={{marginTop: '48px'}}>
        <Box display="flex" p={1} flexDirection="column">
          <Box my={3}>
            <h3> CS 5593 </h3>
          </Box>
          <FormLabel>Login</FormLabel>
          <Input placeholder="Enter your username" onChange={this.handleUsername} defaultValue={getCookie('username')}/>
          <Box mt={4}>
            <Button variant="contained" onClick={this.redirectToRating}>Login & Review</Button>
          </Box>
        </Box>
      </Container>
    );
  }
}

export default HomePage