import { useState, useEffect, useRef } from "react"
import { validateFiles } from "@/utils/fileValidation"
import { MetadataAnalysis } from "@/components/metadataAnalysis"
import { LLMAnalysis } from "@/components/LLMAnalysis"
import { MetadataResults } from "@/components/metadataResults"
import { LLMResults } from "@/components/LLMResults"
import { EmptyState } from "@/components/empty-state"
import { PhoneCall, Image, Mic } from "lucide-react"
import { LoadingBar } from "../ui/loadingBar"


function Analysis() {
  const [metadataResults, setMetadataResults] = useState(null)
  const [llmResults, setLlmResults] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [fileType, setFileType] = useState<'txt' | 'img' | 'aud' | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleUploadClick = () => fileInputRef.current?.click()

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files?.length) return
    const files = Array.from(event.target.files)

    try {
      validateFiles(files)
      setSelectedFiles(files)
      if (files[0].name.endsWith(".txt")) setFileType("txt")
      else if (files[0].type.startsWith("image")) setFileType("img")
      else if (files[0].type.startsWith("audio")) setFileType("aud")
    } catch (error) {
      console.error("Validation error:", error)
    }
  }

  return (
    <main className="p-8 flex flex-col items-center">
      <div className="bg-muted/60 border-border text-center border-2 rounded-xl p-14 justify-center items-center flex flex-col">
        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          multiple
          onChange={handleFileSelect}
        />
        <EmptyState
          title={selectedFiles.length ? `Selected: ${selectedFiles[0].name}` : "No Files Uploaded"}
          description={
            selectedFiles.length
              ? `${selectedFiles.length} file(s) selected - ${fileType?.toUpperCase() || 'Unknown'} type`
              : "Please upload an exported whatsapp chat, screenshots, or an audio recording."
          }
          icons={[Image, PhoneCall, Mic]}
          action={{
            label: selectedFiles.length ? "Change files" : "Upload file(s)",
            onClick: handleUploadClick,
          }}
        />

        {/* Display the metadata results first, as they are shorter and are retrieved faster */}
        {metadataResults && (
          <div className="max-w-5xl mt-6 w-full">
            <MetadataResults data={metadataResults} />
          </div>
        )}

        {/* Loading Spinner */}
        {isLoading && (
          <LoadingBar />
        )}

        {/* Main LLM results */}
        {!isLoading && llmResults && (
          <div className="max-w-5xl mt-6 w-full">
            <LLMResults data={llmResults} />
          </div>
        )}

        {/* Trigger analyses once files are set */}
        {selectedFiles.length > 0 && (
          <>
            <MetadataAnalysis files={selectedFiles} onComplete={setMetadataResults} />
            <LLMAnalysis
              files={selectedFiles}
              onComplete={setLlmResults}
              onLoading={setIsLoading}
            />
          </>
        )}
      </div>
    </main>
  )
}

export { Analysis }