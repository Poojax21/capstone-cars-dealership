import React, { useState } from "react";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import Dealers from "./components/Dealers/Dealers";
import Login from "./components/Login/Login";
import Register from "./components/Register/Register";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [state, setState] = useState("");

  const handleLogin = (data) => {
    setLoggedIn(true);
    setUsername(data.userName);
  };

  return (
    <div className="app">
      <Header loggedIn={loggedIn} username={username} />
      <main className="container">
        <h1>Welcome to Cars Dealership</h1>
        <select value={state} onChange={(e) => setState(e.target.value)}>
          <option value="">All States</option>
          <option value="Kansas">Kansas</option>
          <option value="Texas">Texas</option>
          <option value="Illinois">Illinois</option>
        </select>
        <Dealers state={state} />
        {!loggedIn && <Login onLogin={handleLogin} />}
        <Register />
      </main>
      <Footer />
    </div>
  );
}

export default App;
