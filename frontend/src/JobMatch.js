import React, { useState } from "react";
import axios from "axios";

const JobMatch = () => {
  const [jobDescription, setJobDescription] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

  const handleMatch = async () => {
    if (!jobDescription) {
      setError("Please enter a job description.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/match/", {
        job_description: jobDescription,
        top_n: 5,
      });

      setResults(response.data.matched_resumes);
      setError("");
    } catch (error) {
      setError("Error fetching results. Try again.");
    }
  };

  return (
    <div>
      <h2>Find Best Resumes</h2>
      <textarea
        rows="4"
        placeholder="Enter job description..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />
      <button onClick={handleMatch}>Find Matches</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {results.map((resume) => (
          <li key={resume.id}>
            <strong>{resume.filename}</strong> - Score: {resume.score.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default JobMatch;