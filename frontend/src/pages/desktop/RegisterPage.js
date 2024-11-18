import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { registerUser } from '../../actions/authActions';
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import EyeIcon from "../../assets/icon/eye.svg";

const RegisterPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    console.log("Registration attempt with email:", email);

    try {
      await dispatch(registerUser({ email, password }));
      console.log("Registration successful, redirecting...");
      navigate("/");
    } catch (err) {
      console.error("Registration error:", err);
      if (err.response?.status === 400) {
        setError("A user with this email already exists.");
      } else {
        setError("Registration failed. Please try again.");
      }
    }
  };

  return (
    <div className="full-height">
      <Navbar />
      <div className="register-page">
        <div className="register-container">
          <h2>Create Your Account</h2>
          <form onSubmit={handleRegister}>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <div className="password-input-container">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <img
                  src={EyeIcon}
                  alt="Toggle Password Visibility"
                  className="password-toggle"
                  onClick={() => setShowPassword((prev) => !prev)}
                />
              </div>
            </div>
            {error && <p className="error">{error}</p>}
            <button type="submit" className="register-button">
              Sign Up
            </button>
          </form>
          <p>
            Already have an account?{" "}
            <span onClick={() => navigate("/login")} className="link">
              Log In
            </span>
          </p>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default RegisterPage;