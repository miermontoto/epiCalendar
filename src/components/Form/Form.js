import React, { useEffect } from 'react';
import './Form.css';

import useInput from "../../hooks/use-input";
import SettingsContext from "../../store/settings-context";

import { MsalButton } from './MsalButton';

import {
    DEFAULT_FILENAME,
    // DEFAULT_UNIVERSITY,
} from "../../store/settings-context";

export const Form = (props) => {
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
        // ctx.check(DEFAULT_UNIVERSITY);
        codeReset();
    };

    // const idButton = `"form-container cookies" ${codeHasError ? " invalid" : ""}`;
    // console.log(idButton);
    const idButton = "form-container cookies" + (codeHasError ? " invalid" : "");
    console.log(formIsValid);

    useEffect(() => {
        const cookiesButton = document.getElementById('cookies-sign');
        const signInButton = document.getElementById('signIn');
        const container = document.getElementById('container');

        signInButton.addEventListener('click', () => {
            container.classList.add("right-panel-active");
        });

        cookiesButton.addEventListener('click', () => {
            container.classList.remove("right-panel-active");
        });
    }, []);


    return (<>
        <h1 id="title">autoUniCalendar: Descarga tu calendario de Uniovi.</h1>
        <div id="container" className="container">
            {/* <div className="form-container cookies"> */}
            <div className={idButton} >
                <form id="form" method="post" onSubmit={formSubmissionHandler}>
                    <h1>Cookies</h1>
                    <span id="cookies-span">Introduce tu cookie de sesión.</span>
                    <div className="floating-input">
                        <label>
                            <input type="text" name="jsessionid" id="jsessionid" required onChange={codeChangeHandler}
                                onBlur={codeBlurHandler}
                                value={enteredCode} />
                            <span className="floating-label">JSession</span>
                        </label>
                    </div>
                    <a href="https://bimo99b9.github.io/scripts-autounicalendar/#" target="_blank" rel="noopener noreferrer">¿Necesitas ayuda?</a>
                    <button disabled={!formIsValid} onClick={formSubmissionHandler}>DESCARGAR</button>
                    <div>
                        <input type="hidden" name="filename" value={ctx.saveas} />
                    </div>
                    <div>
                        <input type="hidden" name="location" value={ctx.parse} />
                    </div>
                    <div>
                        <input type="hidden" name="class-type" value={ctx.classParsing} />
                    </div>
                    <div>
                        <input type="hidden" name="links" value={ctx.links} />
                    </div>
                    <div>
                        <input type="hidden" name="extension" value={ctx.extension} />
                    </div>
                </form>
            </div>
            <div className="form-container signin">
                <form action="">
                    <h1>Descargar usando credenciales</h1>
                    <p> Usa tus credenciales para tramitar la solicitud y descargar el calendario.</p>
                    {/* <button disabled="">Sign in</button> */}
                    <MsalButton />
                </form>
            </div>
            <div className="overlay-container">
                <div className="overlay">
                    <div className="overlay-panel overlay-left">
                        <h1>Descargar usando cookie.</h1>
                        <p>Puedes descargar el calendario usando una cookie de sesión, haciendo click aquí.</p>
                        <button id="cookies-sign" className="ghost">Usar cookie</button>
                    </div>
                    <div className="overlay-panel overlay-right">
                        <h1>Descargar usando credenciales.</h1>
                        <p>
                            Si lo prefieres, puedes usar tus credenciales en lugar de tus cookies de sesión para descargar el calendario.
                        </p>
                        <button id="signIn" className="ghost" >Usar crendeciales</button>
                    </div>
                </div>
            </div>
        </div >
        <div className="settings-button">
            <button onClick={props.onShowSettings}>Opciones</button>
        </div>
    </>);
};