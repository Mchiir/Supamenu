import React, { useState } from "react";
import Confirm from "./components/Confirm";
import Login from "./components/login";

function App() {
  const [islogin, setIslogin] = useState(false);

  return (
    <div className="App">
      {islogin ? <Confirm islogin={islogin} /> : <Login setIslogin={setIslogin} />}
    </div>
  );
}

export default App;