import React from "react";

import "./MsalButton.css";

import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../../authConfig";

function handleLogin(instance) {
    instance.loginPopup(loginRequest).catch(e => {
        console.error(e);
    });
}


export const MsalButton = () => {
    const { instance } = useMsal();

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