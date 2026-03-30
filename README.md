# UV Netware - Interactive AI Analytics Pipeline Explorer

Welcome to **UV Netware**, an interactive dashboard built to visually document and explain the lifecycle of raw analytics data as it travels through a modern AI analytics pipeline. This project was developed as part of an ongoing internship, tracking the day-to-day progress from Day 1.

## 🚀 Overview

This single-page application (SPA) serves as a visual, educational map. It replaces complex technical jargon with plain, conversational English definitions and concrete examples. As you click through the visual stepper, you see exactly how data evolves at each stage—from raw user events to actionable AI insights.

## 🧠 The 8-Step Analytics Pipeline

The core of the project visualizes these 8 exact steps. Navigating through the UI will provide rich, formatted analogies and examples for each:

1. **User Data Processed:** The initial capture point where raw events (clicks, page views) are cleaned and standardized.
2. **Aggregated Data Store (MongoDB):** The single source of truth storing the cleaned daily user activity data.
3. **Time Bucketing Engine:** Groups daily data into larger time periods (Weekly, Monthly, Yearly) so you don't deal with thousands of rows.
4. **Time-Based Summarisation Layer:** A staging area that aligns short-term, medium-term, and long-term grouped data.
5. **Metrics Calculator:** Converts those grouped datasets into calculated numbers like `totalSessions`, `avgSessionTime`, and `growthRate` to tell you how your app is performing.
6. **Insight Generator:** Scans the calculated metrics to find important patterns—cheering for "Highlights" and warning you of "Anomalies".
7. **AI Analytics Engine (LLM):** Steps in to interpret the data, translating statistical patterns into plain-English narratives and actionable business advice.
8. **Dashboard UI:** The final interactive frontier where human eyes instantly spot trends through beautiful charts and AI summary boxes.

## 🛠 Tech Stack

- **HTML5:** Core interactive structure.
- **Tailwind CSS (via CDN):** Rapid, rich, beautifully crafted utility stylings (glassmorphism, interactive states, custom color tokens).
- **Vanilla JavaScript:** Powers the interactive stepper state, JSON formatting, and dynamic DOM rendering.
- **Chart.js (via CDN):** Animates and visualizes the simulated analytic trends dynamically.

## 💻 How to Run

1. Clone this repository to your local machine.
2. Open `index.htm` directly in your web browser of choice. 
3. No build steps, no external servers required—the interactive logic runs entirely in the browser.

---
*Built with continuous iteration and focus on simplifying complex data engineering concepts into beautifully structured educational views.*
