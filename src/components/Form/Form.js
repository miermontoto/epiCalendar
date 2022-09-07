import useInput from "../../hooks/use-input";
import HeaderSettingsButton from "./HeaderSettingsButton";
import React from "react";

import SettingsContext from "../../store/settings-context";
import classes from "./Form.module.css";

// Import the default state
import {
  DEFAULT_FILENAME
} from "../../store/settings-context";

// Component that represents the form
const Form = (props) => {
  // Access the settings context
  const ctx = React.useContext(SettingsContext);

  const {
    value: enteredCode,
    isValid: codeIsValid,
    hasError: codeHasError,
    valueChangeHandler: codeChangeHandler,
    inputBlurHandler: codeBlurHandler,
    reset: codeReset,
  } = useInput(
    (value) =>
      value.length === 37 &&
      value.charAt(0) === "0" &&
      value.charAt(1) === "0" &&
      value.charAt(2) === "0" &&
      value.charAt(3) === "0" &&
      value.charAt(27) === ":" &&
      value.charAt(28) === "1" &&
      value.charAt(29) === "d"
  );

  const formSubmissionHandler = (event) => {
    event.preventDefault();

    document.getElementById("form").submit();
    ctx.saveNameHandler(DEFAULT_FILENAME);
    codeReset();
  };

  const logoutHandler = (event) => {
    event.preventDefault();
    document.getElementById("logout").submit();
  };

  // Styling for the form (error message)
  const codeInputClasses = `${classes.form} ${
    codeHasError ? classes.invalid : ""
  }`;

  return (
    <React.Fragment>
      <form method="post" onSubmit={logoutHandler} id="logout" hidden>
        <input type="hidden" name="logout" value="true"></input>
      </form>
      <form method="post" onSubmit={formSubmissionHandler} id="form">
        <legend>epiCalendar (msal test)</legend>
        <div className={classes.control}>
          <div className={codeInputClasses}>
          </div>
          <div>
            <input type="hidden" name="filename" value={ctx.saveas} />
          </div>
          <div>
            <input
              type="hidden"
              name="location"
              value={
                ctx.parse
              }
            />
          </div>
          <div>
            <input
              type="hidden"
              name="class-type"
              value={
                ctx.classParsing
              }
            />
          </div>
          <div>
            <input type="hidden" name="extension" value={ctx.extension} />
          </div>
        </div>
      </form>

      <div className={classes.actions}>
        <HeaderSettingsButton onClick={props.onShowSettings} />
        <button
          className="button"
          //disabled={!formIsValid}
          onClick={formSubmissionHandler}
        >
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          Generar
        </button>
        <button
          className="button"
          onClick={logoutHandler}
        >

          <span></span>
          <span></span>
          <span></span>
          <span></span>
          Logout
        </button>
      </div>
    </React.Fragment>
  );
};

export default Form;
