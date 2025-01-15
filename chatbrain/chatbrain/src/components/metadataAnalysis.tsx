import { useEffect } from "react"

interface MetadataAnalysisProps {
  files: File[]
  onComplete: (metadata: any) => void
}

export function MetadataAnalysis({ files, onComplete }: MetadataAnalysisProps) {
  useEffect(() => {
    async function fetchMetadata() {
      try {
        const formData = new FormData()
        files.forEach((file, index) => formData.append('files', file, file.name))
        
        // Optional: show all the files content transmitted to the server

        const response = await fetch('http://localhost:5000/metadata', {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          throw new Error(`Server error: ${response.statusText}`)
        }

        const metadata = await response.json()
        onComplete(metadata)
      } catch (error) {
        console.error('Error fetching metadata:', error)
        alert("An error occurred in the metadata analysis.")
      }
    }
    fetchMetadata()
  }, [files, onComplete])

  return null
}

export default MetadataAnalysis