import {BrowserRouter, Route, Switch} from 'react-router-dom';
import React, {Suspense} from 'react';
import './App.css';
import NavBar from './components/NavBar/NavBar';
import LoginPage from './components/UserPage/LoginPage';
import SignupPage from './components/UserPage/SignupPage';

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={(<div>...</div>)}>
        <NavBar />
        <div className="App">
            <Switch>
              <Route exact path="/login" component={LoginPage}></Route>
              <Route exact path="/signup" component={SignupPage}></Route>
            </Switch>
          </div>
      </Suspense>
    </BrowserRouter>
    );
}

export default App;