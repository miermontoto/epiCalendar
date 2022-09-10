import React from "react";

import "./SignInButton.css";

import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../../authConfig";

function handleLogin(instance) {
    instance.loginPopup(loginRequest).catch(e => {
        console.error(e);
    });
    // console.log(instance);
}


const SignInButton = () => {
    const { instance } = useMsal();

    // const handleLogin = () => {
    //     instance.loginPopup(loginRequest).catch(e => {
    //         console.error(e);
    //     });
    // };


    return (
        <div className="msal-button">
            <button id="msal-but" onClick={() => handleLogin(instance)}>
                <div className="inline">
                    <i className="btn-microsoft"></i>Sign in
                </div>
            </button>
        </div>
    );
};

export default SignInButton;