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
        
    await uploadAndAnalyze(selectedFiles)
  }

  // Handle upload button click
  const handleUploadClick = () => {
    fileInputRef.current?.click()
  }

  // Upload and analyze files
  const detectFileType = (files: File[]) => {
    const fileTypes = new Set<string>()
    const extensions = new Set<string>()

    files.forEach(file => {
      const mimeType = file.type
      const extension = file.name.split('.').pop()

      if (mimeType.startsWith('text')) {
        fileTypes.add('txt')
      } else if (mimeType.startsWith('audio')) {
        fileTypes.add('aud')
      } else if (mimeType.startsWith('image')) {
        fileTypes.add('img')
      } else {
        alert("A file of an invalid format was submitted.")
        throw new Error("A type of an invalid format was submitted.")
      }

      if (extension) {
        extensions.add(extension)
      }
    })

    if (fileTypes.size > 1 || extensions.size > 1) {
      alert("All files should be of the same type and extension.")
      throw new Error("All files should be of the same type and extension.")
    }
    if (fileTypes.has('txt') && files.length > 1) {
      alert("Only one text file is allowed.")
      throw new Error("Only one text file is allowed.")
    }
  }


  const uploadAndAnalyze = async (files: File[]) => {
    setIsLoading(true)
    
    try {
      detectFileType(files)

      const formData = new FormData()
      files.forEach(file => {
        formData.append('files', file)
      })

      const currDate = new Date();
      const currDateMinusOneDay = new Date(currDate);
      currDateMinusOneDay.setDate(currDateMinusOneDay.getDate() - 1);

      const currTime = new Date();
      const currTimeMinusOneHour = new Date(currTime);
      currTimeMinusOneHour.setHours(currTimeMinusOneHour.getHours() - 1);

      formData.append('start_date', currDateMinusOneDay.toISOString());
      formData.append('end_date', currDate.toISOString());
      formData.append('start_time', currTimeMinusOneHour.toISOString());
      formData.append('end_time', currTime.toISOString());

      const response = await fetch('http://localhost:5000/upload', {
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

  function cn(...classes: (string | undefined | null | false)[]): string {
    return classes.filter(Boolean).join(' ')
  }
  return (
    <main className="min-h-screen p-8 flex flex-col items-center">
      {/* <FeaturesSectionWithHoverEffects /> */}
      <div className={cn(
            "bg-muted/60 border-border hover:bg-muted/75 text-center",
            "border-2 border-dashed rounded-xl p-14",
            "group transition duration-300 ease-in-out hover:duration-200",
            "justify-center items-center flex flex-col",
          )}>
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
      </div>
    </main>
  )
}

export { Analysis }