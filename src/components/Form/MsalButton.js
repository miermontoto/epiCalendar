import React from "react";

import "./MsalButton.css";

import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../../authConfig";

function handlePopup(instance, type) {
    if (type === "login") {
        instance.loginPopup(loginRequest).catch(e => {
            console.error(e);
        });
    } else if (type === "logout") {
        instance.logoutPopup({
            postLogoutRedirectUri: "/",
            mainWindowRedirectUri: "/"
        });
    }
}


const MsalButton = (props) => {
    const { instance } = useMsal();

    return (
        <div className="msal-button">
            <button id="msal-but" onClick={() => handlePopup(instance, props.type)}>
                <div className="inline">
                    <i className="btn-microsoft"></i>{props.text}
                </div>
            </button>
        </div>
    );
};

export default MsalButton;