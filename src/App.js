import React, { useState } from "react";
import { Route, Switch } from "react-router-dom";

import Form from "./components/Form/Form";
import Settings from "./components/Settings/Settings";
import Info from "./components/Info/Info";
import classes from "./App.module.css";
import NotValidCookie from "./pages/NotValidCookie";

function App() {
  // State for the modal window to be open or closed
  const [showSettings, setShowSettings] = useState(false);
  const [showInfo, setShowInfo] = useState(false);

  // Function to toggle (show) the modal window
  const showSettingsHandler = () => {
    setShowSettings(true);
  };

  // Function to toggle (hide) the modal window
  const hideSettingsHandler = () => {
    setShowSettings(false);
  };

  // Function to toggle (show) the modal window
  const showInfoHandler = () => {
    setShowInfo(true);
  };

  // Function to toggle (hide) the modal window
  const hideInfoHandler = () => {
    setShowInfo(false);
  };

  return (
    <div>
      <Switch>
        <Route path="/error" exact>
          <NotValidCookie />
        </Route>
        <Route path="*">
          <div className={classes.app}>
            {showSettings && <Settings onClose={hideSettingsHandler} />}
            {showInfo && <Info onClose={hideInfoHandler} />}
            <main>
              <Form onShowSettings={showSettingsHandler} onShowInfo={showInfoHandler} />
            </main>
          </div>
        </Route>
      </Switch>
    </div>
  );
}

export default App;
