import "./login.css";
import { useState } from "react";
import {login} from "../../services/userApi"

export function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try{
      const user = await login(email);
      localStorage.setItem("user", JSON.stringify(user));

      window.location.href = "/dashboard";
    } catch (err) {
      alert("Error logging in. Please try again later.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Login</h2>
        <form>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="login-btn"
            onClick={handleLogin}
          >
            Login
          </button>
        </form>
        <p className="signup-text">
          Don’t have an account? <a href="/register">Register</a>
        </p>
      </div>
    </div>
  );
}
