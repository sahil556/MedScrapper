import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './components/Navbar';
import Home from './components/Home';
import About from './components/About';
import Search from './components/Search';
import ViewSubscription from './components/ViewSubscription';
import { useState } from 'react';
import { useRef } from 'react';

function App() {
  return (
    <>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route exact path="/" element={<><Home/></>} />
          <Route exact path="/view/subscription" element={<><ViewSubscription/></>} />
          <Route exact path="/about" element={<><About /></>} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
