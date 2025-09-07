import React from "react";
import {Navbar} from "./components/Navbar/navbar.js";
import Home from "./pages/Home";

function App() {

  const elements = [
    "Home",
    "Dashboard",
    "Profile"];
  return (
    <div>
      <Navbar elements={elements}/>
    </div>
  );
}

export default App;
