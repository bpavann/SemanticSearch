
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./Home";
import About from "./About";
import Contact from "./Contact";
import NavBar from "./Navbar";




function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <NavBar />
        <div className="header">
          <div className="logo-container">
            <div className="logo" onClick={handleClick}></div>
          </div>
            <div className="company-name" onClick={handleClick}>
              <h1>Ellenox</h1>
            </div>
        </div>
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/home" element={<Home />}></Route>
          <Route path="/about" element={<About />}></Route>
          <Route path="/contact" element={<Contact />}></Route>
        </Routes>
      </BrowserRouter>
    </div>
    
  );
  
}
const handleClick = () => {
  window.open('https://www.ellenox.com/', '_blank');
}

export default App;
