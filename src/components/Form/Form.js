import React, { useState } from "react";
import useInput from "../../hooks/use-input";
import HeaderInfoButton from "./HeaderInfoButton";
import HeaderSettingsButton from "./HeaderSettingsButton";

import SettingsContext from "../../store/settings-context";
import classes from "./Form.module.css";

// Import the default state
import { DEFAULT_FILENAME } from "../../store/settings-context";

// Component that represents the form
const Form = (props) => {
  // Access the settings context
  const ctx = React.useContext(SettingsContext);

  // estados para manejar errores y loading
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

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

  const formSubmissionHandler = async (event) => {
    event.preventDefault();
    if (!codeIsValid) {
      console.log("Code is not valid");
      return;
    }

    setError("");
    setIsLoading(true);

    try {
      // preparar datos del formulario
      const formData = new FormData();
      formData.append("jsessionid", enteredCode);
      formData.append("filename", ctx.saveas);
      formData.append("location", ctx.parse);
      formData.append("class-type", ctx.classParsing);
      formData.append("extension", ctx.extension);

      const apiUrl = process.env.REACT_APP_API_URL || "https://api.epicalendar.mier.info";
      const response = await fetch(`${apiUrl}/api/generate`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Error al generar el calendario");
      }

      // descargar el archivo
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = ctx.saveas + ctx.extension;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      ctx.saveNameHandler(DEFAULT_FILENAME);
      codeReset();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
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
            {error && (
              <React.Fragment>
                <p className={classes.error}>{error}</p>
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
          disabled={!formIsValid || isLoading}
          onClick={formSubmissionHandler}
        >
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          {isLoading ? "Generando..." : "Generar"}
        </button>
        <HeaderSettingsButton onClick={props.onShowSettings} />
      </div>
    </React.Fragment>
  );
};

export default Form;
