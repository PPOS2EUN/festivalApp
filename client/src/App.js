import {Route, Routes} from 'react-router-dom';
import React from "react";
import Form from "./Form";
import Welcome from "./welcome";
import FaceRecongnize from "./faceRecongnize";

function App() {

  return (
    <div className="App">
       <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/form" element={<Form/>} />
            <Route path="/welcome" element={<Welcome/>}/>
            <Route path="/face" element={<FaceRecongnize/>}/>
       </Routes>
    </div>
  );
}

function Home(){
  return <h2>Home</h2>
}
export default App;
