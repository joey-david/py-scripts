import { useState } from 'react'
import { Hero } from './components/ui/animated-hero'
import { Footer } from './components/footer'
import ChatbrainLogo from "./components/ChatbrainLogo"
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1 className="flex items-center justify-center gap-2"><ChatbrainLogo className="gap-6"/> chatbrain </h1>
      <div className="animated-hero">
        <Hero />
      </div>
      <Footer />
    </>
  )
}

export default App
