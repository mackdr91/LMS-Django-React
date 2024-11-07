import { Navigate } from "react-router-dom";
import  {useAuthStore}  from "../store/auth";

    /**
     * PrivateRoute is a functional component that takes a children prop
     * and renders the children only if the user is logged in.
     * If the user is not logged in, it navigates to the login page.
     * @param {Object} props - component props
     * @param {ReactNode} props.children - the children to render
     * @returns {ReactNode} - the rendered children or a Navigate component
     */
const PrivateRoute = ({ children }) => { // PrivateRoute is a functional component that takes a children prop
    const loggedIn = useAuthStore(state => state.isLoggedIn)(); // get the auth user; () making use of zustand

    /*
     * Navigate to the login page if the user is not logged in
     * Otherwise, render the children
     */
    return loggedIn ? <>{children}</>: <Navigate to="/login" />

}

export default PrivateRoute

/*

<PrivateRoute>
    <Home />
    <Dashboard />
</PrivateRoute>

*/