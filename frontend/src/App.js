import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import ResumeUpload from "./ResumeUpload";
import JobMatch from "./JobMatch";

function App() {
  return (
    <Router>
      <div>
        <nav>
          <Link to="/">Upload Resume</Link> | 
          <Link to="/match">Find Matches</Link>
        </nav>

        <Routes>
          <Route path="/" element={<ResumeUpload />} />
          <Route path="/match" element={<JobMatch />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;