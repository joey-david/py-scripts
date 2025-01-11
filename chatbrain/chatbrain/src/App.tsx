// filepath: /home/joey/Projects/py-scripts/chatbrain/chatbrain/src/App.tsx
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Home } from './components/pages/home'
import { Header } from './components/header'
import { Footer } from './components/footer'
import { Analysis } from './components/pages/analysis'
import './App.css'

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analysis" element={<Analysis />} />
      </Routes>
      <Footer />
    </Router>
  )
}

export default App