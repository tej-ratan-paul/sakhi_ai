# Sakhi AI — Task 4 Deliverables: Demo Script, Pitch Deck & SDG Alignment

## 1. Live Demo Script (3-Minute Judge Walkthrough)

**Setup before the demo:** `GEMINI_API_KEY` exported, `uvicorn main:app` running, phone/laptop on
`localhost:8000/index.html`. Use a real mic, Tamil mode, dark room. No slides during the live part.

### Minute 0:00 – 0:25 — The problem hook
> "There are 400+ central welfare schemes. My neighbour, Ramani, lost 14 months of maternity benefit
> not because she was ineligible, but because nobody could explain it to her in Tamil. The scheme
> existed. The information did not reach the person it was written for.
> That is the invisible woman this project is about."

Point at the screen: one 160px orange microphone. Nothing else.

### Minute 0:25 – 1:10 — Live test case (Scenario C, the judged scenario)
Ask the judge: *"Who here has a sister, a daughter, a neighbour who is 10th standard and asking
'does the government pay for my studies?' Let's ask Sakhi exactly that."*

1. **Voice-in (0:25)** — Press mic, speak the Tamil test line in a natural dialect:
   > *"என் மகள் 10 ஆம் வகுப்பு முடித்துள்ளா, அவளுக்கு இனி படிக்க உதவி திட்டம் இருக்கா?"*
2. **Query transformation (0:35)** — Show the search string on screen (proves it is not a chatbot guess):
   `National Scholarship Portal post matric scholarship girls eligibility India benefit amount required documents myscheme.gov.in`
3. **Grounding (0:40)** — Point out the live crawl of myscheme.gov.in / nsp.edu.in. Say:
   "Gemini 2.5 Flash is searching the government portals right now. It cannot answer from memory."
4. **Visual card (0:50)** — Card renders: scheme name, green benefit banner, document badges with
   icons (Aadhaar icon, marksheet book icon), orange "where to go" panel, and green checkmarked
   `✓ அரசு வலைத்தளம்` chip.
5. **Voice-out (1:00)** — Audio auto-plays the Tamil spoken_script. Do not talk over it. Let the
   judge hear a warm human voice explain a government rule in plain words.

### Minute 1:10 – 1:40 — Stress the judge with the hard cases
Run these live, fast, from the text fallback box if the mic is flaky:
- `I am 5 months pregnant, will government give money?` → PMMVY, ₹5,000, Anganwadi.
- `mujhe silai ka kaam shuru karna hai` → Lakhpati Didi / SHG, Gram Panchayat.
- `gas cylinder kahan se milega` → Ujjwala, LPG distributor.
- Garbage input: `xyzqwerty` → she gets a kind spoken retry, never a stack trace.

Say the line: **"Same code, four states, two languages, zero reading required."**

### Minute 1:40 – 2:10 — How it is trustworthy (judge's #1 worry)
- Every answer ships with source URLs pulled from `grounding_metadata`, and the UI marks which ones
  are official `.gov.in` domains. Non-official sources are visibly demoted, never hidden silently.
- `build_search_query()` converts rural speech into portal-grade search terms before the model ever
  sees them, so the model searches the right portal instead of guessing.
- The persona is forbidden from inventing an amount: the system instruction says to set
  `confidence: low` and say so plainly rather than guess.
- Low temperature (0.2) + strict JSON schema = no creative writing in a welfare answer.

### Minute 2:10 – 2:40 — Access reach (why voice is the whole product)
- Web Speech API = zero install, works on any Android with Chrome, offline-tolerant UI shell.
- Bhashini regional engine is the drop-in upgrade for dialect STT/TTS quality.
- 140px single-button target, ~55px minimum, zero English text required to finish a task.

### Minute 2:40 – 3:00 — The ask and close
> "4 hours built the proof. The next 4 months builds reach: a WhatsApp voice-note bot and a toll-free
> IVR dialer so the poorest woman needs no smartphone at all. Every rupee of welfare already exists
> in the budget. Sakhi AI just makes sure it reaches the woman it was written for."

---

## 2. Hackathon Alignment Scorecard

