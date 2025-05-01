import { useState } from "react";
import "terminal.css";

function App() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [jwt, setJwt] = useState("");
  const [error, setError] = useState("");

  // Handle form input changes
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setJwt("");

    try {
      const response = await fetch("https://YOUR_LAMBDA_ENDPOINT", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error("Invalid credentials or server error.");
      }

      const data = await response.json();
      setJwt(data.token || "No token returned");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="App terminal">
      <h1>Request JWT from Lambda</h1>
      <div className="terminal-card">
        <header>Login</header>
        <form onSubmit={handleSubmit}>
          <fieldset>
            <legend>Enter Credentials</legend>
            <div>
              <label>
                Username:
                <input
                  type="text"
                  name="username"
                  value={form.username}
                  onChange={handleChange}
                  required
                />
              </label>
            </div>
            <div>
              <label>
                Password:
                <input
                  type="password"
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  required
                />
              </label>
            </div>
            <button type="submit">Get JWT</button>
          </fieldset>
        </form>
        {jwt && (
          <div className="terminal-alert terminal-alert-success">
            <strong>JWT:</strong> <code>{jwt}</code>
          </div>
        )}
        {error && (
          <div className="terminal-alert terminal-alert-error">{error}</div>
        )}
      </div>
    </div>
  );
}

export default App;
