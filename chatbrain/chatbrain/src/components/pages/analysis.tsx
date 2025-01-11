import { EmptyState } from "@/components/empty-state"
import { Results } from "@/components/results"
import { FeaturesSectionWithHoverEffects } from "@/components/input-selection"
import { PhoneCall, Image, Mic } from "lucide-react"

function Analysis() {
  return (
    <main className="min-h-screen p-8 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-6">Analysis</h1>
      <FeaturesSectionWithHoverEffects />
      <EmptyState
        className=""
        title="No Files Uploaded"
        description="Please upload an exported whatsapp chat, a set of screenshots or an audio recording of your vocal messages."
        icons={[Image, PhoneCall, Mic]} // optional set of icons
        action={{
          label: "Upload file(s)",
          onClick: () => {
            // handle file upload
          },
        }}
      />
      < Results data = {
        {
          conversation_metrics: {
            stability_score_out_of_100: 80,
            health_score_out_of_100: 60,
            intensity_score_out_of_100: 40
          },
          users: {
            "Alice": {
              assertiveness: 70,
              positiveness: 90,
              affection_towards_other: 80,
              romantic_attraction_towards_other: 10,
              rationality: 60,
              emotiveness: 70,
              IQ_estimate: 120
            },
            "Bob": {
              assertiveness: 30,
              positiveness: 40,
              affection_towards_other: 50,
              romantic_attraction_towards_other: 70,
              rationality: 80,
              emotiveness: 30,
              IQ_estimate: 110
            }
          },
          insights: [
            "Alice is more assertive than Bob",
            "Bob is more rational than Alice"          ]
        }
      }
      />
      <section className="mt-8 text-center">
        <h2 className="text-xl font-semibold">Analysis Results</h2>
        <p className="text-sm text-muted-foreground mt-2">
          This section will display your results once files have been analyzed.
        </p>
      </section>
    </main>
  )
}

export { Analysis }