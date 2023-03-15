import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './components/Navbar';
import Home from './components/Home';
import About from './components/About';
import ViewSubscription from './components/ViewSubscription';
import { useState } from 'react';
import { useRef } from 'react';
import Test from './components/Test';

function App() {
  return (
    <>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route exact path="/" element={<><Home/></>} />
          <Route exact path="/view/subscription" element={<><ViewSubscription/></>} />
          <Route exact path="/about" element={<><About /></>} />
          <Route exact path="/test" element={<><Test /></>} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
