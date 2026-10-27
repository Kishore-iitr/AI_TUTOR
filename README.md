# 🎓 AI Tutor (Putty) — CBSE Class 10 Interactive Learning Platform

[![Puter.js](https://img.shields.io/badge/AI%20Engine-Puter.js%20v2-blue.svg)](https://puter.com)
[![KaTeX](https://img.shields.io/badge/Math-KaTeX-007acc.svg)](https://katex.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenRouter](https://img.shields.io/badge/LLM-OpenRouter%20Auto--Router-purple.svg)](https://openrouter.ai/)

An intelligent, interactive learning platform designed for CBSE Class 10 students (Science & Mathematics). **AI Tutor** blends comprehensive curriculum notes, interactive PhET simulations, and an LLM-powered pedagogical assistant named **Putty** featuring real-time streaming, speech-to-text dictation, and complete LaTeX mathematical notation rendering.

---

## 🌟 Key Highlights

- **📘 Comprehensive CBSE Curriculum**: Full chapter-by-chapter notes for CBSE Class 10 Science & Mathematics, complete with structured headings, definitions, tabular comparisons, lists, and key formulas.
- **🧪 Interactive Simulation Labs**: Integrated PhET and web simulations mapped to specific chapters and experiments (e.g., Ohm's law, acid-base indicators, refraction of light, geometry).
- **🤖 Putty — The AI Doubt Assistant**:
  - **Streaming LLM Chat**: Instant word-by-word streaming responses with real-time "Thinking..." indicator.
  - **Multi-Model Intelligence**: Switch seamlessly between Free Auto-Routing (`openrouter/free`), GPT-4o Mini, Claude 3 Haiku, Claude 3.5 Sonnet, and GPT-4o.
  - **Speech-to-Text Input**: Built-in voice dictation powered by the Web Speech API.
  - **Dual-State Send/Stop Button**: Start and halt generation on demand, mimicking modern interfaces like Antigravity and ChatGPT.
  - **Integrated Antigravity-Style Dock**: Compact, sleek input bar with inline model switcher and audio controls.
- **📐 Mathematical & Chemical Equation Rendering**: Powered by KaTeX and `marked-katex-extension` to render standard LaTeX delimiters (`$$...$$`, `$..$`, `\\[...\\]`, and `\\(...\\)`).
- **💳 Puter.js Cloud Auth & Credit Tracker**: Real-time quota monitoring with visual conic-gradient radial meter and one-click Puter Account authentication.
- **💾 Local Storage Chat Persistence**: Automatically caches chat history with instant manual wipe support.

---

## 🗂️ Project Structure

```text
AI_TUTOR/
├── index.html                           # Single-page web app (Notes reader + Putty AI dock)
├── cbse_science_scraped_dataset.json    # Structured CBSE Class 10 Science notes dataset
├── cbse_maths_scraped_dataset.json      # Structured CBSE Class 10 Mathematics notes dataset
├── sci_math_simulations.json            # Curated PhET & web simulation mappings
├── scraper.py                           # Python web scraper for CBSE Science curriculum
├── scraper_maths.py                     # Python web scraper for CBSE Mathematics curriculum
├── .gitignore                           # Git ignore definitions
└── README.md                            # Project documentation
```

---

## 🚀 Live Demo & Getting Started

### Prerequisites

No complex build step or package installation is required to run the web application. You only need a modern web browser.

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Kishore-iitr/AI_TUTOR.git
   cd AI_TUTOR
   ```

2. **Serve with any local HTTP server**:
   Because the application loads JSON files (`fetch(...)`), run it via a local web server to avoid CORS `file://` restrictions:
   
   - **Using Python 3**:
     ```bash
     python -m http.server 8000
     ```
     Then navigate to `http://localhost:8000` in your browser.
     
   - **Using VS Code Live Server**:
     Right-click `index.html` and choose **"Open with Live Server"**.

   - **Using Node.js (`npx serve`)**:
     ```bash
     npx serve .
     ```

---

## 🤖 AI Tutor ("Putty") Capabilities

### 1. Model Selection & Credit Tiers

Putty leverages Puter.js with OpenRouter routing to offer both free and high-performance foundation models:

| Model | Value Identifier | Credit Cost | Description |
| :--- | :--- | :--- | :--- |
| **Auto-Router** | `openrouter/free` | **Free (0 Credits)** | Automatically routes queries to the best available free open-weights model. |
| **GPT-4o Mini** | `gpt-4o-mini` | Medium (2x) | Fast, highly capable reasoning model for everyday student queries. |
| **Claude 3 Haiku** | `claude-3-haiku` | Medium (2x) | Ultra-fast responses with high conversational nuance. |
| **Claude 3.5 Sonnet**| `claude-3-5-sonnet` | High (10x) | Premier benchmark performance for deep problem solving and mathematics. |
| **GPT-4o** | `gpt-4o` | High (10x) | Multimodal flagship model for complex logical deductions. |

### 2. Dual-State Control

- While idle, pressing <kbd>Enter</kbd> or clicking the **Send** button transmits the question.
- While the response is streaming, the Send icon dynamically morphs into a **Stop** button, allowing the user to abort generation immediately.

### 3. Voice Dictation

- Click the **Microphone** icon to dictate questions hands-free.
- Automatically handles punctuation and speech recognition events via the Web Speech API.

---

## 📊 Dataset Schema

The application uses a unified, structured JSON format for CBSE subjects.

### Structure of `cbse_*_scraped_dataset.json`:
```json
{
  "subject": "science",
  "class": 10,
  "chapters": [
    {
      "chapter_number": 1,
      "chapter_title": "Chemical Reactions and Equations",
      "subtopics": [
        {
          "subtopic_id": "ch1_sub1",
          "subtopic_title": "1.1 Chemical Reactions",
          "content_elements": [
            {
              "type": "heading",
              "level": 2,
              "text": "What is a Chemical Reaction?"
            },
            {
              "type": "paragraph",
              "text": "A process in which one or more substances..."
            },
            {
              "type": "formula",
              "text": "$$2H_2 + O_2 \\rightarrow 2H_2O$$"
            },
            {
              "type": "table",
              "headers": ["Type", "Example"],
              "rows": [
                ["Combination", "$$CaO + H_2O \\rightarrow Ca(OH)_2$$"],
                ["Decomposition", "$$2FeSO_4 \\xrightarrow{\\Delta} Fe_2O_3 + SO_2 + SO_3$$"]
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### Structure of `sci_math_simulations.json`:
```json
[
  {
    "subject": "science",
    "chapter_number": 12,
    "chapter_title": "Electricity",
    "experiments": [
      {
        "experiment_title": "Ohm's Law Virtual Lab",
        "simulation_url": "https://phet.colorado.edu/sims/html/ohms-law/latest/ohms-law_en.html",
        "learning_objective": "Explore relationship between voltage, current, and resistance."
      }
    ]
  }
]
```

---

## 🕷️ Scraping Pipeline

To regenerate or extend the curriculum datasets:

1. Install Python dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```
2. Run the scrapers:
   ```bash
   # Scrapes Science notes
   python scraper.py

   # Scrapes Mathematics notes
   python scraper_maths.py
   ```
The scripts clean text, parse formulas, format superscripts/subscripts, convert tables, and export standard JSON files.

---

## 🛠️ Built With

- **[Puter.js](https://js.puter.com/v2/)**: Cloud AI streaming, model routing, and client-side authentication.
- **[KaTeX](https://katex.org/)**: Fast math typesetting for LaTeX formulas.
- **[Marked.js](https://marked.js.org/)**: Markdown parsing with custom KaTeX tokens.
- **[DOMPurify](https://github.com/cure53/DOMPurify)**: Client-side sanitization to guarantee security.
- **[PhET Interactive Simulations](https://phet.colorado.edu/)**: Physics, chemistry, and math virtual laboratories.
- **HTML5 & Vanilla CSS**: Zero external CSS framework bloat, fast load times, and custom CSS variables.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open an issue or submit a pull request on [GitHub](https://github.com/Kishore-iitr/AI_TUTOR).

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
