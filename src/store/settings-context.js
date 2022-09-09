import { parse } from "nth-check";
import React, { createContext, useEffect, useState } from "react";

// Default values for the context
export const DEFAULT_FILENAME = "Calendario";
export const DEFAULT_UNIVERSITY = "epi";

// Context for the settings of the app (better autocomplete)
const SettingsContext = createContext({

  saveNameHandler: (name) => { },
  saveas: "",
  parse: true,
  parseHandler: (state) => { },
  classParsing: true,
  classParsingHandler: (state) => { },
  links: true,
  linksHandler: (state) => { },
  update: false,
  updateHandler: (state) => { },
  extension: ".ics",
  extensionHandler: (extension) => { },
});

export const SettingsProvider = (props) => {
  const [saveas, setSaveas] = useState("Calendario"); // State for the filename

  // States for checkboxes
  const [update, setUpdate] = useState(false);
  const [isCheckedParsing, setIsCheckedParsing] = useState(true);
  const [isClassParsing, setIsClassParsing] = useState(true);
  const [isLinks, setIsLinks] = useState(true);

  // State for the extension of the file
  const [extension, setExtension] = useState(".ics");

  // Function to set the filename state
  const saveNameHandler = (name) => {
    setSaveas(name);
  };

  // Functions to set the checkboxes state
  const parseHandler = (state) => {
    setIsCheckedParsing(state);
  };
  const classParsingHandler = (state) => {
    setIsClassParsing(state);
  };
  const linksHandler = (state) => {
    setIsLinks(state);
  }

  // Function to set the update state
  const updateHandler = (state) => {
    setUpdate(state);
  };

  // Function to set the extension state
  const extensionHandler = (extension) => {
    setExtension(extension);
  };

  return (
    <SettingsContext.Provider
      value={{
        // check: checkHandler,
        saveNameHandler: saveNameHandler,
        saveas: saveas,
        parseHandler: parseHandler,
        parse: isCheckedParsing,
        classParsing: isClassParsing,
        classParsingHandler: classParsingHandler,
        links: isLinks,
        linksHandler: linksHandler,
        update: update,
        updateHandler: updateHandler,
        extension: extension,
        extensionHandler: extensionHandler,
      }}
    >
      {props.children}
    </SettingsContext.Provider>
  );
};

export default SettingsContext;
