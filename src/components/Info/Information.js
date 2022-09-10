import React, { useState } from "react";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../../authConfig";
import { useIsAuthenticated } from "@azure/msal-react";
import { ProfileData } from "./ProfileData";
import { callMsGraph } from "../../graph";



// export const Information = () => {
//     return (<>
//         <h1>LOGED IN!</h1>
//         <SignOutButton />
//     </>);
// };



/**
 * Renders information about the signed-in user or a button to retrieve data about the user
 */
export const Information = () => {
    // const isAuthenticated = useIsAuthenticated();
    const { instance, accounts } = useMsal();
    const [graphData, setGraphData] = useState(null);

    function RequestProfileData() {
        // Silently acquires an access token which is then attached to a request for MS Graph data
        instance.acquireTokenSilent({
            ...loginRequest,
            account: accounts[0]
        }).then((response) => {
            callMsGraph(response.accessToken).then(response => setGraphData(response));
        });
    }

    return (
        <>
            <h5 className="card-title">Welcome {accounts[0].name}</h5>
            {graphData ?
                <ProfileData graphData={graphData} />
                :
                <button onClick={RequestProfileData}>Request Profile Information</button>
            }

        </>
    );
};