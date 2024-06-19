import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import React from "react";

// Renders the App component
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
