import { useState, useRef } from 'react'
import { EmptyState } from "@/components/empty-state"
import { Results } from "@/components/results"
import { FeaturesSectionWithHoverEffects } from "@/components/input-selection"
import { PhoneCall, Image, Mic } from "lucide-react"

interface AnalysisResults {
  data: any;
  timestamp: string;
  conversation_metrics: any; // Replace 'any' with the appropriate type
  users: any; // Replace 'any' with the appropriate type
  insights: any; // Replace 'any' with the appropriate type
}

function Analysis() {
  // State management
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Handle file selection
  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files?.length) return

    const selectedFiles = Array.from(event.target.files)
    
    // Check if files are all the same type
    const fileType = selectedFiles[0]?.type
    const allSameType = selectedFiles.every(file => file.type === fileType)
    
    if (!allSameType) {
      alert("All files must be of the same type")
      return
    }

    await uploadAndAnalyze(selectedFiles)
  }

  // Handle upload button click
  const handleUploadClick = () => {
    fileInputRef.current?.click()
  }

  // Upload and analyze files
  const uploadAndAnalyze = async (files: File[]) => {
    setIsLoading(true)
    
    try {
      const formData = new FormData()
      files.forEach(file => {
        formData.append('files', file)
      })

      const response = await fetch('http://chatbrain/api/files.py', {
        method: 'POST',
        body: formData
      })

      const results = await response.json()
      setAnalysisResults(results)
    } catch (error) {
      console.error('Error uploading files:', error)
      alert('An error occurred while uploading files. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="min-h-screen p-8 flex flex-col items-center">
      {/* <FeaturesSectionWithHoverEffects /> */}
      
      <input
        type="file"
        ref={fileInputRef}
        className="hidden"
        multiple
        onChange={handleFileSelect}
      />

      <EmptyState
        className=""
        title="No Files Uploaded"
        description="Please upload an exported whatsapp chat, a set of screenshots or an audio recording of your vocal messages."
        icons={[Image, PhoneCall, Mic]}
        action={{
          label: "Upload file(s)",
          onClick: handleUploadClick,
        }}
      />

      {/* Loading and Results Section */}
      <div className="w-full max-w-3xl mt-8">
        {isLoading && (
          <div className="flex justify-center items-center p-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
          </div>
        )}
        {!isLoading && analysisResults && (
          <Results data={analysisResults} />
        )}
      </div>
    </main>
  )
}

export { Analysis }