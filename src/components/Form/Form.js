import React, { useEffect } from 'react';
import './Form.css';

export const Form = (props) => {

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
            <div className="form-container cookies">
                <form action="" method="post">
                    <h1>Cookies</h1>
                    <span id="cookies-span">Introduce tu cookie de sesión.</span>
                    <div className="floating-input">
                        <label>
                            <input type="text" id="jsession" required />
                            <span className="floating-label">JSession</span>
                        </label>
                    </div>
                    <a href="https://bimo99b9.github.io/scripts-autounicalendar/#" target="_blank" rel="noopener noreferrer">¿Necesitas ayuda?</a>
                    <button>DESCARGAR</button>
                </form>
            </div>
            <div className="form-container signin">
                <form action="">
                    <h1>Descargar usando credenciales</h1>
                    <p> Usa tus credenciales para tramitar la solicitud y descargar el calendario.</p>
                    <button disabled="">Iniciar sesion</button>
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