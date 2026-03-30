# UV Netware – AI Analytics Pipeline

## Project Overview
A single‑page interactive dashboard that visualises an AI analytics pipeline. Users can step through each stage of the pipeline, see a plain‑English description, the key data attributes, and example JSON payloads.

## File Structure
```
UV Netware/
├─ .git/                # Git repository metadata
├─ index.html           # Entry point – loads Tailwind, Chart.js and our app
├─ css/
│   └─ styles.css      # All custom CSS (currently minimal because Tailwind is used)
├─ js/
│   └─ app.js          # Core JavaScript – pipeline data, UI rendering, Chart.js
├─ docs/
│   ├─ Analysis (1).docx
│   ├─ UV network architecture.pdf
│   └─ workflow AI_ML.docx
└─ README.md           # This file
```

## How to Run
1. Open `index.html` in a browser (no server required).  
2. The dashboard will load and you can click through the steps on the left.

## Development
- Edit `js/app.js` to modify the pipeline data or UI logic.
- Edit `css/styles.css` for any additional custom styling.
- Commit and push changes with the usual Git workflow.

---
*Built with Tailwind CSS, Chart.js and vanilla JavaScript.*
