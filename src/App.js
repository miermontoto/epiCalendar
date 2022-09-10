import React, { useState } from "react";
import { Redirect, Route, Routes } from "react-router-dom";

import Form from "./components/Form/Form";
import Settings from "./components/Settings/Settings";
import classes from "./App.module.css";
import NotValidCookie from "./pages/NotValidCookie";

// IN DEV
import { AuthenticatedTemplate, UnauthenticatedTemplate, useMsal } from "@azure/msal-react";
import { Information } from "./components/Info/Information";
import { SignOutButton } from "./components/Info/SignOutButton";


function App() {
  // State for the modal window to be open or closed
  const [showSettings, setShowSettings] = useState(false);

  // Function to toggle (show) the modal window
  const showSettingsHandler = () => {
    setShowSettings(true);
  };

  // Function to toggle (hide) the modal window
  const hideSettingsHandler = () => {
    setShowSettings(false);
  };

  return (
    <div>
      <Routes>
        <Route path="/error" exact element={<NotValidCookie />} />
        <Route path="*" element={
          <div className={classes.app}>
            {showSettings && <Settings onClose={hideSettingsHandler} />}
            <main>
              <AuthenticatedTemplate>
                <Information />
                <SignOutButton />
              </AuthenticatedTemplate>
              <UnauthenticatedTemplate>
                <Form onShowSettings={showSettingsHandler} />
              </UnauthenticatedTemplate>
            </main>
          </div>
        } />
      </Routes>
    </div>
  );
}

export default App;
