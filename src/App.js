import React, { useState } from 'react';
import './App.css';
import { Form } from './components/Form/Form';
import Settings from "./components/Settings/Settings";
import { Footer } from './components/UI/Footer';

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
      {showSettings && <Settings onClose={hideSettingsHandler} />}
      <Form onShowSettings={showSettingsHandler} />
      <Footer />
    </div>
  );
}

export default App;
