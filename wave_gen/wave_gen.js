const { createCanvas } = require('canvas');
const { createNoise3D } = require('simplex-noise');
const fs = require('fs');

// Configuration
const config = {
    width: 3000,
    height: 3000,
    waveColors: ["#818cf8", "#c084fc", "#e879f9", "#22d3ee"],
    waveWidth: 150,
    backgroundFill: "black",
    backgroundOpacity: 1.0, // New separate opacity for background
    waveOpacity: 1.5,
    blur: 300
};

// Create canvas and context
const canvas = createCanvas(config.width, config.height);
const ctx = canvas.getContext('2d');

// Initialize 3D noise
const noise = createNoise3D();

// Draw waves
function drawWave(n, offsetX = 0, offsetY = 0, alpha = config.waveOpacity) {
    ctx.globalAlpha = alpha; // Set opacity for waves
    for (let i = 0; i < n; i++) {
        ctx.beginPath();
        ctx.lineWidth = config.waveWidth;
        ctx.strokeStyle = config.waveColors[i % config.waveColors.length];
        
        for (let x = -100; x < config.width + 100; x += 5) {
            const y = noise(x / 2400, 0.3 * i, 0) * 300;
            ctx.lineTo(x + offsetX, y + config.height * 0.5 + offsetY);
        }
        
        ctx.stroke();
        ctx.closePath();
    }
}

// Main rendering function
function render() {
    // Set background with its own opacity
    ctx.globalAlpha = config.backgroundOpacity;
    ctx.fillStyle = config.backgroundFill;
    ctx.fillRect(0, 0, config.width, config.height);
    
    // Draw waves with blur effect
    const blurPasses = Math.max(1, Math.floor(config.blur));
    const baseAlpha = config.waveOpacity / blurPasses;

    for (let i = 0; i < blurPasses; i++) {
        const offset = (config.blur / 2) * (Math.random() - 0.5);
        drawWave(5, offset, offset, baseAlpha);
    }
    
    // Save to file
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync('wave-output.png', buffer);
    console.log('Image saved as wave-output.png');
}

// Generate the image
render();