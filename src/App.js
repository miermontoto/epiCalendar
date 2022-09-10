import React, { useState } from 'react';
import './App.css';
import { Form } from './components/Form/Form';
import Settings from "./components/Settings/Settings";
import { Footer } from './components/UI/Footer';

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
    <div className="group">
      {/* <h1 id="title">autoUniCalendar: Descarga tu calendario de Uniovi.</h1> */}
      {/* <br /> */}
      <AuthenticatedTemplate>
        <Information />
        <SignOutButton />
      </AuthenticatedTemplate>
      <UnauthenticatedTemplate>
        {showSettings && <Settings onClose={hideSettingsHandler} />}
        <Form onShowSettings={showSettingsHandler} />
      </UnauthenticatedTemplate>
      <Footer />
    </div>
  );
}

export default App;
