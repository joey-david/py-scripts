import { useEffect, useState } from "react"

const statusToProgress: Record<string, number> = {
  processing: 5,
  compressing: 10,
  metadata: 25,
  analysis: 35,
  done: 100
}

const statusMessages: Record<string, string> = {
  processing: "Processing your files...",
  compressing: "Compressing chat data...",
  metadata: "Analyzing metadata...",
  analysis: "Running LLM analysis...",
  done: "Analysis complete!"
}

export function LoadingBar() {
  const [status, setStatus] = useState("")
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const source = new EventSource("http://localhost:5000/analysis-progress", {
        withCredentials: false
    })
    
    source.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setStatus(data.status)
      setProgress(statusToProgress[data.status] || 0)
    }

    source.onerror = (error) => {
      console.error("SSE Error:", error)
      source.close()
    }

    return () => source.close()
  }, [])

  return (
    <div className="p-4 w-full max-w-xl mx-auto">
      <p className="text-center mb-2 font-medium">
        {statusMessages[status] || "Initializing..."}
      </p>
      <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
        <div
          className="bg-blue-600 h-2.5 rounded-full transition-all duration-300 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="text-center text-sm text-gray-500 mt-2">
        {progress}% Complete
      </p>
    </div>
  )
}