import  {useAuthStore}  from "../store/auth"; // import useAuthStore from the store directory
import axios from "./axios"; // import axios; axios = apiInstance()
import jwt_decode from "jwt-decode"; // import the jwt-decode library; decode JWT tokens
import Cookie from "js-cookie"; // import the Cookie library; store and retrieve Cookies
import Swal from "sweetalert2"; // import the SweetAlert2 library; send alerts to the user


/**
 * Logs the user in with an email and password. If the status is 200, the login is successful and the user is set with the access and refresh tokens.
 * If there is an error, the error message is returned.
 * @param {string} email - The user's email
 * @param {string} password - The user's password
 * @returns {Object} A Promise that resolves to an object with two properties: data and error.
 * If there is no error, data is the response from the API and error is null.
 * If there is an error, data is null and error is the error message.
 */
export const login = async (email, password) => { // login function asynchronously waits for a response from the API (Promise)
    try {
        const { data, status } = await axios.post("user/token", { email, password }); // get the response from the API; destructure the data and status from the response

        if (status === 200) { 

           setAuthUser(data.access, data.refresh) // if the status is 200, set the auth user with the access and refresh tokens
           alert("Login successful"); // alert the user that the login was successful
        }
        return { data, error: null } // if there is no error, return the data

    } catch (error) {
        console.log(error)
        return { data: null, error: error.response.data.detail || "Something went wrong" } // if there is an error, return the error message
    }
};

/**
 * Registers the user with the provided information. If the status is 200, the registration is successful.
 * If there is an error, the error message is returned.
 * @param {string} full_name - The user's full name
 * @param {string} email - The user's email
 * @param {string} password - The user's password
 * @param {string} password2 - The user's password repeated to check if it's correct
 * @returns {Object} A Promise that resolves to an object with two properties: data and error.
 * If there is no error, data is the response from the API and error is null.
 * If there is an error, data is null and error is the error message.
 */
export const register = async (full_name, email, password, password2) => { // register function asynchronously waits for a response from the API (Promise)
    try {
        const { data, status } = await axios.post("user/register/", { // get the response from the API; destructure the data and status from the response
            full_name,
            email,
            password,
            password2,
        });

        await login(email, password); // login the user with the email and password
        alert("Registration successful"); // alert the user that the registration was successful
        return { data, error: null } // if there is no error, return the data

    } catch (error) {
        console.log(error)
        return { data: null, error: error.response.data.detail || "Something went wrong" }

    }
}

/**
 * Logs the user out by performing the following actions:
 * - Removes the access and refresh tokens from Cookies.
 * - Sets the authenticated user state to null.
 * - Displays an alert to inform the user that the logout was successful.
 */
export const logout = () => {
    Cookie.remove("access_token"); // remove the access Cookie
    Cookie.remove("refresh_token"); // remove the refresh Cookie
    useAuthStore.getState().setUser(null); // set the auth user to null

    alert("Logout successful"); // alert the user that the logout was successful
}

/**
 * Checks if the access token is expired and if so, gets a new access token from the refresh token.
 * If the access token is not expired, sets the auth user with the access and refresh tokens.
 * If the access or refresh token is null, does nothing.
 */
export const setUser = async () => {
    const access_token = Cookie.get("access_token"); // get the access token from Cookies
    const refresh_token = Cookie.get("refresh_token"); // get the refresh token from Cookies

    if (!access_token || !refresh_token) { // if the access or refresh token is null
        return;
    }
    if (isAccessTokenExpired(access_token)) { // if the access token is expired
        const res = getRefreshToken(refresh_token); // get the refresh token
        setAuthUser(res.access, res.refresh); // set the auth user with the access and refresh tokens
    } else {
        setAuthUser(access_token, refresh_token); // set the auth user with the access and refresh tokens
    }
    }


/**
 * Sets the auth user with the access and refresh tokens.
 * If the access token is not expired, sets the auth user with the access and refresh tokens.
 * If the access or refresh token is null, does nothing.
 * @param {string} access_token - The access token
 * @param {string} refresh_token - The refresh token
 */
export const setAuthUser = (access_token, refresh_token) => {
    Cookie.set("access_token", access_token, { expires: 1 , secure: true}); // set the access token in Cookies; expires in 1 hour
    Cookie.set("refresh_token", refresh_token, { expires: 7 , secure: true}); // set the refresh token in Cookies; expires in 7 days

    const user = jwt_decode(access_token) ?? null; // decode the access token

    if (user) { // if the user is not null
        useAuthStore.getState().setUser(user); // set the auth user
    } else {
        useAuthStore.getState().setLoading(false); // set the auth user to null
    }
}


export const getRefreshToken = async () => {
    const refresh_token = Cookie.get("refresh_token"); // get the refresh token from Cookies
    const res = await axios.post("user/token/refresh/", { refresh: refresh_token }); // get the response from the API
    return res.data;
}

/**
 * Checks if the provided access token is expired.
 *
 * This function decodes the given JWT access token to extract
 * its expiration time and compares it to the current time.
 *
 * @param {string} access_token - The JWT access token to be checked.
 * @returns {boolean} - Returns true if the token is expired, otherwise false.
 */
export const isAccessTokenExpired = (access_token) => {
    try {
        const decoded = jwt_decode(access_token); // decode the access token
        return decoded.exp < Date.now() / 1000; // check if the access token is expired
    } catch (error) {
        console.log(error);
        return true;
    }


}

/*
 jwt_decode(access_token) = {
    "id": 1,
    "username": "admin",
    "first_name": "admin",
    "last_name": "admin",
    "email": "2P5oJ@example.com",
    exp: 1680000000,
    iat: 1680000000
 }
*/