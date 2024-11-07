import {useEffect, useState} from "react";
import { setUser } from "../utils/auth";

/**
 * MainWrapper is a functional component that initializes and manages the loading state
 * while setting the authenticated user with access and refresh tokens. It uses the
 * useEffect hook to execute the handler function when the component mounts, which
 * sets the loading state to true, invokes the `setUser` function to update user
 * authentication details, and then sets the loading state to false once completed.
 *
 * @param {Object} props - The component properties.
 * @param {ReactNode} props.children - The child components to be rendered within
 * the MainWrapper.
 */
const MainWrapper = ({ children }) => {
    const [loading, setLoading] = useState(true); // set loading state

    useEffect(() => {
        /**
         * Handler to set the auth user with the access and refresh tokens.
         * It sets the loading state to true, sets the auth user with the access and refresh tokens,
         * and then sets the loading state to false.
         */
        const handler = async() => {
            setLoading(true); // set loading state

            await setUser(); // set the auth user

            setLoading(false); // set loading state
        };

        handler();
    }, []); // run the handler when the component mounts


    /* if loading is true, return null, otherwise return children */
    return <>{loading ? null : children}</>;

}
export default MainWrapper;