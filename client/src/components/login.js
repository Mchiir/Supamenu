import React from 'react'

const Login = () =>{
    return(
        <div className="login">
            <div className='left-header'>
                <span style={{ color:'black' }}>Supa</span>
                <span style={{ color:'white' }}>Menu</span>
            </div>
            <div className='login-box'>
                <form>
                    <h4>Welcome</h4>
                    <h2>Login to Supamenu</h2>
                    <p>Enter your email and password below</p>
                    <div className='inputs'>
                    <input type="email" id='email' placeholder='Email...'/>
                    <input type="password" id='password' placeholder='Password...'/>
                    <input type="submit" value={'Login'}/>
                    </div>
                    <div className='guidance'>
                        <p>
                            Don't have an account? <a href="#">Sign up</a>
                            <br />  <br /> Forgot your password/login <a href="#">RESET</a>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default Login