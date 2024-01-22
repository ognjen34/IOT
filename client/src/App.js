import logo from "./logo.svg";
import "./App.css";
import axios from "axios";
import { React, useEffect } from "react";
import Navbar from "./Components/Navbar";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  Outlet,
} from "react-router-dom";
import PI1 from "./Pages/Pi1";
import PI3 from "./Pages/Pi3";
import PI2 from "./Pages/Pi2";

function App() {
  

  return (
    <div className="App">
      <Navbar />

      <Routes>
        <Route path="/" element={<PI1 />} />
        <Route path="/pi1" element={<PI1 />} />
        <Route path="/pi2" element={<PI2 />} />
        <Route path="/pi3" element={<PI3 />} />
      </Routes>

      <Outlet style={{ flex: 1, overflowY: "auto" }}></Outlet>
    </div>
  );
}

export default App;
