import axios from "axios";
import {getRefreshToken, isAccessTokenExpired, setAuthUser} from "./auth";
import { API_BASE_URL } from "./constant";
import Cookies from "js-cookie";

/**
 * Custom hook to create an axios instance with token-based authentication.
 *
 * This hook sets up an axios instance with the API base URL and includes the
 * access token from cookies in the Authorization header for each request. It
 * also intercepts requests to refresh the access token if it is expired, using
 * the refresh token from cookies.
 *
 * @returns {Object} - An axios instance configured with token-based authentication.
 */
const useAxios = () => {
    const accessToken = Cookies.get("access_token"); // get the access token from Cookies
    const refreshToken = Cookies.get("refresh_token"); // get the refresh token from Cookies

    const axiosInstance = axios.create({// create an axios instance
        baseURL: API_BASE_URL,
        headers: {
            Authorization: `Bearer ${accessToken}`, // set the Authorization header with the access token
        },
    });

    axiosInstance.interceptors.request.use(async (req) => {
        if (!isAccessTokenExpired) { // if the access token is not expired
            return req;
        }

        const res = await getRefreshToken(refreshToken); // get the refresh token
        setAuthUser(res.access, res.refresh); // set the auth user with the access and refresh tokens
        req.headers.Authorization = `Bearer ${res.data?.access}`; // set the Authorization header with the access token

        return req;
    });

    return axiosInstance;
};

export default useAxios;