import React from "react";

import "./MsalButton.css";

export const MsalButton = () => {
    return (
        <div className="msal-button">
            <button id="msal-but">
                <div className="inline">
                    <i className="btn-microsoft"></i>Sign in
                </div>
            </button>
        </div>
    );
};