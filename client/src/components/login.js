import React, { useEffect, useState } from 'react';

const Login = ({ setIslogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${process.env.REACT_APP_SERVERURL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.status === 200) {
        console.log("Login successful!");
        setIslogin(true); // Update the islogin state to true if login is successful
      } else {
        console.error("Login failed!");
        setIslogin(false); // Update the islogin state to false if login fails
      }
    } catch (error) {
      console.error("Error during login:", error);
      setIslogin(false); // Update the islogin state to false in case of an error
    }
  };

  return (
    <div className="login">
      <div className='left-header'>
        <span style={{ color: 'black' }}>Supa</span>
        <span style={{ color: 'white' }}>Menu</span>
      </div>
      <div className='login-box'>
        <form onSubmit={handleSubmit}>
          <h4>Welcome</h4>
          <h2>Login to Supamenu</h2>
          <p>Enter your email and password below</p>
          <div className='inputs'>
            <input
              type="email"
              id='email'
              placeholder='Email...'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              id='password'
              placeholder='Password...'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <input type="submit" value={'Login'} />
          </div>
          <div className='guidance'>
            <p>
              Don't have an account? <a href="#">Sign up</a>
              <br /> <br /> Forgot your password/login <a href="#">RESET</a>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;