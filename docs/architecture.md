# Architecture — Onboarding & Offboarding Automation

Detailed breakdown of the workflow logic, node by node. Use this to explain the build in an interview or rebuild it from scratch.

---

## Design Principles

1. **One trigger, two paths** — A single entry point handles both onboarding and offboarding, branched by event type. Less to maintain.
2. **Role-based, not per-user** — Access is granted by mapping a role to a group, not by manually picking apps. Adding a new role = updating one mapping.
3. **Notify + log on every run** — Nothing happens silently. Every execution produces a Slack message and an audit row.
4. **Fail loud** — Errors route to an alert, not a silent drop.

---

## Trigger Layer

**Node: Webhook (or n8n Form Trigger)**

Accepts a JSON payload:

```json
{
  "event": "onboard",
  "employee": {
    "first_name": "Jane",
    "last_name": "Doe",
    "personal_email": "jane.doe@example.com",
    "role": "Sales - AE",
    "department": "Sales",
    "manager_email": "manager@company.com",
    "start_date": "2026-07-01"
  }
}
```

`event` is either `onboard` or `offboard`. For offboarding, only the identifier and last day are required.

---

## Routing Layer

**Node: Switch**

Reads `event` and routes to the onboarding branch or offboarding branch.

---

## Onboarding Branch

| Step | Node | Action |
|------|------|--------|
| 1 | Set / Function | Build username + email from naming convention (e.g., `first.last@company.com`) |
| 2 | HTTP Request / Okta | Create user account |
| 3 | HTTP Request / Okta | Add user to role-based group(s) using a role→group map |
| 4 | HTTP Request / Google | Create mailbox / Workspace account if separate |
| 5 | Jira | Create onboarding checklist (device, MDM enrollment, training) |
| 6 | Slack | Post to #it-onboarding with the new hire summary |
| 7 | Email | Send manager a confirmation + first-day checklist |
| 8 | Google Sheets | Append audit row (who, what, when, by which workflow run) |

**Role → group mapping** lives in a single Set node or an external lookup, so access logic is centralized:

```
Sales - AE      → [Salesforce-Users, Gong-Users, Slack-Sales, Google-Sales]
Engineering     → [GitHub-Eng, Jira-Eng, Slack-Eng, Google-Eng]
...
```

---

## Offboarding Branch

| Step | Node | Action |
|------|------|--------|
| 1 | HTTP Request / Okta | Suspend user account |
| 2 | HTTP Request / Okta | Remove from all groups (revoke SaaS access) |
| 3 | Jira | Create offboarding tasks (device recovery, asset return, license reclaim) |
| 4 | Slack | Alert #it-offboarding |
| 5 | Email | Notify manager + IT asset owner |
| 6 | Google Sheets | Append audit row |

> Suspending rather than deleting preserves data and supports a clean handoff while immediately killing access — the security-correct default.

---

## Notification + Logging Layer (shared)

Both branches converge into:

- **Slack node** — formatted summary message
- **Google Sheets node** — audit row: `timestamp | event | employee | role | actions taken | run_id`

---

## Error Handling

- An **Error Trigger** workflow catches failures and posts to a #it-alerts Slack channel with the failed node + payload, so a half-completed onboarding is visible immediately.

---

## Security Notes

- All credentials stored in n8n's credential store, never in node parameters.
- This repo ships with **placeholders only**.
- Offboarding revokes access first, before any slower cleanup steps run.
- Audit log supports periodic access reviews.

---

## Planned AI Enhancement

Insert a Claude / ChatGPT node (via HTTP Request to the API) after step 5 of onboarding:

- **Input:** role + department + manager name
- **Prompt:** built with the ICC framework (Instruction / Context / Constraints)
- **Output:** a personalized welcome message + role-specific first-week resource list
- **Then:** pass to the email/Slack node

This is where no-code automation meets AI — the workflow handles the mechanics, the model handles the human-readable, context-specific content.
