# Employee Onboarding & Offboarding Automation (n8n)

An n8n workflow that automates the repetitive steps of employee onboarding and offboarding — account provisioning, task creation, notifications, and tracking — so IT spends less time on manual setup and nothing gets missed.

> Built to mirror real enterprise IT operations: identity provisioning, SaaS access, MDM enrollment, and offboarding access removal.

---

## The Problem

Onboarding and offboarding are high-frequency, high-risk, manual tasks. In a typical IT environment each new hire requires:

- Account creation across multiple systems (email, SSO, SaaS apps)
- Group/role assignment for correct access
- Device provisioning and MDM enrollment
- A welcome/checklist communication
- Tracking so nothing falls through

Done by hand, this is slow, inconsistent, and error-prone. Missed offboarding steps are also a **security risk** — orphaned accounts are a common audit finding.

This workflow standardizes the process and removes the manual clicking.

---

## What It Does

### Onboarding flow
1. **Trigger** — New hire submitted via form / webhook (name, role, department, start date, manager).
2. **Create identity** — Generate the user account and assign to the correct role-based group.
3. **Provision SaaS access** — Add the user to the apps their role requires.
4. **Create onboarding tasks** — Generate a checklist (device, MDM enrollment, training) in the task system.
5. **Notify** — Post to the IT Slack channel and email the manager a confirmation + checklist.
6. **Log** — Write a record to a tracking sheet for audit/visibility.

### Offboarding flow
1. **Trigger** — Departure submitted (user, last day).
2. **Suspend access** — Disable the account and revoke SaaS group memberships.
3. **Create offboarding tasks** — Device recovery, asset return, license reclamation.
4. **Notify** — Alert IT and the manager.
5. **Log** — Record completion for audit.

---

## Architecture

```
                        ┌──────────────────┐
   New Hire / Departure │   Trigger        │
   (Form or Webhook) ──▶│   (Webhook node) │
                        └────────┬─────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Branch: Onboard /      │
                    │   Offboard (Switch node) │
                    └──────┬────────────┬──────┘
                           │            │
              ┌────────────▼──┐   ┌─────▼────────────┐
              │ Identity:     │   │ Identity:        │
              │ create user + │   │ suspend user +   │
              │ assign groups │   │ revoke access    │
              └───────┬───────┘   └────────┬─────────┘
                      │                    │
              ┌───────▼───────┐    ┌────────▼────────┐
              │ Create tasks  │    │ Create tasks    │
              │ (checklist)   │    │ (recovery)      │
              └───────┬───────┘    └────────┬────────┘
                      │                     │
                      └─────────┬───────────┘
                                │
                   ┌────────────▼────────────┐
                   │ Notify (Slack + email)  │
                   └────────────┬────────────┘
                                │
                   ┌────────────▼────────────┐
                   │ Log to tracking sheet   │
                   └─────────────────────────┘
```

---

## Tools Used

| Layer | Tool | Notes |
|-------|------|-------|
| Orchestration | **n8n** | Self-hosted, no-code/low-code workflow engine |
| Trigger | Webhook / Form | Accepts new-hire and departure events |
| Identity | Okta / Google Workspace | User + group provisioning (role-based access) |
| Notifications | Slack + Email | IT channel alert + manager confirmation |
| Tasking | Jira / checklist | Generated onboarding/offboarding tasks |
| Logging | Google Sheets | Audit + visibility record |

> This repo uses **placeholder credentials only**. No API keys, tokens, or company data are included. Swap in your own connections to run it.

---

## Why This Matters (the IT-ops angle)

- **Reduces manual work** — replaces a multi-system manual checklist with one trigger.
- **Improves consistency** — every hire/departure follows the same steps.
- **Strengthens security** — offboarding revokes access automatically, reducing orphaned-account risk and supporting access reviews.
- **Creates an audit trail** — every run is logged.

This mirrors the kind of internal automation that lets a lean IT team scale support without scaling headcount.

---

## Repo Contents

```
.
├── README.md                      # This file
├── workflows/
│   ├── onboarding.json            # Sanitized n8n export
│   └── offboarding.json           # Sanitized n8n export
├── docs/
│   └── architecture.md            # Detailed flow + node breakdown
└── examples/
    └── sample-payload.json        # Example trigger payload (dummy data)
```

---

## How to Run

1. Import the workflow JSON into your n8n instance (`Workflows → Import from File`).
2. Open each node with a credential placeholder and connect your own accounts (Okta/Google, Slack, Jira, Sheets).
3. Send a test payload to the webhook URL (see `examples/sample-payload.json`).
4. Confirm the Slack notification, task creation, and log entry.

---

## Roadmap

- [ ] Add AI step (Claude / ChatGPT via API) to auto-draft a personalized welcome message from the new hire's role + department
- [ ] Add manager-approval gate before provisioning
- [ ] Add Slack slash-command trigger for self-service offboarding requests

---

*Built by Mack McFarland — IT operations + AI automation.* `github.com/Mack-Masters`
