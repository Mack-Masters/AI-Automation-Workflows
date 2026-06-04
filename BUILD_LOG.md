# Build Log — AI Automation Workflow Project

A running journal of building this project end to end: environment setup, troubleshooting, the workflow build, and publishing to GitHub. Kept so the process is reproducible and so I can walk through my reasoning, not just the result.

**Goal:** Build a working onboarding automation in n8n (trigger → AI welcome message → log → notify), self-hosted, then publish it with documentation.

---

## Day 1 — Environment Setup & Troubleshooting

### What I set out to do
Get n8n running locally (self-hosted) after my cloud trial ended.

### What happened
Ran `npx n8n` and hit a wall of npm warnings. Separated the signal from the noise:
- Most warnings were `deprecated` notices on sub-dependencies (glob, uuid, tar, etc.) — normal, ignorable.
- The real blocker was `EBADENGINE`: n8n requires Node `^18.19.0 || >=20.6.0`, but my machine was on **Node v16.17.0**.

### Diagnosis
```
node -v        → v16.17.0
which node     → /usr/local/bin/node
command -v nvm → (nothing — no version manager installed)
```
Conclusion: a single, outdated Node install with no version manager. n8n would not run on it.

### Fix
Installed the current Node LTS via the official macOS `.pkg` installer (simplest, lowest-risk path vs. setting up nvm under time pressure).
- Result: **Node v24.16.0**, npm v11.13.0, installed to `/usr/local/bin` (already on `$PATH`).
- Reopened terminal, confirmed `node -v` → v24.16.0.
- Re-ran `npx n8n` — engine warnings gone, n8n booted to `http://localhost:5678`.

### Takeaway
The error volume looked alarming but only one line mattered. Isolating the actual blocker (version mismatch) from dependency noise is the core of troubleshooting. Noted that a version manager (nvm) would prevent this recurring — a future improvement, not a blocker today.

---

## Day __ — Building the Workflow

### Nodes built
- [ ] Form Trigger — fields: First Name, Last Name, Role, Department, Manager Email
- [ ] Edit Fields — build company email from naming convention + timestamp
- [ ] HTTP Request → Claude API — generate role-specific welcome message (ICC prompt)
- [ ] Google Sheets — append audit row
- [ ] Slack / Gmail — notify manager

### Decisions & notes
*(fill in as you build: what worked, what you changed, why)*
-
-

### Problems hit & how I solved them
*(this is the most valuable section for an interview — capture real debugging)*
-
-

---

## Day __ — Testing

### Test runs
*(record what you submitted and what came out)*
- Input:
- Result in sheet:
- Notification received:

### Things I fixed after testing
-

---

## Day __ — Publishing to GitHub

### Steps
- [ ] Exported workflow JSON from n8n (`⋯ → Download`)
- [ ] Scrubbed JSON: removed API keys, real emails, live webhook/form URLs (replaced with placeholders)
- [ ] Trimmed README + architecture doc to match what was actually built
- [ ] Uploaded files to repo (`Add file → Upload files`)
- [ ] Pinned the repo on my profile

### Final repo structure
```
AI-Automation-Workflows/
├── README.md
├── BUILD_LOG.md          ← this file
├── docs/architecture.md
├── examples/sample-payload.json
└── workflows/onboarding.json
```

---

## Reflection (for the interview)

**What this project demonstrates:**
- No-code/low-code automation (n8n) — direct JD match
- AI integration via API (Claude) using a structured prompt framework (ICC)
- Self-hosting and environment troubleshooting (Node version conflict)
- Documentation discipline — README, architecture, and this build log

**What I'd do next / in production:**
- Replace Sheets logging with real Okta/Google provisioning
- Add the offboarding branch with automatic access revocation
- Add error handling that alerts on failed runs
- Manager-approval gate before provisioning

**One-line summary I can say out loud:**
"I built it end to end on my own machine, hit a real Node version conflict, diagnosed and fixed it, then shipped a working trigger→AI→log→notify automation with full docs — and the architecture notes show how I'd extend it to production identity systems."
