import React from "react";

import useInput from "../../hooks/use-input";
import classes from "./Saver.module.css";

import SettingsContext from "../../store/settings-context";

// Component to set the name of the filename
const Saver = (props) => {
  // Access the settings context
  const ctx = React.useContext(SettingsContext);

  // useInput hook to get the name of filename
  const {
    value: enteredName,
    valueChangeHandler: nameChangeHandler,
    inputBlurHandler: nameBlurHandler,
  } = useInput((value) => value.length > 0);

  // Function to set the name of the file
  const nameHandlerValue = (name) => {
    if (name.target.value.trim().length > 0) {
      nameChangeHandler(name);
      props.onSave(name.target.value);
    } else if (name.target.value === "") {
      nameChangeHandler(name);
      props.onSave("Calendario");
    }
  };

  const handleExtensionChange = (event) => {
    ctx.extensionHandler(event.target.value);
  };

  return (
    <React.Fragment>
      <div className={classes.saveas}>
        <h3>Filename</h3>
      </div>
      <div className={classes.form}>
        <input
          type="text"
          id="saveAs"
          name="filename"
          onChange={nameHandlerValue}
          onBlur={nameBlurHandler}
          value={enteredName}
          placeholder="Calendario"
        />
        <div className={classes.extension}>
          <select value={ctx.extension} onChange={handleExtensionChange}>
            <option value=".ics">.ics</option>
            <option value=".csv">.csv</option>
          </select>
        </div>
      </div>
    </React.Fragment>
  );
};

export default Saver;
