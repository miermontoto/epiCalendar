import React from "react";
import Modal from "../UI/Modal";
import classes from "./Info.module.css";

// Settings component which contains the modal and the options
const Settings = (props) => {
  // Context to access the settings state

  return (
    <Modal onClose={props.onClose}>
      <div className={classes.overall}>
        <h1>Info</h1>
        <p> epiCalendar, un fork de <a href="https://github.com/Bimo99B9/autoUniCalendar" rel="noreferrer" target="_blank">autoUniCalendar</a>,
        hecho por <a href="https://mier.info" rel="noreferrer" target="_blank">Juan Mier</a> y
        <a href="https://github.com/JonathanAriass" rel="noreferrer" target="_blank"> Jonathan Arias</a>. </p>
        <p> Frontend hecho con React, backend con Flask. </p>
        <div className={classes.links}>
          <ul>
            <li>
              <img src="https://github.com/favicon.ico" alt="GitHub" width="16" height="16" />
              <a href="https://github.com/miermontoto/epiCalendar" rel="noreferrer" target="_blank">Repositorio de GitHub</a>
            </li>
            <li>
              <img src="https://mier.info/assets/favicon.svg" alt="JSESSION" width="16" height="16" />
              <a href="https://mier.info/epiCalendar" rel="noreferrer" target="_blank">¿Cómo obtener "JSESSION"?</a>
            </li>
            <li>
              <img src="https://uniovi.es/favicon.ico" alt="SIES" width="16" height="16" />
              <a href="https://sies.uniovi.es/serviciosacademicos" rel="noreferrer" target="_blank">SIES</a>
            </li>
          </ul>
        </div>
        <div className={classes.buttons}>
          <button className={classes["button--alt"]} onClick={props.onClose}>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            Close
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default Settings;
