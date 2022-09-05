import React from "react";
import { useMsal } from "@azure/msal-react";


/**
 * Renders a button which, when selected, will open a popup for logout
 */
export const SignOutButton = () => {
    const { instance } = useMsal();

    const handleLogout = async () => {
        await instance.logoutPopup({
            postLogoutRedirectUri: "/",
            mainWindowRedirectUri: "/"
        });
    }

    return (
        <button onClick={() => handleLogout(instance)}>Sign out using Popup</button>
    );
}