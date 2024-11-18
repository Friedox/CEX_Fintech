import { LOGIN_SUCCESS, LOGOUT_SUCCESS } from '../actions/authActions'; // Import action types

const initialState = {
  isAuthenticated: false,
  session_id: null,
  user: null, // Store user details
};

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOGIN_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        session_id: action.payload.session_id,
        user: action.payload.user, // Store full user details, including ID
      };
    case LOGOUT_SUCCESS:
      return {
        ...state,
        isAuthenticated: false,
        session_id: null,
        user: null,
      };
    default:
      return state;
  }
};

export default authReducer;