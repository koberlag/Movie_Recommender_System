import React, { useState } from 'react';
import HomePage from './pages/HomePage'
import RatingPage from './pages/RatingPage'
import './App.scss';

function App() {
  const location = window.location.pathname
  const [route, updateRoute ] = useState(location || '/')
  

  const Page = route === '/' ? <HomePage onChangeRoute={updateRoute} /> : <RatingPage onChangeRoute={updateRoute} />
  return (
    <div className="App full-width full-height">
      {Page}
    </div>
  );
}

export default App;
