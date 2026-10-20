import React, { useState } from "react";

const Login = ({ onLogin }) => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const body = new URLSearchParams({ userName, password });
    fetch("/djangoapp/login", { method: "POST", body })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === 200) {
          setMessage("Login successful");
          if (onLogin) onLogin(data);
        } else {
          setMessage(data.message || "Invalid credentials");
        }
      })
      .catch(() => setMessage("Login failed"));
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <label>
        Username
        <input type="text" value={userName} onChange={(e) => setUserName(e.target.value)} required />
      </label>
      <label>
        Password
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      </label>
      <button type="submit">Login</button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default Login;
