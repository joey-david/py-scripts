import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom'
import { useEffect, useRef } from 'react'
import { Home } from './components/pages/home'
import { Header } from './components/header'
import { Footer } from './components/footer'
import { Analysis } from './components/pages/analysis'
import './App.css'

const GradientBackground = () => {
  const gradientRef = useRef<HTMLDivElement>(null)
  const location = useLocation()

  useEffect(() => {
    if (!gradientRef.current) return

    switch (location.pathname) {
      case '/':
        gradientRef.current.style.setProperty('--size', '30rem')
        gradientRef.current.style.setProperty('--speed', '20s')
        break
      case '/analysis':
        gradientRef.current.style.setProperty('--size', '50rem')
        gradientRef.current.style.setProperty('--speed', '40s')
        break
      default:
        gradientRef.current.style.setProperty('--size', '70rem')
        break
    }
  }, [location])

  return <div className="gradient fixed" ref={gradientRef} />
}

function App() {
  return (
    <Router>
      <div className='background-container'>
        <GradientBackground />
      </div>
      <div id="root">
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