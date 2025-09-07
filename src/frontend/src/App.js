import React from "react";
import {Navbar} from "./components/Navbar/navbar.js";
import Home from "./pages/Home";
import LoginPage from "./pages/Login/Login.js";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {

  const elements = [
    "Home",
    "Dashboard",
    "Profile",
    "Login"
  ];

  return (
    <Router>
      <Navbar elements = {elements}/>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </Router>
  );
}

export default App;
