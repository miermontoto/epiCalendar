import React from "react";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../../authConfig";

function handleLogin(instance) {
    instance.loginPopup(loginRequest).catch(e => {
        console.error(e);
    });
}

const SignInButton = () => {
    const { instance } = useMsal();

    return <button onClick={() => handleLogin(instance)}>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        Sign In
    </button>;
}

export default SignInButton;