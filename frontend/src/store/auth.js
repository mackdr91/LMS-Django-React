import { create } from "zustand"; // is a function that creates a store
import { mountStoreDevtool } from "simple-zustand-devtools"; // is a function that sets up a debugging tool for a store

// store for authentication; get user information
const useAuthStore = create((set, get) => ({
  allUserData: null, // user not logged in
  loading: false, // loading state

  user: () => ({
    // The ?. syntax is used to safely access the user_id
    // and username properties of allUserData,
    // in case they are null or undefined.
    user_id: get().allUserData?.user_id,
    username: get().allUserData?.username, // username
  }),

  isLoading: () => ({
    isLoading: true
  }),

  setUser: (user) => set({ allUserData: user }), // set user

  // set loading state
  setLoading: (isLoading) => set({ loading: isLoading }),

  isLoggedIn: () => !!get().allUserData, // check if user is logged in
  // The !! operator is a double negation, which converts the result to a boolean value:
  // If allUserData is truthy (i.e., not null or undefined), !! will return true.
  // If allUserData is falsy (i.e., null or undefined), !! will return false.
}));

// devtools
// checks if the application is running in a development environment (DEV) and,
// if so, mounts a store devtool for debugging purposes.
if (import.meta.env.DEV) { // import.meta.env.DEV is a way to access environment variables in modern JavaScript.
  mountStoreDevtool("Auth Store", useAuthStore);
}

export { useAuthStore }; // export store { useAuthStore, <other stores> } to export multiple stores
