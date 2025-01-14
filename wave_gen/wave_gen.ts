import { createCanvas } from "canvas"
import { createNoise3D } from "simplex-noise"
import * as fs from "fs"

type Speed = "slow" | "fast"
interface WavyParams {
  outPath?: string
  width?: number
  height?: number
  colors?: string[]
  waveCount?: number
  waveWidth?: number
  backgroundFill?: string
  blur?: number // Note: node-canvas filter support is experimental
  speed?: Speed
  waveOpacity?: number
}

export function generateWavyImage({
    outPath = "wavy_background.png",
    width = 1920,
    height = 1080,
    colors = ["#38bdf8", "#818cf8", "#c084fc", "#e879f9", "#22d3ee"],
    waveCount = 5,
    waveWidth = 50,
    backgroundFill = "black",
    blur = 100,
    waveOpacity = 0.5,
}: WavyParams) {
    const noise3D = createNoise3D()
    const canvas = createCanvas(width, height)
    const ctx = canvas.getContext("2d")

    // Fill the background
    ctx.fillStyle = backgroundFill
    ctx.globalAlpha = 1
    ctx.fillRect(0, 0, width, height)

    // Function to draw waves
    const drawWaves = (offsetX: number, offsetY: number, alpha: number) => {
        ctx.globalAlpha = alpha
        for (let waveIndex = 0; waveIndex < waveCount; waveIndex++) {
            ctx.beginPath()
            ctx.lineWidth = waveWidth
            ctx.strokeStyle = colors[waveIndex % colors.length]
            for (let x = 0; x < width; x += 5) {
                const y = noise3D(x / 1600, 0.6 * waveIndex, 0) * 400
                ctx.lineTo(x + offsetX, y + height * 0.55 + offsetY)
            }
            ctx.stroke()
            ctx.closePath()
        }
    }

    // Draw multiple copies with offset to create blur effect
    const blurPasses = Math.max(1, Math.floor(blur))
    const baseAlpha = waveOpacity / blurPasses

    for (let i = 0; i < blurPasses; i++) {
        const offset = (blur / 2) * (Math.random() - 0.5)
        drawWaves(offset, offset, baseAlpha)
    }

    // Save to file
    const buffer = canvas.toBuffer("image/png")
    fs.writeFileSync(outPath, buffer)
    console.log(`Saved wavy background to ${outPath}`)
}

// Example usage (uncomment to run directly):
generateWavyImage({
  outPath: "my_wavy.png",
  width: 4000,
  height: 4000,
  waveCount: 5,
  waveWidth: 250,
  waveOpacity: 0.7,
  colors: ["#38bdf8", "#818cf8", "#c084fc", "#e879f9", "#22d3ee"],
  backgroundFill: "#000000",
  blur: 200
})