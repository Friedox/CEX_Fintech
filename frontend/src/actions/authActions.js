import authService from '../services/authService';
import Cookies from 'js-cookie';

// Action Types
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS';
export const LOGOUT_SUCCESS = 'LOGOUT_SUCCESS';

export const authenticateUser = ({ email, password }) => async (dispatch) => {
  try {
    console.log("Attempting login...");
    const loginResponse = await authService.login({ email, password });

    // Access session_id directly from the login response
    const session_id = loginResponse.data?.detail?.session_id;
    if (!session_id) {
      throw new Error("Session ID not found in login response.");
    }
    Cookies.set('session_id', session_id, { path: '/' });

    // Fetch user details
    const userDetailsResponse = await authService.getUserDetails();
    const userDetails = userDetailsResponse?.detail; // Access nested user details
    if (!userDetails || !userDetails.id) {
      throw new Error("User details not found in response.");
    }
    Cookies.set('user_id', userDetails.id, { path: '/' });

    // Dispatch login success
    dispatch({
      type: LOGIN_SUCCESS,
      payload: { session_id, user: userDetails },
    });

    console.log("Login successful with user ID:", userDetails.id);
  } catch (error) {
    console.error("Authentication failed:", error.message || error);
    throw error;
  }
};

export const registerUser = ({ email, password }) => async (dispatch) => {
  try {
    console.log("Attempting registration...");
    await authService.register({ email, password });

    console.log("Registration successful.");
    // Optionally, trigger login after registration
    // await dispatch(authenticateUser({ email, password }));
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const logout = () => (dispatch) => {
  try {
    console.log("Logging out...");

    // Remove session_id and user_id from cookies
    Cookies.remove('session_id', { path: '/' });
    Cookies.remove('user_id', { path: '/' });

    // Dispatch logout success
    dispatch({ type: LOGOUT_SUCCESS });

    console.log("Logout successful.");
  } catch (error) {
    console.error("Error during logout:", error);
    throw error;
  }
};