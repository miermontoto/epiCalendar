import React from "react";

import "./SignOutButton.css";

import { useMsal } from "@azure/msal-react";

export const SignOutButton = () => {
    const { instance } = useMsal();

    const handleLogout = () => {
        instance.logoutPopup({
            postLogoutRedirectUri: "/",
            mainWindowRedirectUri: "/"
        });
    }

    return (
        <div className="msal-button">
            <button id="msal-but" onClick={() => handleLogout(instance)}>
                <div className="inline">
                    <i className="btn-microsoft"></i>Sign out
                </div>
            </button>
        </div>
    );
};