### SDG Alignment
| SDG | How Sakhi AI serves it |
| :--- | :--- |
| **SDG 5 — Gender Equality** | Women-first access layer to money the state already allocates; closes the last-mile information gap that keeps entitlements unclaimed. |
| **SDG 4 — Quality Education** | Surfaces post-matric scholarships for girls leaving school after 10th/12th — the exact dropout moment the scholarship test case demonstrates. |
| **SDG 10 — Reduced Inequalities** | Language and literacy become irrelevant inputs; a rural Tamil speaker with no English and no reading gets the same verified answer as a city user. |
| **SDG 3 — Good Health** (supporting) | Maternity benefit and Ayushman Bharat path-finding, spoken in the mother's own language. |
| **SDG 8 — Decent Work** (supporting) | Lakhpati Didi / Mudra / SHG routes into self-employment and small enterprise for women. |

### Core Innovation
- **Voice-in / Voice-out, no literacy prerequisite.** The user never types, reads, scrolls, or
  navigates a portal. One button, one question, one spoken answer.
- **Web-grounded real-time verification.** Every claim is sourced from a live crawl of
  `.gov.in` portals at the moment of the question, so a scheme change or a closed budget cannot
  silently make the answer wrong.
- **Jargon-to-dialect translation as a product surface.** Administrative English is not shortened,
  it is *re-asked* in Tamil/Hindi kinship language ("Akka, Didi") with a 3-sentence TTS script.
- **Retrieval-shaped prompts for low-literacy speech.** A dedicated query-transformer converts
  broken, filler-heavy rural speech into portal-grade search strings, which is the accuracy unlock
  most voice assistants miss.

### Technical Edge
| Dimension | Sakhi AI approach |
| :--- | :--- |
| Model | `gemini-2.5-flash` — low-latency voice-turn inference, no quality drop on structured extraction. |
| Grounding | `types.Tool(google_search=types.GoogleSearch())` live retrieval + `grounding_metadata` citation capture. |
| Structure | Strict `response_schema` → guaranteed JSON contract for the visual card; no parsing heuristics. |
| Latency | Single grounded call per question; no multi-agent debate, no vector store to go stale. |
| Anti-hallucination | Low temperature, verified-domain filter, mandatory source list, `confidence` field, retry with backoff. |
| Failure UX | Errors are spoken as encouragement in the user's language. No error string ever reaches the screen. |

### Why judges should care
Most "AI for rural India" submissions stop at a chatbot. Sakhi AI is judged on the last 10% —
the mic size, the badge colours, the spoken script's warmth, and the fact that a wrong answer is
visibly marked as unverified. The interface *is* the inclusion strategy.

---

## 3. Scalability Roadmap

| Phase | Horizon | Build | Outcome |
| :--- | :--- | :--- | :--- |
| **P0 — Prototype (done)** | 4 hours | Grounded FastAPI + single-button voice PWA, Tamil/Hindi | Judges see a working end-to-end verified answer. |
| **P1 — Dialect depth** | 4 weeks | Bhashini ASR/TTS for 8 regional languages, code-switched utterances, per-state document and office vocabularies | Rural speech in the local dialect is understood without training. |
| **P2 — Scheme graph** | 8 weeks | Nightly crawl + embedding index of myscheme.gov.in, pib.gov.in and 30 state portals; eligibility pre-check from Aadhaar-blocked (consent-only) data | Answers are instant and state-accurate; "am I eligible?" becomes a yes/no check, not a search. |
| **P3 — WhatsApp voice-note bot** | 3 months | Same engine behind a WhatsApp Business webhook: forward a voice note, receive a voice note + document checklist | Reaches users with no app install and no data plan beyond voice notes. |
| **P4 — Toll-free IVR dialer** | 6 months | Telephony provider + streaming STT/TTS on the existing engine, local-language prompts, DTMF-free fully voice navigation | Zero-smartphone access. Highest-reach, lowest-infrastructure option. |
| **P5 — Federated state rollout** | 12 months | State nodal officers, helpline escalation ("call a human"), application-status tracking, audit dashboard for officials | Moves from information to completed applications, with accountability. |

**North-star metric:** percentage of eligible women who successfully complete the first
application step within 7 days of asking — not monthly active users.

---

## 4. Fallback Plan If the Live Demo Fails
1. Network drops → switch to the text fallback box, narrate that the same path runs in production.
2. Gemini latency spike → pre-record the 40-second Scenario C run and narrate over it; the JSON
   and card are already rendered in the recording.
3. Mic permission denied in the judge's browser → hand the judge the phone and let them speak; the
   Tamil demo line is printed in this document for them to read aloud.
