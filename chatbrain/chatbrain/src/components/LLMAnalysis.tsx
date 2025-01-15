import { useEffect } from "react"

interface LLMAnalysisProps {
  files: File[]
  onComplete: (results: any) => void
  onLoading: (loading: boolean) => void
}

export function LLMAnalysis({ files, onComplete, onLoading }: LLMAnalysisProps) {
    useEffect(() => {
      async function getLLMAnalysis() {
        onLoading(true)
        try {
          const formData = new FormData()
          files.forEach(file => formData.append('files', file))

      // Build your date/time fields
      const currDate = new Date()
      const currDateMinusOneDay = new Date(currDate)
      currDateMinusOneDay.setDate(currDateMinusOneDay.getDate() - 1)
      const currTime = new Date()
      const currTimeMinusOneHour = new Date(currTime)
      currTimeMinusOneHour.setHours(currTimeMinusOneHour.getHours() - 1)

      formData.append('start_date', currDateMinusOneDay.toISOString())
      formData.append('end_date', currDate.toISOString())
      formData.append('start_time', currTimeMinusOneHour.toISOString())
      formData.append('end_time', currTime.toISOString())

      const response = await fetch('http://localhost:5000/llm', { method: 'POST', body: formData })
        const results = await response.json()
        onComplete(results)
      } catch (error) {
        alert("An error occurred in the LLM analysis.")
      } finally {
        onLoading(false)
      }
    }
    getLLMAnalysis()
  }, [files, onComplete, onLoading])

  return null
}