import React from "react";

const Confirm = ({ islogin }) => {
  return (
    <div className="Dashboard">
      <div className="confirmation" style={islogin ? { color: 'green' } : { color: 'red' }}>
        {islogin ? "You're logged in Successfully" : 'Login Failed'}
      </div>
    </div>
  );
};

export default Confirm;