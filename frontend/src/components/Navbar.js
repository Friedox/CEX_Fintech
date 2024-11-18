import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../actions/authActions"
import Profile from "../assets/icon/profile.svg";

const Navbar = () => {
  const dispatch = useDispatch();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const { isAuthenticated, user } = useSelector((state) => state.auth);

  const commonLinks = [
    { path: "/", label: "Home" },
    { path: "/market", label: "Market" },
    { path: "/features", label: "Features" },
    { path: "/faq", label: "FAQ" },
  ];

  const authLinks = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/crane", label: "Crane (Faucet)" },
    { path: "/transfer", label: "Transfer" },
    { path: "/create-token", label: "Create Token" },
    { path: "/trade", label: "Trade" },
  ];

  const handleLogout = () => {
    dispatch(logout());
    setIsMenuOpen(false);
  };

  return (
    <div className="navbar-wrapper">
      <nav className="navbar">
        <div className="navbar-logo-container">
          <h1>
            <Link to="/" className="navbar-logo">
              Crypto CEX / MATRASURY
            </Link>
          </h1>
        </div>
        <div className="navbar-links-container">
          <ul>
            {/* Common Links */}
            {commonLinks.map(({ path, label }) => (
              <li key={path}>
                <Link
                  to={path}
                  className={location.pathname === path ? "active" : ""}
                  aria-label={label}
                >
                  {label}
                </Link>
              </li>
            ))}

            {/* Authenticated User Links */}
            {isAuthenticated &&
              authLinks.map(({ path, label }) => (
                <li key={path}>
                  <Link
                    to={path}
                    className={location.pathname === path ? "active" : ""}
                    aria-label={label}
                  >
                    {label}
                  </Link>
                </li>
              ))}

            {/* Profile or Auth Links */}
            {isAuthenticated ? (
              <li
                className="profile-container"
                onMouseEnter={() => setIsMenuOpen(true)}
                onMouseLeave={() => setIsMenuOpen(false)}
              >
                <div className="profile-icon">
                  <img
                    src={Profile}
                    alt="Profile"
                    className="profile-image"
                    aria-label="User Profile"
                  />
                  <span>{user?.username || "Profile"}</span>
                </div>
                {isMenuOpen && (
                  <div className="dropdown-menu dropdown-menu-animated">
                    <Link to="/dashboard" onClick={() => setIsMenuOpen(false)}>
                      Dashboard
                    </Link>
                    <Link to="/settings" onClick={() => setIsMenuOpen(false)}>
                      Settings
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="logout-button"
                      aria-label="Logout"
                    >
                      Logout
                    </button>
                  </div>
                )}
              </li>
            ) : (
              <>
                <li>
                  <Link
                    to="/login"
                    className={location.pathname === "/login" ? "active" : ""}
                    aria-label="Login"
                  >
                    Login
                  </Link>
                </li>
                <li>
                  <Link
                    to="/register"
                    className={location.pathname === "/register" ? "active" : ""}
                    aria-label="Register"
                  >
                    Register
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </nav>
    </div>
  );
};

export default Navbar;