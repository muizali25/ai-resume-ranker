"use client";

import { useEffect, useState } from "react";

const API = "http://localhost:5000/api";
const MAX = 3;

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  return `${(bytes / 1024).toFixed(1)} KB`;
}

function fileExt(name) {
  const parts = name.split(".");
  return parts.length > 1 ? parts.pop().toUpperCase() : "FILE";
}

export default function Home() {
  const [resumes, setResumes] = useState([]);
  const [jobDescription, setJobDescription] = useState("");
  const [bestMatch, setBestMatch] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  async function loadResumes() {
    try {
      const res = await fetch(`${API}/resumes`);
      const data = await res.json();
      setResumes(data.resumes || []);
    } catch {
      setError("Cannot reach backend. Is it running on port 5000?");
    }
  }

  useEffect(() => {
    loadResumes();
  }, []);

  async function handleUpload() {
    setError("");
    if (!selectedFile) {
      setError("Please choose a resume file first.");
      return;
    }
    if (resumes.length >= MAX) {
      setError(`Maximum ${MAX} resumes allowed.`);
      return;
    }

    const form = new FormData();
    form.append("resume", selectedFile);

    setLoading(true);
    try {
      const res = await fetch(`${API}/upload`, { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Upload failed");
      } else {
        setResumes(data.resumes || []);
        setSelectedFile(null);
        setBestMatch("");
      }
    } catch {
      setError("Upload failed. Check backend connection.");
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(savedName) {
    setError("");
    try {
      const res = await fetch(`${API}/resumes/${encodeURIComponent(savedName)}`, {
        method: "DELETE",
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Delete failed");
      } else {
        setResumes(data.resumes || []);
        setBestMatch("");
      }
    } catch {
      setError("Delete failed.");
    }
  }

  async function handleAskAI() {
    setError("");
    setBestMatch("");

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }
    if (resumes.length === 0) {
      setError("Upload at least one resume first.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API}/rank`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jobDescription }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || data.details || "Ranking failed");
      } else {
        setBestMatch(data.bestMatch);
      }
    } catch {
      setError("Ask AI failed. Check backend and Gemini API key.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <h1>AI Resume Ranker</h1>
      <p className="subtitle">
        Upload up to {MAX} resumes, paste the job requirements, then ask AI to
        pick the best match.
      </p>

      {/* 1. Resume upload */}
      <section className="section">
        <h2>1. Upload Resume</h2>
        <div className="upload-row">
          <input
            type="file"
            accept=".pdf,.txt,.md"
            onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
            disabled={resumes.length >= MAX || loading}
          />
          <button
            onClick={handleUpload}
            disabled={resumes.length >= MAX || loading || !selectedFile}
          >
            Upload
          </button>
        </div>
        <p className="hint">
          PDF or TXT only. Max {MAX} files. ({resumes.length}/{MAX} used)
        </p>
      </section>

      {/* 2. Uploaded resumes info */}
      <section className="section">
        <h2>2. Uploaded Resumes</h2>
        {resumes.length === 0 ? (
          <p className="empty">No resumes uploaded yet.</p>
        ) : (
          <ul className="resume-list">
            {resumes.map((r) => (
              <li key={r.savedName} className="resume-item">
                <div className="resume-icon" title={r.originalName}>
                  {fileExt(r.originalName)}
                </div>
                <div className="resume-info">
                  <div className="name">{r.originalName}</div>
                  <div className="meta">{formatSize(r.size)}</div>
                </div>
                <button
                  className="secondary"
                  onClick={() => handleDelete(r.savedName)}
                  disabled={loading}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* 3. Job description + Ask AI */}
      <section className="section">
        <h2>3. Job Description</h2>
        <textarea
          placeholder="Paste job requirements here..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          disabled={loading}
        />
        <button onClick={handleAskAI} disabled={loading}>
          {loading ? "Asking AI..." : "Ask from AI"}
        </button>
      </section>

      {/* 4. Best match result */}
      <section className="section">
        <h2>4. Best Match</h2>
        {bestMatch ? (
          <div className="result-box">
            <div className="label">Highly matched resume</div>
            <div className="name">{bestMatch}</div>
          </div>
        ) : (
          <p className="empty">Result will appear here after Ask from AI.</p>
        )}
      </section>

      {error && <p className="error">{error}</p>}
    </main>
  );
}
