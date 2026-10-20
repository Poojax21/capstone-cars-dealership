import React from "react";

const Header = ({ loggedIn, username }) => {
  return (
    <nav className="navbar">
      <div className="nav-brand">Cars Dealership</div>
      <ul className="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="/about">About Us</a></li>
        <li><a href="/contact">Contact Us</a></li>
        {loggedIn ? (
          <>
            <li className="nav-user">Logged in as <strong>{username}</strong></li>
            <li><a href="/logout">Logout</a></li>
          </>
        ) : (
          <>
            <li><a href="/login">Login</a></li>
            <li><a href="/register">Sign Up</a></li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Header;
