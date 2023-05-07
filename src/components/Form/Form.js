import useInput from "../../hooks/use-input";
import HeaderSettingsButton from "./HeaderSettingsButton";
import HeaderInfoButton from "./HeaderInfoButton";
import React from "react";

import SettingsContext from "../../store/settings-context";
import classes from "./Form.module.css";

// Import the default state
import { DEFAULT_FILENAME } from "../../store/settings-context";

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
      value.charAt(28) === "1"
  );

  // Variable for the validity of the form
  let formIsValid = codeIsValid;

  const formSubmissionHandler = (event) => {
    event.preventDefault();
    if (!codeIsValid) {
      console.log("Code is not valid");
      return;
    }

    document.getElementById("form").submit();
    ctx.saveNameHandler(DEFAULT_FILENAME);
    codeReset();
  };

  // Styling for the form (error message)
  const codeInputClasses = `${classes.form} ${
    codeHasError ? classes.invalid : ""
  }`;

  return (
    <React.Fragment>
      <form method="post" onSubmit={formSubmissionHandler} id="form">
        <legend>epiCalendar</legend>
        <div className={classes.control}>
          <div className={codeInputClasses}>
          <a href="https://mier.info/epiCalendar" target="_blank" rel="noreferrer" id="tutorial"
            title="Enlace de ayuda para obtener JSESSIONID">JSESSIONID</a>
            <input
              type="text"
              id="codigo"
              name="jsessionid"
              onChange={codeChangeHandler}
              onBlur={codeBlurHandler}
              value={enteredCode}
              placeholder="0000XXXXXXXXXXXXXXXXXXXXXXX:1XXXXXXXX"
            />
            {codeHasError && (
              <React.Fragment>
                <p className={classes.error}>El código no es válido.</p>
              </React.Fragment>
            )}
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
        <HeaderInfoButton onClick={props.onShowInfo} className={classes.infoButton}/>
        <button
          className={classes.mainButton}
          disabled={!formIsValid}
          onClick={formSubmissionHandler}
        >
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          Generar
        </button>
        <HeaderSettingsButton onClick={props.onShowSettings} />
      </div>
    </React.Fragment>
  );
};

export default Form;
