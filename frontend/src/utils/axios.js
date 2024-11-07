import axios from "axios";
import { API_BASE_URL } from "./constant"; // Import the API base URL

/*
Headers:
"Content-Type": "application/json",
"Accept": "application/json",
*/

const apiInstance = axios.create({
    baseURL: API_BASE_URL, // API base URL
    timeout: 10000, // Request timeout 10s
    headers: { // Set the content type header
        "Content-Type": "application/json", // Set the Content-Type header: JSON
        "Accept": "application/json", // Set the Accept header: JSON
    },
});

export default apiInstance;

// apiInstance.get('<url>')