import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Route, BrowserRouter as Router, Switch } from 'react-router-dom';
import { PublicTemplateRoute } from './templates';
import Main from "./route/main/index"
import Live from './route/live/index';
import History from './route/history/index';
import AboutUs from './route/aboutUs/index';
function App() {
  return (
    <Router basename="/" hashType="noslash">
      <Switch>
        <PublicTemplateRoute
        path="/main"
        component={Main}
        />
         <PublicTemplateRoute
        path="/live"
        component={Live}
        />

<PublicTemplateRoute
        path="/history"
        component={History}
        />

<PublicTemplateRoute
        path="/about"
        component={AboutUs}
        />
      </Switch>
    </Router>
  );
}

export default App;
