import React, { useState } from "react";
import "./Register.css";
import Header from "../Header/Header";

const Register = () => {
  const [form, setForm] = useState({
    userName: "",
    firstName: "",
    lastName: "",
    email: "",
    password: ""
  });

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch("/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });

      const result = await response.json();

      if (response.ok && result.status === "Registered") {
        alert("Registration successful.");
        window.location.href = "/";
      } else {
        alert(result.message || "Registration unsuccessful.");
      }
    } catch (error) {
      alert("Unable to connect to the registration service.");
    }
  };

  return (
    <div>
      <Header />
      <div className="register_panel">
        <h1>Sign Up</h1>
        <form onSubmit={handleSubmit}>
          <label>Username</label>
          <input name="userName" type="text" required onChange={handleChange} />

          <label>First Name</label>
          <input name="firstName" type="text" required onChange={handleChange} />

          <label>Last Name</label>
          <input name="lastName" type="text" required onChange={handleChange} />

          <label>Email</label>
          <input name="email" type="email" required onChange={handleChange} />

          <label>Password</label>
          <input name="password" type="password" required onChange={handleChange} />

          <button type="submit" className="action_button">Register</button>
        </form>
      </div>
    </div>
  );
};

export default Register;
