import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Home } from './components/pages/home'
import { Header } from './components/header'
import { Footer } from './components/footer'
import { Analysis } from './components/pages/analysis'
import './App.css'

function App() {
  return (
    <Router>
      <div id="root">
        <div className="background-container">
          <div className="gradient" />
        </div>
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analysis" element={<Analysis />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App