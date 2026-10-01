<div align="center">

# 🌸 Sakhi AI • சகி • सखी
### *Voice-First, Zero-Literacy Welfare Gateway for Rural India*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/LLM-Gemini%20%2F%20OpenRouter%20%2F%20Ollama-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Tavily Search](https://img.shields.io/badge/Search%20Grounding-Tavily%20%2F%20Google-FF6F00?style=for-the-badge)](https://tavily.com)
[![PWA Ready](https://img.shields.io/badge/PWA-Zero--Install-5A0FC8?style=for-the-badge&logo=pwa&logoColor=white)](https://web.dev/progressive-web-apps/)
[![Languages](https://img.shields.io/badge/Languages-Tamil%20%7C%20Hindi%20%7C%20Telugu%20%7C%20English-1976D2?style=for-the-badge)](#%EF%B8%8F-supported-languages)
[![Web Speech API](https://img.shields.io/badge/Voice-Web%20Speech%20API-FF6F00?style=for-the-badge&logo=googlechrome&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
[![SDG Alignment](https://img.shields.io/badge/UN%20SDGs-SDG%205%20%7C%204%20%7C%2010-E5243B?style=for-the-badge)](https://sdgs.un.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  <b>No typing. No reading. No English required.</b><br>
  Empowering rural Indian women to discover, understand, and claim verified government welfare schemes directly in their mother tongue through pure voice interaction.
</p>

<p align="center">
  <b>🗣️ Tamil</b> &nbsp;•&nbsp; <b>हिंदी Hindi</b> &nbsp;•&nbsp; <b>తెలుగు Telugu</b> &nbsp;•&nbsp; <b>English</b>
</p>

[✨ Key Features](#-key-features) • [🗣️ Languages](#%EF%B8%8F-supported-languages) • [✅ Verified Results](#-verified-live-results) • [🚨 Error Handling](#%EF%B8%8F-error-handling-matrix) • [🏛️ Architecture](#-system-architecture) • [🚀 Quick Start](#-quick-start) • [📡 API Reference](#-api-reference) • [🎯 Supported Schemes](#-supported-schemes--test-cases) • [🌱 SDG Impact](#-un-sdg-alignment) • [🗺️ Roadmap](#-scalability-roadmap)

---

</div>

## 📌 The Problem We Solve

There are **400+ central and state welfare schemes** in India with thousands of crores allocated every year. Yet, millions of eligible rural women miss out on life-changing maternity benefits, education scholarships, and enterprise loans because:

1. **Information Asymmetry:** Scheme portals are written in complex administrative English or high-register official vocabulary.
2. **Literacy & Tech Barrier:** Navigating multi-page government portals (`myscheme.gov.in`, `nsp.edu.in`) requires digital literacy, reading skills, and smartphones.
3. **Hallucination Risk in AI:** Standard conversational LLMs frequently hallucinate rupee amounts, outdated eligibility cutoffs, or nonexistent rules.

> [!IMPORTANT]
> **Sakhi AI bridges this last-mile gap.** It converts spoken colloquial dialects into high-precision government portal search queries, grounds every single claim on live `.gov.in` records, and responds in warm kinship language (*"Akka" / "Didi"*) with a spoken voice output and high-contrast visual cue cards.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🎙️ **Voice-In / Voice-Out UI** | Zero typing required. Powered by Web Speech API with automatic speech recognition (ASR) and browser Text-To-Speech (TTS). |
| 💬 **Chat-Style Interface** | Every question and answer is a real chat bubble. Her words on the right, Sakhi's verified card on the left. One big mic, nothing else. |
| 🗺️ **Language Gate Onboarding** | An animated traditional woman asks "which language?" first. Four languages, then the mic appears. Nothing else on screen. |
| 🔍 **Live Search Grounding** | Every answer is grounded in real-time via **Tavily** or **Google Search Grounding** querying `myscheme.gov.in`, `pib.gov.in`, and state `.gov.in` sites. |
| 🛡️ **Anti-Hallucination Engine** | Strict JSON schema contract, low-temperature inference (0.2), and strict system instructions forbidding fabricated rupee amounts. |
| 🗣️ **Colloquial Dialect Tuning** | Query transformer converts rural, broken speech (e.g. *"என் மகள் 10 ஆம் வகுப்பு முடித்துள்ளா..."*) into portal-grade search queries. |
| 🏷️ **Verified Domain Badging** | Transparent trust scoring — verifies `.gov.in` / `.nic.in` domains and visibly flags verified official sources on the UI. |
| ⚡ **Multi-LLM Resilience** | Built-in provider fallback: **Google Gemini 3.8 Flash** → **OpenRouter** → **Local Offline Ollama** (`llama3.1`). Zero-quota safe. |
| 📱 **Zero-Literacy PWA** | Oversized **150px glowing mic target**, high-contrast benefit banners, visual document badge icons (Aadhaar, Marksheet, Passbook), and offline tolerance. |
| ⌨️ **Type Anything Instead** | A text composer sits under the mic for anyone who cannot speak — same grounded pipeline, same answer. |

---

## 🗣️ Supported Languages

Sakhi asks first, then listens. Speech recognition, text-to-speech, every label, and every error
message switch to the chosen language.

| # | Language | Locale | Script | Tested end-to-end |
| :--: | :--- | :--- | :--- | :--: |
| 1 | **தமிழ்** Tamil | `ta-IN` | Tamil | ✅ |
| 2 | **हिंदी** Hindi | `hi-IN` | Devanagari | ✅ |
| 3 | **తెలుగు** Telugu | `te-IN` | Telugu | ✅ |
| 4 | **English** | `en-IN` | Latin | ✅ |

**Graceful degradation, honestly handled**
- If the device has **no voice** for the chosen language, the app logs a warning and still shows
  every word on screen — nothing is silently dropped.
- If the browser has **no Speech Recognition** (e.g. Firefox), the mic is disabled with a dashed
  border, the gate explains why, and the text composer still works.
- `no-speech` is reported as *"I didn't hear anything, please speak again"*, never as a crash.

---

## ✅ Verified Live Results

Real responses from the running pipeline (Tavily retrieval + LLM), captured during testing:

| Spoken / typed question | Language | Answer returned | Official sources |
| :--- | :--- | :--- | :--: |
| `gas cylinder kahan se milega` | Hindi | **Pradhan Mantri Ujjwala Yojana** — free LPG connection, first refill + stove; Aadhaar, bank details, ration card; go to local LPG distributor | 6 / 6 `.gov.in` |
| `I am 5 months pregnant, will government give money?` | English | **PMMVY** — ₹5,000 first child, ₹6,000 second; Aadhaar, pregnancy certificate, bank account; go to Anganwadi | 6 / 6 `.gov.in` |
| `gas cylinder kahan se milega` | Telugu / Kannada / Assamese | Correct scheme, localized `spoken_script` | 6 / 6 `.gov.in` |

`/health` at time of writing:
```json
{ "ready": true, "retrieval": { "provider": "tavily" }, "llm": { "providers_available": ["gemini", "ollama"] } }
```

---

## 🚨 Error Handling Matrix

Nothing technical ever reaches the woman. Every failure has a warm, localized, spoken fallback —
and an honest one.

| Failure | Detected via | What she sees / hears | Status dot |
| :--- | :--- | :--- | :--: |
| Browser cannot listen | `SpeechRecognition` undefined | Mic disabled, dashed border, gate explains, typing still works | grey |
| Mic permission denied | `not-allowed` | "I could not hear you. Please tap the mic and speak again." | grey |
| Nothing said | `no-speech` | "I didn't hear anything. Please speak again." | grey |
| Language unsupported by browser | `language-not-supported` | "No voice for this language. Please type instead." | grey |
| Server not running | fetch rejects | "Sakhi is not connected right now." | 🔴 red |
| Wrong port / missing route | HTTP 404, 502 | "Sakhi's server is not connected right now." | 🔴 red |
| No API key configured | HTTP 503 | "Sakhi's server is not connected right now." | 🔴 red |
| Quota exhausted | HTTP 429 | "Sakhi's server is busy at the moment." | 🔴 red |
| Search took too long | `AbortController` @ 90s | "The search took too long. Please ask again." | 🔴 red |
| LLM returned odd JSON keys | alias normalizer | Same card, keys remapped automatically | 🟢 green |
| Just a greeting (`hi`, `hello`, `namaste`) | local shortcut | Instant reply, no API call spent | 🟢 green |

A green dot means the last search returned a grounded, sourced answer.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Client ["📱 Zero-Literacy Voice PWA (index.html)"]
        A[🎙️ Voice or Typed Input in Tamil / Hindi / Telugu / English] --> B[Web Speech STT / Audio Visualizer]
        B --> C[HTTP POST /api/query]
        K[🔊 Spoken Voice TTS] <-- J[High-Contrast Visual Card & Badges]
        J <-- I[Response Parser & Normalizer]
    end

    subgraph Backend ["⚡ FastAPI Gateway (main.py)"]
        C --> D[Language & Script Detector (query.py)]
        D --> E[Colloquial Query Transformer]
        E --> F[Dual Retrieval Engine (search.py)]
        
        subgraph Retrieval ["🌐 Real-time Grounding"]
            F -->|Primary| G1[Tavily API - site:*.gov.in]
            F -->|Fallback| G2[Gemini Google Search Grounding]
        end

        G1 --> H[Rank & Context Builder]
        G2 --> H
        
        subgraph Reasoning ["🧠 Anti-Hallucination LLM Layer (llm.py)"]
            H --> L{LLM Provider Router}
            L -->|Cloud Primary| M1[Gemini 2.5 / 3.8 Flash]
            L -->|Cloud Secondary| M2[OpenRouter]
            L -->|Offline Local| M3[Ollama LLaMA 3.1]
            M1 & M2 & M3 --> N[Enforced JSON Schema Validation]
        end

        N --> I
    end
```

---

## 📱 The Interface, Screen by Screen

**Screen 1 — The language gate**
An animated traditional woman in a sari waves, the speech bubble blinks, and four big language
buttons appear. That is the entire screen. She cannot misread it and she cannot mis-tap it.

**Screen 2 — The chat**
- Header: `●` connection dot, name, current language chip (tap it to change language).
- Chat log: her question as an orange bubble on the right, Sakhi's answer on the left.
- Sakhi's answer card: scheme name → `✓ verified on a government portal` chip → green benefit
  banner → who can apply → document badges with SVG icons (Aadhaar, marksheet, passbook) → orange
  "where to go" block → source list → `🔊 Listen again` + `🎙️ Ask another question`.
- Bottom dock: audio visualizer, a **150px mic**, and a text composer.
- While searching: a bouncing-dots typing bubble with "Searching government portals".

Every word — including all error messages — is written in her chosen language.

---

## 📂 Project Structure

```
sakhi_ai/
├── 📄 main.py                 # FastAPI backend gateway & API endpoints (/api/query, /health, /api/schemes)
├── 📄 query.py                # Dialect query transformer, language detection & official domain verification
├── 📄 search.py               # Live retrieval layer (Tavily government search & Gemini grounding fallback)
├── 📄 llm.py                  # Multi-LLM provider engine (Google GenAI, OpenRouter, Ollama)
├── 🌐 index.html              # Single-file high-contrast PWA: animated language gate → chat + 150px mic
├── 📱 manifest.json           # Progressive Web App manifest configuration
├── 📋 requirements.txt        # Python backend dependencies
├── ⚡ start.ps1               # Automated startup script for Windows PowerShell
├── 📖 TASK4_DEMO_AND_PITCH.md # 3-minute judge walkthrough script, SDG scorecard & roadmap
└── 📘 README.md               # Project documentation
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** installed
- A modern browser (**Google Chrome** or **Microsoft Edge** recommended for Web Speech API support)
- At least one API key:
  - `GEMINI_API_KEY` (from [Google AI Studio](https://aistudio.google.com/)) **and/or**
  - `TAVILY_API_KEY` (from [Tavily AI](https://tavily.com/))

---

### Installation & Execution

#### Option 1: Quick Launch (Windows PowerShell)

```powershell
# 1. Clone or navigate to the directory
cd sakhi_ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API Key (or set in Windows Environment Variables)
$env:GEMINI_API_KEY="your-gemini-api-key"
$env:TAVILY_API_KEY="your-tavily-api-key"   # Optional, recommended

# 4. Start the server
.\start.ps1
```

#### Option 2: Manual Start (Cross-Platform / Linux / macOS)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Export API keys
export GEMINI_API_KEY="your-gemini-api-key"
export TAVILY_API_KEY="your-tavily-api-key"  # Optional

# 3. Run FastAPI gateway with uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Option 3: Offline / Local Execution via Ollama

Sakhi AI can run without any cloud API keys using **Ollama**:
```bash
# Ensure Ollama is running locally with llama3.1
ollama run llama3.1

# Run the server (it will auto-detect Ollama)
python -m uvicorn main:app --port 8000
```

> [!TIP]
> Once started, open **`http://localhost:8000/index.html`** in your browser. You can also open `index.html` directly as a standalone file; the frontend auto-detects `localhost:8000`.

---

## ⚙️ Environment Configuration

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | *(None)* | Primary LLM key. Also enables Gemini Search grounding as the retrieval fallback. |
| `TAVILY_API_KEY` | *(None)* | Web search restricted to official Indian government portals (preferred retrieval). |
| `OPENROUTER_API_KEY` | *(None)* | Second LLM provider — any model the account has credits for. |
| `SAKHI_LLM_PROVIDER` | `auto` | Force one provider: `gemini`, `openrouter` or `ollama`. `auto` walks the chain until one answers. |
| `SAKHI_MODEL` | `gemini-3.8-flash` | Primary Gemini model id. `gemini-2.5-flash` is retired for new keys (404). |
| `SAKHI_MODEL_FALLBACKS` | `gemini-flash-latest` | Comma-separated Gemini fallback model list. |
| `OLLAMA_HOST` | `http://localhost:11434` | Endpoint for local offline LLM inference. |
| `SAKHI_OLLAMA_MODEL` | `llama3.1` | Model name when running under Ollama. |
| `SAKHI_LLM_TIMEOUT` | `90` | Seconds before a slow provider is abandoned for the next one. |

---

## 📡 API Reference

### 1. Process Voice / Text Query
**`POST /api/query`**

#### Request Payload
```json
{
  "query": "என் மகள் 10 ஆம் வகுப்பு முடித்துள்ளா, அவளுக்கு படிக்க உதவி திட்டம் இருக்கா?",
  "language": "Tamil"
}
```
*`language` accepts `"Tamil"`, `"Hindi"`, `"Telugu"`, `"English"`, or `"auto"` (auto-detected via Unicode script and keyword n-grams).*

#### Response (Guaranteed JSON Schema)
```json
{
  "scheme_name": "National Scholarship Portal (Post-Matric Scholarship for Girls)",
  "benefit_summary": "₹10,000 - ₹35,000 per year paid directly into the student's bank account",
  "eligibility": [
    "Girl student who has passed 10th standard in a recognized government/aided school",
    "Annual family income less than ₹2,50,000"
  ],
  "documents_needed": [
    "Aadhaar Card",
    "10th Standard Marksheet",
    "Bank Passbook copy (linked to Aadhaar)",
    "Income Certificate"
  ],
  "where_to_go": "Block Education Office (BEO) or school scholarship desk",
  "spoken_script": "அக்கா, உங்கள் மகள் 10-ஆம் வகுப்பு முடித்திருந்தால் கல்வி உதவித்தொகை பெறலாம். ஆதார் அட்டை, மதிப்பெண் சான்றிதழ் மற்றும் வங்கி கணக்கு புத்தகத்துடன் பள்ளி அல்லது வட்டார கல்வி அலுவலகத்தை அணுகவும்.",
  "confidence": "high",
  "verified": true,
  "sources": [
    {
      "title": "National Scholarship Portal - Government of India",
      "url": "https://scholarships.gov.in",
      "official": true,
      "excerpt": "Post matric scholarship scheme for girl students..."
    }
  ],
  "language": "Tamil",
  "search_query": "National Scholarship Portal post matric scholarship girls eligibility Tamil Nadu benefit amount required documents myscheme.gov.in",
  "retrieval": "tavily",
  "model": "ollama/llama3.1",
  "sources_consulted": 6
}
```

> The `model` field always tells you which provider actually answered — `gemini-3.8-flash`,
> an OpenRouter model id, or `ollama/llama3.1` when everything cloud-side was unavailable.

---

### 2. Service Health & Readiness
**`GET /health`**

```json
{
  "status": "ok",
  "retrieval": {
    "provider": "tavily",
    "tavily_configured": true,
    "max_results": 6
  },
  "llm": {
    "llm_provider": "gemini",
    "providers_available": ["gemini", "ollama"],
    "gemini_configured": true,
    "openrouter_configured": false,
    "ollama_available": true,
    "ollama_model": "llama3.1",
    "models": ["gemini-3.8-flash", "gemini-flash-latest"]
  },
  "ready": true
}
```

---

## 🎯 Supported Schemes & Test Cases

The query transformer is pre-tuned for core rural welfare domains across India:

```
┌────────────────────────────────────────┬────────────────────────────────────────┬────────────────────────────────────────┐
│ Scheme Name                            │ Colloquial Spoken Voice Trigger        │ Key Verified Benefit                   │
├────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┤
│ 🤰 Pradhan Mantri Matru Vandana (PMMVY)│ "5 months pregnant, will govt give     │ ₹5,000 maternity cash benefit paid in   │
│                                        │ money?" / "நான் கர்ப்பிணி..."          │ direct installments via Anganwadi      │
├────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┤
│ 🧵 Lakhpati Didi & SHG Loans           │ "mujhe silai ka kaam shuru karna hai"  │ Interest-subvention loans up to ₹1-5L  │
│                                        │ / "தையல் தொழில் கடன்..."                │ for women Self-Help Groups (Gram P.)   │
├────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┤
│ 🎓 National Scholarship Portal (NSP)   │ "Daughter passed 10th, help for study?"│ Annual scholarship up to ₹35,000 for   │
│                                        │ / "10-ஆம் வகுப்பு படிப்பு உதவி..."     │ post-matric higher education           │
├────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┤
│ 🔥 PM Ujjwala Yojana                   │ "gas cylinder kahan se milega"         │ Free LPG connection + first refill     │
│                                        │ / "இலவச எரிவாயு சிலிண்டர்..."          │ & stove subsidy                        │
├────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┤
│ 👧 Sukanya Samriddhi Yojana (SSY)      │ "daughter savings scheme" / "மகள் சேமிப்பு" High-interest girl child deposit at PO │
├────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┤
│ 🏥 Ayushman Bharat (PM-JAY)            │ "health card hospital free treatment"  │ Up to ₹5 Lakh cashless family coverage │
└────────────────────────────────────────┴────────────────────────────────────────┴────────────────────────────────────────┘
```

---

## 🛡️ Anti-Hallucination & Trust Architecture

Sakhi AI is purpose-built to eliminate hallucinated welfare claims:

1. **Mandatory Live Retrieval:** The LLM is never permitted to answer welfare details from parametric memory. Excerpts from `.gov.in` must be present.
2. **Domain-Restricted Search:** Search strings explicitly append `site:myscheme.gov.in OR site:pib.gov.in OR site:*.gov.in`.
3. **Official URL Scoring:** Source URLs are parsed and classified. Official domains receive top ranking; commercial loan aggregators and third-party blogs are filtered.
4. **Honest Confidence Downgrading:** If official excerpts do not contain the verified amount, the system marks `confidence: "low"` and instructs the user which local physical office (e.g. *Anganwadi*, *Gram Panchayat*) to visit in person.
5. **No Technical Error Leakage:** Network hiccups or transient errors are never shown as stack traces; they are translated into gentle, spoken encouragement.

---

## 🌱 UN SDG Alignment

Sakhi AI directly addresses 5 United Nations Sustainable Development Goals:

```
     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
     │   SDG 5 ♀️   │     │   SDG 4 📚   │     │   SDG 10 ⚖️  │
     │Gender Equality│    │Quality Educ. │     │Reduced Ineq. │
     └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
            │                    │                    │
            └────────────┐       │       ┌────────────┘
                         ▼       ▼       ▼
                     ┌───────────────────────┐
                     │     🌸 SAKHI AI       │
                     │  Inclusion by Design  │
                     └───────────┬───────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
             ┌──────────────┐          ┌──────────────┐
             │   SDG 3 🏥   │          │   SDG 8 💼   │
             │ Good Health  │          │ Decent Work  │
             └──────────────┘          └──────────────┘
```

- **SDG 5 — Gender Equality:** Closes the last-mile information gap for women-centric entitlements.
- **SDG 4 — Quality Education:** Promotes girl-child secondary & higher education retention via post-matric scholarship discovery.
- **SDG 10 — Reduced Inequalities:** Eradicates the literacy barrier — illiterate rural citizens get identical verified access to public funds as urban users.
- **SDG 3 — Good Health:** Accelerates maternal and child health benefits (PMMVY, Janani Suraksha, Ayushman Bharat).
- **SDG 8 — Decent Work & Economic Growth:** Direct discovery of *Lakhpati Didi* and *PM Mudra* loans for micro-enterprises.

---

## 🗺️ Scalability Roadmap

```
  [P0] Completed
  ├── Grounded FastAPI gateway + Gemini 2.5 Flash
  ├── Zero-literacy single-button PWA (Tamil / Hindi / English)
  └── Official .gov.in domain ranker & trust scoring

  [P1] Dialect & Regional Scale (Next 4 Weeks)
  ├── Bhashini ASR/TTS regional voice models
  └── Support for 8 additional Indian languages (Telugu, Kannada, Malayalam, Marathi, Bengali, Odia, Gujarati, Punjabi)

  [P2] Real-Time Scheme Knowledge Graph (Next 8 Weeks)
  ├── Nightly crawl & vector indexing of myscheme.gov.in & 30 state portals
  └── Rule-based eligibility pre-check

  [P3] WhatsApp Voice Note Integration (3 Months)
  └── Forward voice notes to WhatsApp Business bot; receive voice notes + printable document checklists

  [P4] Toll-Free IVR Phone Gateway (6 Months)
  └── DTMF-free voice phone dialer for non-smartphone users on basic feature phones (2G)

  [P5] Direct Grievance & Application Submission (12 Months)
  └── Integration with state single-window portals & human nodal officer escalation
```

---

## 🤝 Contributing

Contributions are warmly welcome! If you'd like to add new dialect cues, expand language support, or enhance government portal scrapers:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/dialect-expansion`)
3. Commit your changes (`git commit -m 'Add Telugu & Kannada dialect cues'`)
4. Push to the branch (`git push origin feature/dialect-expansion`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<div align="center">
  <sub>Built with ❤️ for rural inclusion • <b>Sakhi AI</b></sub>
</div>
