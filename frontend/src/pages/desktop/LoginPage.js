import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { authenticateUser } from "../../actions/authActions";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import EyeIcon from "../../assets/icon/eye.svg";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await dispatch(authenticateUser({ email, password }));
      navigate("/dashboard");
    } catch (err) {
      const errorMsg =
        err.response?.status === 401
          ? "Invalid credentials. Please check your email or password."
          : "Login failed. Please try again later.";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-height">
      <Navbar />
      <div className="login-page">
        <div className="login-container">
          <h2>Login</h2>
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                placeholder="Enter your email"
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
                  placeholder="Enter your password"
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
            <button type="submit" className="login-button" disabled={loading}>
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>
          <p>
            Don't have an account?{" "}
            <span onClick={() => navigate("/register")} className="link">
              Register
            </span>
          </p>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default LoginPage;