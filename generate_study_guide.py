#!/usr/bin/env python3
"""Generate Okta Interview Study Guide PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import datetime

# ── Palette ──────────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1A2B4A")
MID_BLUE    = colors.HexColor("#2563EB")
LIGHT_BLUE  = colors.HexColor("#DBEAFE")
ACCENT      = colors.HexColor("#0EA5E9")
GRAY_DARK   = colors.HexColor("#374151")
GRAY_MID    = colors.HexColor("#6B7280")
GRAY_LIGHT  = colors.HexColor("#F3F4F6")
GOLD        = colors.HexColor("#F59E0B")
GREEN       = colors.HexColor("#10B981")
RED_SOFT    = colors.HexColor("#FEE2E2")
GREEN_SOFT  = colors.HexColor("#D1FAE5")
WHITE       = colors.white

PAGE_W, PAGE_H = letter
MARGIN = 0.75 * inch


# ── Page number footer ────────────────────────────────────────────────────────
def add_page_number(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(GRAY_MID)
    canvas_obj.drawRightString(PAGE_W - MARGIN, 0.45 * inch,
                                f"Page {doc.page}")
    canvas_obj.drawString(MARGIN, 0.45 * inch, "Okta Interview Study Guide  |  Confidential")
    canvas_obj.setStrokeColor(GRAY_LIGHT)
    canvas_obj.line(MARGIN, 0.6 * inch, PAGE_W - MARGIN, 0.6 * inch)
    canvas_obj.restoreState()


def first_page(canvas_obj, doc):
    pass  # cover page has no footer


# ── Style factory ─────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    s = {}

    s["cover_title"] = ParagraphStyle(
        "cover_title",
        fontName="Helvetica-Bold",
        fontSize=32,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=40,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub",
        fontName="Helvetica",
        fontSize=14,
        textColor=colors.HexColor("#BFDBFE"),
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    s["cover_date"] = ParagraphStyle(
        "cover_date",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=GOLD,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    s["toc_title"] = ParagraphStyle(
        "toc_title",
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=DARK_BLUE,
        spaceBefore=20,
        spaceAfter=12,
    )
    s["toc_entry"] = ParagraphStyle(
        "toc_entry",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRAY_DARK,
        leftIndent=0,
        spaceAfter=4,
        leading=14,
    )
    s["toc_entry_sub"] = ParagraphStyle(
        "toc_entry_sub",
        fontName="Helvetica",
        fontSize=9,
        textColor=GRAY_MID,
        leftIndent=16,
        spaceAfter=2,
        leading=12,
    )
    s["section_header"] = ParagraphStyle(
        "section_header",
        fontName="Helvetica-Bold",
        fontSize=17,
        textColor=WHITE,
        spaceBefore=6,
        spaceAfter=6,
        leading=22,
        leftIndent=8,
    )
    s["subsection_header"] = ParagraphStyle(
        "subsection_header",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=DARK_BLUE,
        spaceBefore=10,
        spaceAfter=4,
        leading=16,
    )
    s["body"] = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRAY_DARK,
        leading=15,
        spaceAfter=4,
        alignment=TA_JUSTIFY,
    )
    s["bullet"] = ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRAY_DARK,
        leading=15,
        leftIndent=18,
        firstLineIndent=-12,
        spaceAfter=3,
    )
    s["bullet2"] = ParagraphStyle(
        "bullet2",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=GRAY_DARK,
        leading=14,
        leftIndent=34,
        firstLineIndent=-12,
        spaceAfter=2,
    )
    s["required_label"] = ParagraphStyle(
        "required_label",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=WHITE,
        alignment=TA_CENTER,
    )
    s["qa_q"] = ParagraphStyle(
        "qa_q",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        textColor=DARK_BLUE,
        spaceBefore=10,
        spaceAfter=3,
        leading=15,
    )
    s["qa_a"] = ParagraphStyle(
        "qa_a",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRAY_DARK,
        leading=15,
        spaceAfter=4,
        leftIndent=12,
        alignment=TA_JUSTIFY,
    )
    s["card_header"] = ParagraphStyle(
        "card_header",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=DARK_BLUE,
        spaceAfter=3,
        leading=15,
    )
    s["card_body"] = ParagraphStyle(
        "card_body",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=GRAY_DARK,
        leading=14,
        spaceAfter=2,
    )
    s["interviewer_q"] = ParagraphStyle(
        "interviewer_q",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=DARK_BLUE,
        spaceBefore=8,
        spaceAfter=2,
        leading=15,
    )
    s["interviewer_note"] = ParagraphStyle(
        "interviewer_note",
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        textColor=GRAY_MID,
        leading=14,
        leftIndent=12,
        spaceAfter=4,
    )
    return s


# ── Helper flowables ──────────────────────────────────────────────────────────
def section_banner(title, styles, required=False):
    """Dark blue banner for section headers."""
    label = "  [Required Skill]" if required else ""
    text = f"{title}{label}"
    data = [[Paragraph(text, styles["section_header"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return [Spacer(1, 10), t, Spacer(1, 8)]


def bullet_item(text, styles, level=1):
    style = styles["bullet"] if level == 1 else styles["bullet2"]
    bullet_char = "•" if level == 1 else "◦"
    return Paragraph(f"{bullet_char}&nbsp;&nbsp;{text}", style)


def sub_header(text, styles):
    return [Paragraph(text, styles["subsection_header"])]


def hr(color=LIGHT_BLUE):
    return HRFlowable(width="100%", thickness=1, color=color, spaceAfter=6, spaceBefore=6)


def note_box(text, styles, bg=LIGHT_BLUE):
    data = [[Paragraph(text, styles["body"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN - 0.2 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [3]),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 4)]


def qa_pair(q, a, styles):
    return [
        Paragraph(f"Q: {q}", styles["qa_q"]),
        Paragraph(f"A: {a}", styles["qa_a"]),
        hr(GRAY_LIGHT),
    ]


# ── Cover page ────────────────────────────────────────────────────────────────
def build_cover(canvas_obj, doc):
    canvas_obj.saveState()
    # Full-page gradient background (dark blue → mid blue)
    canvas_obj.setFillColor(DARK_BLUE)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Accent stripe top
    canvas_obj.setFillColor(MID_BLUE)
    canvas_obj.rect(0, PAGE_H - 0.35 * inch, PAGE_W, 0.35 * inch, fill=1, stroke=0)

    # Accent stripe bottom
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.rect(0, 0, PAGE_W, 0.3 * inch, fill=1, stroke=0)

    # Decorative horizontal rule
    canvas_obj.setStrokeColor(GOLD)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(MARGIN, PAGE_H * 0.62, PAGE_W - MARGIN, PAGE_H * 0.62)

    canvas_obj.restoreState()


def cover_flowables(styles):
    date_str = "June 13, 2026"

    elems = []
    # Push content to vertical center-ish
    elems.append(Spacer(1, 2.2 * inch))
    elems.append(Paragraph("OKTA INTERVIEW", styles["cover_title"]))
    elems.append(Paragraph("STUDY GUIDE", styles["cover_title"]))
    elems.append(Spacer(1, 0.15 * inch))

    elems.append(Paragraph("Complete Technical Reference", styles["cover_sub"]))
    elems.append(Paragraph("IT Administrator · Identity & Access Management · MDM · Google Workspace", styles["cover_sub"]))
    elems.append(Spacer(1, 0.25 * inch))
    elems.append(Paragraph(f"Prepared: {date_str}", styles["cover_date"]))
    elems.append(Spacer(1, 0.15 * inch))
    elems.append(Paragraph("CONFIDENTIAL — FOR PERSONAL USE ONLY", ParagraphStyle(
        "cover_conf",
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.HexColor("#94A3B8"),
        alignment=TA_CENTER,
    )))
    return elems


# ── Table of Contents ─────────────────────────────────────────────────────────
def toc_page(styles):
    elems = []
    elems.append(Paragraph("Table of Contents", styles["toc_title"]))
    elems.append(hr(MID_BLUE))
    elems.append(Spacer(1, 6))

    sections = [
        ("1.", "Okta Onboarding Automation", True),
        ("2.", "Okta Offboarding", True),
        ("3.", "SAML vs SCIM", True),
        ("4.", "Integration Troubleshooting", True),
        ("5.", "RBAC Rule Logic", True),
        ("6.", "Google Workspace Administration", True),
        ("7.", "Microsoft 365 Exposure", False),
        ("8.", "MDM — macOS and Windows", True),
        ("9.", "Jira and Confluence", True),
        ("10.", "Asset Management and Procurement", True),
        ("11.", "Security Best Practices", True),
        ("12.", "Ticket Prioritization & Help Desk Communication", True),
        ("13.", "Interview Performance Tips", False),
        ("14.", "Quick Reference Card", False),
        ("15.", "Mock Q&A — Practice Questions with Model Answers", False),
        ("16.", "Questions to Ask the Interviewer", False),
    ]

    for num, title, req in sections:
        req_tag = ' <font color="#2563EB"><b>[Required]</b></font>' if req else ""
        elems.append(Paragraph(
            f'<b>{num}</b>&nbsp;&nbsp;{title}{req_tag}',
            styles["toc_entry"]
        ))

    elems.append(Spacer(1, 0.15 * inch))
    elems.append(note_box(
        "<b>How to use this guide:</b> Read sections 1–5 for deep Okta mastery. "
        "Review sections 6–12 for breadth across required skills. "
        "Drill the Mock Q&amp;A (section 15) aloud until answers flow naturally. "
        "Keep the Quick Reference Card (section 14) open during final review.",
        styles,
        bg=LIGHT_BLUE,
    )[0])
    return elems


# ══════════════════════════════════════════════════════════════════════════════
# SECTION CONTENT
# ══════════════════════════════════════════════════════════════════════════════

def section_1(styles):
    elems = []
    elems += section_banner("1. Okta Onboarding Automation (End to End)", styles, required=True)

    elems += sub_header("Overview", styles)
    elems.append(Paragraph(
        "Okta onboarding automation creates a seamless, repeatable workflow that begins the moment "
        "an employee record is created in your HRIS and ends with a staged laptop on day one. "
        "The goal is <b>zero manual steps for standard roles</b>.",
        styles["body"]
    ))

    elems += sub_header("Step 1 — HRIS as Source of Truth", styles)
    elems.append(bullet_item("<b>BambooHR</b> or <b>Workday</b> holds the canonical employee record", styles))
    elems.append(bullet_item("Fields that matter: name, email, department, title, location, start date, manager, employee type", styles))
    elems.append(bullet_item("HRIS is the trigger point — nothing in Okta should happen before HRIS confirms the hire", styles))

    elems += sub_header("Step 2 — Webhook / API Trigger", styles)
    elems.append(bullet_item("HRIS fires a <b>webhook</b> on new employee record creation (or status change to 'Active')", styles))
    elems.append(bullet_item("Webhook hits an automation layer: Okta Workflows, Workato, Zapier, or a custom middleware", styles))
    elems.append(bullet_item("Trigger fires N days before start date (commonly 2–5 business days) for staging time", styles))

    elems += sub_header("Step 3 — Data Mapping", styles)
    elems.append(bullet_item("Map HRIS fields → Okta user profile attributes", styles))
    elems.append(bullet_item("Examples: <b>department</b> → used in group rules, <b>location</b> → determines policy set, <b>employeeType</b> → contractor vs. FTE rules", styles))
    elems.append(bullet_item("Mapping must be exact — attribute drift causes group rule failures", styles))

    elems += sub_header("Step 4 — Automated Account Creation", styles)
    elems.append(bullet_item("Okta creates user profile via <b>SCIM provisioning</b> or API call from automation layer", styles))
    elems.append(bullet_item("Account is staged (not yet activated) until start date, or activated immediately depending on policy", styles))
    elems.append(bullet_item("Activation email fires on day one, or a temp password is delivered via manager", styles))

    elems += sub_header("Step 5 — Group Rules and RBAC Auto-Assignment", styles)
    elems.append(bullet_item("Okta <b>Group Rules</b> evaluate attribute conditions and assign groups automatically", styles))
    elems.append(bullet_item("Example rule: IF <b>department = Engineering</b> AND <b>employeeType = Employee</b> → assign group 'eng-team'", styles))
    elems.append(bullet_item("Groups map to app assignments — joining a group grants access to all apps assigned to that group", styles))
    elems.append(bullet_item("This is <b>RBAC at scale</b>: role defines access, not the individual", styles))

    elems += sub_header("Step 6 — Apps Outside RBAC (Manager Form Flow)", styles)
    elems.append(bullet_item("Some apps are sensitive or bespoke — not all roles get them automatically", styles))
    elems.append(bullet_item("Manager submits a request form (Jira ticket, Okta Workflow form, or Service Desk form)", styles))
    elems.append(bullet_item("IT reviews → approves → manually assigns or triggers provisioning", styles))
    elems.append(bullet_item("These exceptions should be tracked as tech debt — if a pattern emerges, build a group rule", styles))

    elems += sub_header("Step 7 — Manual Checklist Generation", styles)
    elems.append(bullet_item("Automation triggers a checklist in Jira or Service Desk for tasks that can't be automated", styles))
    elems.append(bullet_item("Examples: badge access, parking, building key card, desk assignment, hardware accessories", styles))
    elems.append(bullet_item("Checklist is assigned to the correct owner (facilities, IT, manager)", styles))

    elems += sub_header("Step 8 — Laptop Staging and First Day Prep", styles)
    elems.append(bullet_item("MDM (Kandji/Jamf for Mac, Intune for Windows) enrolls device during staging", styles))
    elems.append(bullet_item("Configuration profiles, required apps, and compliance policies push automatically", styles))
    elems.append(bullet_item("Laptop is named, tagged in asset management, and assigned to user record", styles))
    elems.append(bullet_item("Device is ready before day one — user boots up and Okta Verify enrollment is first prompt", styles))

    elems.append(Spacer(1, 6))
    elems += note_box(
        "<b>Key talking point:</b> The entire onboarding chain is triggered by a single HRIS event. "
        "IT's job is to build the automation once and monitor it — not to manually run it every time.",
        styles, bg=GREEN_SOFT
    )
    return elems


def section_2(styles):
    elems = []
    elems += section_banner("2. Okta Offboarding", styles, required=True)

    elems += sub_header("Core Framing", styles)
    elems.append(Paragraph(
        "<b>Offboarding is onboarding in reverse.</b> The same HRIS-to-Okta integration that provisions "
        "access deprovisions it. Speed is a security requirement — every hour between termination and "
        "account deactivation is an open window.",
        styles["body"]
    ))

    elems += sub_header("The Offboarding Cascade", styles)
    elems.append(bullet_item("<b>Step 1 — HRIS deactivation triggers the workflow</b>: HR marks employee as terminated", styles))
    elems.append(bullet_item("<b>Step 2 — Okta deactivates the account</b>: user can no longer authenticate to any Okta-federated app", styles))
    elems.append(bullet_item("<b>Step 3 — Group memberships removed</b>: RBAC rules no longer apply → all group-based app access revoked", styles))
    elems.append(bullet_item("<b>Step 4 — App access removed</b>: direct app assignments also removed; SCIM sends deprovisioning payload to each app", styles))
    elems.append(bullet_item("<b>Step 5 — Laptop lockdown</b>: MDM sends remote lock or wipe command; device marked 'pending return' in asset management", styles))
    elems.append(bullet_item("<b>Step 6 — Data preservation</b>: Google Drive/email forwarded or transferred per policy before deletion", styles))
    elems.append(bullet_item("<b>Step 7 — Account deletion or archival</b>: Okta account suspended for retention period, then deleted", styles))

    elems += sub_header("Why Speed Matters", styles)
    elems.append(bullet_item("Disgruntled employees may attempt data exfiltration in the gap between termination and deactivation", styles))
    elems.append(bullet_item("Compliance frameworks (SOC 2, ISO 27001) require documented, timely deprovisioning", styles))
    elems.append(bullet_item("Target: <b>account deactivated within 15 minutes of HR action</b>", styles))

    elems += sub_header("What to Watch For", styles)
    elems.append(bullet_item("Apps <b>not connected via SCIM</b> require manual deprovisioning — maintain a checklist", styles))
    elems.append(bullet_item("Shared accounts or service accounts the employee owned — rotate credentials immediately", styles))
    elems.append(bullet_item("Slack, GitHub, AWS — verify these are revoked even if not Okta-federated", styles))

    elems += note_box(
        "<b>Interview framing:</b> 'Offboarding is onboarding in reverse — the same HRIS trigger "
        "that created the account terminates it. The goal is to close every access door in one "
        "automated sweep, with a manual checklist for the exceptions.'",
        styles, bg=GREEN_SOFT
    )
    return elems


def section_3(styles):
    elems = []
    elems += section_banner("3. SAML vs SCIM", styles, required=True)

    elems += sub_header("SAML — Authentication Protocol", styles)
    elems.append(Paragraph(
        "<b>SAML (Security Assertion Markup Language)</b> is how Okta proves to an app that a user is "
        "who they say they are. It is an <b>authentication and authorization</b> protocol — not provisioning.",
        styles["body"]
    ))
    elems.append(bullet_item("<b>Okta acts as the Identity Provider (IdP)</b>; the app is the Service Provider (SP)", styles))
    elems.append(bullet_item("Flow: user logs in → Okta authenticates → Okta sends signed <b>XML assertion</b> to the app", styles))
    elems.append(bullet_item("App validates the assertion signature using Okta's <b>metadata/certificate</b>", styles))
    elems.append(bullet_item("If valid → user is granted access. If not → login fails", styles))
    elems.append(bullet_item("Setup requires exchanging metadata: download from Okta, upload to app (and vice versa)", styles))

    elems += sub_header("What Breaks SAML and How to Fix It", styles)
    elems.append(bullet_item("<b>Expired certificate</b>: Okta's signing cert has a validity period — download new metadata from Okta, re-upload to app", styles))
    elems.append(bullet_item("<b>Metadata mismatch</b>: SP metadata out of sync with Okta config — re-export and re-import both sides", styles))
    elems.append(bullet_item("<b>Clock skew</b>: SAML assertions have timestamps — servers more than a few minutes apart will reject assertions", styles))
    elems.append(bullet_item("<b>Attribute mapping error</b>: app expects specific claim names — verify in Okta app settings under 'SAML attributes'", styles))

    elems += sub_header("SCIM — Provisioning Protocol", styles)
    elems.append(Paragraph(
        "<b>SCIM (System for Cross-domain Identity Management)</b> is how Okta creates, updates, and "
        "deletes user accounts in downstream apps. It is <b>provisioning</b> — not authentication.",
        styles["body"]
    ))
    elems.append(bullet_item("<b>Okta pushes user data to the app</b> via SCIM API calls (JSON payloads)", styles))
    elems.append(bullet_item("On create: Okta sends user attributes → app creates account", styles))
    elems.append(bullet_item("On update: attribute change in Okta → SCIM payload updates the app", styles))
    elems.append(bullet_item("On deactivation: Okta sends deprovisioning call → app deactivates or deletes user", styles))
    elems.append(bullet_item("Requires a <b>SCIM bearer token</b> from the app — stored in Okta integration settings", styles))

    elems += sub_header("What Breaks SCIM and How to Fix It", styles)
    elems.append(bullet_item("<b>Expired token</b>: regenerate in the app, update in Okta integration → test provisioning", styles))
    elems.append(bullet_item("<b>Payload mapping drift</b>: app renamed an attribute field — verify field names in Okta's attribute mapping screen", styles))
    elems.append(bullet_item("<b>App-side permission error</b>: SCIM token may have lost scope — regenerate with correct permissions", styles))

    elems += sub_header("When to Use Each", styles)
    data = [
        ["", "SAML", "SCIM"],
        ["Purpose", "Authentication (who you are)", "Provisioning (creating/managing accounts)"],
        ["Direction", "App pulls assertion from Okta", "Okta pushes user data to app"],
        ["Protocol", "XML over HTTPS redirect", "REST API / JSON"],
        ["Used for", "SSO login flow", "Auto-create/update/deactivate users"],
        ["Common failure", "Expired cert / metadata mismatch", "Expired token / attribute mapping drift"],
    ]
    t = Table(data, colWidths=[1.3 * inch, 2.5 * inch, 2.5 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), DARK_BLUE),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("BACKGROUND",   (0, 1), (-1, -1), GRAY_LIGHT),
        ("BACKGROUND",   (0, 2), (-1, 2), WHITE),
        ("BACKGROUND",   (0, 4), (-1, 4), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GRAY_LIGHT]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("FONTNAME",     (0, 1), (0, -1), "Helvetica-Bold"),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("ALIGN",        (0, 0), (-1, 0), "CENTER"),
    ]))
    elems.append(Spacer(1, 6))
    elems.append(t)
    elems.append(Spacer(1, 6))
    return elems


def section_4(styles):
    elems = []
    elems += section_banner("4. Integration Troubleshooting — Step by Step", styles, required=True)

    elems += sub_header("The Diagnostic Framework", styles)
    elems.append(Paragraph(
        "When an app integration breaks, follow this sequence. <b>Start with logs before touching any configuration.</b> "
        "Changing settings before you understand the failure often makes diagnosis harder.",
        styles["body"]
    ))

    steps = [
        ("Step 1 — Check Okta System Logs",
         "Go to Reports → System Log. Filter by the affected app and the time the issue started. "
         "Ask: 'When exactly did it stop working? What changed around that time?' Look for authentication failures, "
         "provisioning errors, or policy changes."),
        ("Step 2 — Check SAML Assertions or SCIM Payloads",
         "For SAML: use the SAML Tracer browser extension or Okta's built-in diagnostic tools to capture the "
         "assertion. Verify the signature, the audience, and the attributes being sent. "
         "For SCIM: check the provisioning logs under the app's Provisioning tab for payload errors or 4xx/5xx responses."),
        ("Step 3 — Check Both Sides of the Integration",
         "Okta's logs show what it sent. The app's logs show what it received (or rejected). "
         "Common gap: Okta shows success, but app rejected it silently. Always check the app's own admin console or logs."),
        ("Step 4 — Replace Expired Cert or Token",
         "If SAML: download fresh metadata from Okta, re-upload to the SP. Download fresh SP metadata, re-upload to Okta. "
         "If SCIM: regenerate the API token in the app, update it in the Okta integration settings, then test provisioning."),
        ("Step 5 — Open Support Ticket in Parallel",
         "If the issue isn't resolved in 15–20 minutes of diagnosis, open a ticket with the app vendor OR Okta support "
         "in parallel while continuing to investigate. Don't wait until you're stuck to file the ticket."),
    ]
    for title, body in steps:
        elems.append(Paragraph(f"<b>{title}</b>", styles["subsection_header"]))
        elems.append(Paragraph(body, styles["body"]))
        elems.append(Spacer(1, 4))

    elems += note_box(
        "<b>Key principle:</b> 'Logs first, changes second.' Never reconfigure an integration based on a hunch. "
        "The logs will tell you exactly what failed and when — use them.",
        styles, bg=LIGHT_BLUE
    )
    return elems


def section_5(styles):
    elems = []
    elems += section_banner("5. RBAC Rule Logic", styles, required=True)

    elems += sub_header("Core Structure", styles)
    elems.append(Paragraph(
        "<b>RBAC (Role-Based Access Control)</b> in Okta is implemented through Group Rules. "
        "Group Rules evaluate user profile attributes and automatically assign users to groups — "
        "which then grant app access. The goal is <b>zero manual group membership</b>.",
        styles["body"]
    ))

    elems += sub_header("Rule Syntax", styles)
    elems.append(bullet_item("<b>IF</b> [attribute] <b>AND</b> [attribute] <b>→</b> assign to group", styles))
    elems.append(bullet_item("<b>IF</b> [attribute] <b>AND NOT</b> [attribute] <b>→</b> assign to group", styles))
    elems.append(bullet_item("Rules support: equals, contains, starts with, regex", styles))
    elems.append(bullet_item("Multiple conditions joined with AND / OR", styles))

    elems += sub_header("Real-World Examples", styles)
    examples = [
        ("Austin Engineering FTEs", "location = 'Austin' AND department = 'Engineering' AND employeeType != 'Contractor'"),
        ("All Contractors", "employeeType = 'Contractor'"),
        ("Sales Team — US Only", "department = 'Sales' AND countryCode = 'US'"),
        ("Managers Only", "title CONTAINS 'Manager' OR title CONTAINS 'Director'"),
        ("New Hires (first 90 days)", "daysFromHire <= 90  [requires custom attribute]"),
    ]
    data = [["Rule Name", "Condition Logic"]] + [[n, c] for n, c in examples]
    t = Table(data, colWidths=[2 * inch, 4.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), MID_BLUE),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GRAY_LIGHT]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("FONTNAME",     (0, 1), (0, -1), "Helvetica-Bold"),
    ]))
    elems.append(Spacer(1, 4))
    elems.append(t)
    elems.append(Spacer(1, 8))

    elems += sub_header("Why Manual Membership = Tech Debt", styles)
    elems.append(bullet_item("<b>Manual assignment drifts</b> — people leave groups they shouldn't, or stay in ones they should have left", styles))
    elems.append(bullet_item("Every manual membership is a future support ticket waiting to happen", styles))
    elems.append(bullet_item("Audits become painful when access can't be explained by a rule", styles))
    elems.append(bullet_item("<b>Rule of thumb:</b> if you can write a rule for it, you should", styles))

    elems += note_box(
        "<b>Exception handling:</b> When an edge case doesn't fit a rule, use a dedicated group (e.g., 'manual-overrides-app-name') "
        "and document who is in it and why. This keeps exceptions visible and auditable.",
        styles, bg=LIGHT_BLUE
    )
    return elems


def section_6(styles):
    elems = []
    elems += section_banner("6. Google Workspace Administration", styles, required=True)

    elems += sub_header("User Lifecycle Management", styles)
    elems.append(bullet_item("<b>Create</b>: Admin Console → Users → Add New User. Set OU, primary email, recovery email", styles))
    elems.append(bullet_item("<b>Suspend</b>: removes access without deleting data — standard for offboarding", styles))
    elems.append(bullet_item("<b>Delete</b>: permanent — always transfer Drive/Gmail data first. Requires confirmation step", styles))
    elems.append(bullet_item("Bulk operations: use CSV import for mass user creation during migrations or acquisitions", styles))

    elems += sub_header("Organizational Unit (OU) Structure", styles)
    elems.append(bullet_item("OUs organize users for applying different policies (e.g., 2FA exemptions, app access)", styles))
    elems.append(bullet_item("Typical structure: /Company → /Departments → /Contractors, /Employees", styles))
    elems.append(bullet_item("Policy inheritance: child OUs inherit parent settings unless overridden", styles))
    elems.append(bullet_item("OU changes take effect within minutes but can take up to 24 hours to fully propagate", styles))

    elems += sub_header("App Access Control", styles)
    elems.append(bullet_item("Apps are enabled/disabled per OU in Admin Console → Apps → Google Workspace / Additional Google Services", styles))
    elems.append(bullet_item("Third-party apps: control OAuth scopes and API access under Security → API Controls", styles))
    elems.append(bullet_item("<b>Google Groups</b> can be used to grant access to Shared Drives, calendar resources, and distribution lists", styles))

    elems += sub_header("Security Settings", styles)
    elems.append(bullet_item("<b>2-Step Verification enforcement</b>: Security → Authentication → 2-Step Verification → Enforce for all users", styles))
    elems.append(bullet_item("<b>Session controls</b>: set session length for Google services and third-party apps", styles))
    elems.append(bullet_item("<b>Login challenges</b>: suspicious activity detection can require additional verification", styles))
    elems.append(bullet_item("<b>Password policies</b>: minimum length, reuse rules, require strong password", styles))

    elems += sub_header("Shared Drives and Permissions", styles)
    elems.append(bullet_item("Shared Drives are owned by the org, not individuals — data persists after employee departure", styles))
    elems.append(bullet_item("Membership roles: Manager, Content Manager, Contributor, Viewer", styles))
    elems.append(bullet_item("Sharing policies: restrict external sharing at OU or org level", styles))
    elems.append(bullet_item("DLP policies can flag or block sharing of sensitive content", styles))

    elems += sub_header("Audit Logs and Reporting", styles)
    elems.append(bullet_item("Admin Console → Reporting → Audit → Admin (admin actions), Login (auth events), Drive (file activity)", styles))
    elems.append(bullet_item("Alert Center for security-critical events (suspicious login, data exfiltration signals)", styles))
    elems.append(bullet_item("BigQuery export for long-term log retention and custom queries", styles))

    elems += sub_header("Integration with Okta", styles)
    elems.append(bullet_item("Google Workspace integrates with Okta via <b>SAML</b> (SSO) and <b>SCIM</b> (provisioning)", styles))
    elems.append(bullet_item("Okta provisions/deprovisions users directly into Google Workspace", styles))
    elems.append(bullet_item("Google OU assignment can be driven by Okta group membership via SCIM attribute mapping", styles))
    elems.append(bullet_item("Okta becomes the IdP — Google authentication is delegated to Okta Verify/MFA", styles))
    return elems


def section_7(styles):
    elems = []
    elems += section_banner("7. Microsoft 365 Exposure", styles, required=False)

    elems += sub_header("M365 Admin Center Basics", styles)
    elems.append(bullet_item("<b>User management</b>: create, edit, delete users; reset passwords; assign licenses", styles))
    elems.append(bullet_item("<b>License assignment</b>: assign M365 Business/Enterprise licenses per user or group", styles))
    elems.append(bullet_item("<b>Groups</b>: Microsoft 365 Groups, Security Groups, Distribution Lists — each has different capabilities", styles))
    elems.append(bullet_item("<b>Exchange admin</b>: mailbox management, shared mailboxes, mail flow rules", styles))

    elems += sub_header("Azure AD / Entra ID Fundamentals", styles)
    elems.append(bullet_item("<b>Azure Active Directory</b> (now Entra ID) is Microsoft's cloud identity platform — analogous to Okta", styles))
    elems.append(bullet_item("Supports SAML, OIDC, OAuth 2.0 for SSO to apps", styles))
    elems.append(bullet_item("<b>Conditional Access policies</b>: require MFA, block legacy auth, restrict by location or device compliance", styles))
    elems.append(bullet_item("<b>Groups-based licensing</b>: assign licenses via group membership (mirrors RBAC concept from Okta)", styles))
    elems.append(bullet_item("<b>App registrations</b>: register custom apps for SSO/API access", styles))

    elems += sub_header("Similarities vs Google Workspace", styles)
    data = [
        ["Concept", "Google Workspace", "Microsoft 365 / Entra ID"],
        ["User management", "Admin Console → Users", "M365 Admin Center / Entra ID"],
        ["Groups for access", "Google Groups / OUs", "Security Groups / M365 Groups"],
        ["SSO federation", "SAML via Okta IdP", "SAML/OIDC via Okta or Entra ID"],
        ["MDM integration", "Android Enterprise / BeyondCorp", "Intune / Endpoint Manager"],
        ["Audit logs", "Admin Audit Log", "Unified Audit Log / Entra Sign-ins"],
        ["MFA enforcement", "2SV policy in Admin Console", "Conditional Access in Entra ID"],
    ]
    t = Table(data, colWidths=[1.5 * inch, 2.5 * inch, 2.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), DARK_BLUE),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GRAY_LIGHT]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("FONTNAME",     (0, 1), (0, -1), "Helvetica-Bold"),
    ]))
    elems.append(Spacer(1, 6))
    elems.append(t)
    elems.append(Spacer(1, 8))

    elems += note_box(
        "<b>Key talking point:</b> 'My primary experience is with Google Workspace and Okta, but the "
        "admin concepts transfer directly. User lifecycle, group-based access, MFA enforcement, and "
        "audit logging work the same way — just different consoles. I'm comfortable picking up M365 quickly.'",
        styles, bg=LIGHT_BLUE
    )
    return elems


def section_8(styles):
    elems = []
    elems += section_banner("8. MDM — macOS and Windows", styles, required=True)

    elems += sub_header("macOS MDM — Kandji and Jamf", styles)
    elems.append(bullet_item("<b>Kandji</b>: modern, blueprint-based MDM. Each blueprint = a set of profiles and enforcements for a device group", styles))
    elems.append(bullet_item("<b>Jamf Pro</b>: enterprise-grade, highly configurable. Uses policies, scripts, and configuration profiles", styles))
    elems.append(bullet_item("<b>Configuration profiles</b>: enforce Wi-Fi, VPN, FileVault encryption, screen lock, software update restrictions", styles))
    elems.append(bullet_item("<b>App deployment</b>: push apps silently via MDM catalog (Kandji) or Self Service (Jamf) — no user action required", styles))
    elems.append(bullet_item("<b>Enforcement policies</b>: require OS version minimums, block USB storage, enforce disk encryption", styles))
    elems.append(bullet_item("<b>Scripts</b>: run shell scripts on enrollment, on schedule, or on trigger (Jamf policies)", styles))

    elems += sub_header("Windows MDM — Microsoft Intune", styles)
    elems.append(bullet_item("<b>Intune</b>: Microsoft's cloud-based MDM, integrated with Entra ID / Azure AD", styles))
    elems.append(bullet_item("<b>Device enrollment</b>: Azure AD join + Intune enrollment during Windows Autopilot or manual setup", styles))
    elems.append(bullet_item("<b>Compliance policies</b>: require BitLocker, antivirus, minimum OS version, password complexity", styles))
    elems.append(bullet_item("<b>Configuration profiles</b>: push registry settings, Wi-Fi, VPN, Edge browser settings", styles))
    elems.append(bullet_item("<b>App deployment</b>: deploy Win32 apps, MSI packages, or Microsoft Store apps", styles))
    elems.append(bullet_item("<b>Conditional Access integration</b>: non-compliant devices can be blocked from M365 resources", styles))

    elems += sub_header("Device Enrollment Workflows", styles)
    elems.append(bullet_item("<b>User-initiated</b>: user enrolls device manually via Company Portal or MDM profile download", styles))
    elems.append(bullet_item("<b>Zero-touch (macOS)</b>: ABM (Apple Business Manager) + Kandji/Jamf. Device purchased, added to ABM, MDM server assigned. On first boot → MDM enrollment automatic", styles))
    elems.append(bullet_item("<b>Zero-touch (Windows)</b>: Windows Autopilot. Device hardware hash registered. Shipped directly to user. User powers on → Azure AD join + Intune auto-enrolls", styles))
    elems.append(bullet_item("Zero-touch requires vendor coordination: Apple Authorized Reseller or Microsoft partner for hardware hash upload", styles))

    elems += sub_header("Offboarding Device Actions", styles)
    elems.append(bullet_item("<b>Remote lock</b>: secure the device immediately, display contact info on screen", styles))
    elems.append(bullet_item("<b>Remote wipe</b>: factory reset, removes all data — use for departing employees or lost devices", styles))
    elems.append(bullet_item("<b>Selective wipe (BYOD)</b>: removes only corporate apps/data, leaves personal content intact", styles))
    elems.append(bullet_item("<b>Remove from MDM</b>: unenroll device before reassigning; re-enroll under new user", styles))

    elems += sub_header("Asset Tracking in MDM", styles)
    elems.append(bullet_item("Both Kandji and Jamf display hardware info: serial number, model, OS version, last check-in time", styles))
    elems.append(bullet_item("Serial number = primary asset identifier — sync to asset management system", styles))
    elems.append(bullet_item("Use MDM inventory as the source of truth for deployed device status", styles))
    return elems


def section_9(styles):
    elems = []
    elems += section_banner("9. Jira and Confluence", styles, required=True)

    elems += sub_header("Jira — Ticket Management", styles)
    elems.append(bullet_item("<b>Queue management</b>: organize IT tickets by type, priority, and SLA tier", styles))
    elems.append(bullet_item("<b>Workflow states</b>: Open → In Progress → Pending → Resolved → Closed", styles))
    elems.append(bullet_item("<b>Priority tiers</b>: P1 (critical/business-down) → P2 (high impact) → P3 (standard) → P4 (low)", styles))
    elems.append(bullet_item("<b>SLA awareness</b>: track time-to-first-response and time-to-resolution. Escalate before breach", styles))
    elems.append(bullet_item("<b>Components and labels</b>: tag tickets by system (Okta, MDM, Google) for reporting and pattern detection", styles))
    elems.append(bullet_item("<b>Automation rules</b>: auto-assign by issue type, auto-transition on comment, notify on SLA breach", styles))
    elems.append(bullet_item("<b>Subtasks</b>: break complex onboarding/offboarding tickets into trackable steps", styles))

    elems += sub_header("Confluence — Documentation", styles)
    elems.append(bullet_item("<b>Knowledge base structure</b>: Space → Page hierarchy. Organize by team and topic", styles))
    elems.append(bullet_item("<b>Runbooks</b>: step-by-step operational procedures for common IT tasks", styles))
    elems.append(bullet_item("<b>SOPs</b>: Standard Operating Procedures — document once, reference forever", styles))
    elems.append(bullet_item("<b>Onboarding docs</b>: new employee guides, IT setup checklists, software request process", styles))
    elems.append(bullet_item("<b>Incident post-mortems</b>: document what broke, why, how it was fixed, and what prevents recurrence", styles))
    elems.append(bullet_item("<b>Templates</b>: create page templates for runbooks, post-mortems, and change requests for consistency", styles))

    elems += sub_header("Using Both Together for IT Ops", styles)
    elems.append(bullet_item("Link Jira tickets to Confluence runbooks — ticket includes a 'how-to' link for the responder", styles))
    elems.append(bullet_item("Post-incident: close the Jira ticket AND write/update the Confluence runbook", styles))
    elems.append(bullet_item("Onboarding/offboarding: Jira = the checklist instance; Confluence = the process documentation", styles))

    elems += note_box(
        "<b>Key talking point:</b> 'Documentation is a force multiplier. Every runbook I write means the next "
        "person who hits that issue resolves it in 5 minutes instead of 45. Good docs also make it safe to "
        "take a vacation.'",
        styles, bg=GREEN_SOFT
    )
    return elems


def section_10(styles):
    elems = []
    elems += section_banner("10. Asset Management and Procurement", styles, required=True)

    elems += sub_header("Hardware Lifecycle", styles)
    stages = [
        ("Procurement", "Submit purchase order, vendor selection, budget approval. Standard: MacBook Pro/Air for engineering, MacBook Air for general staff, Windows for specific roles"),
        ("Receiving and Tagging", "Verify serial numbers, apply asset tags, log in asset management system (Snipe-IT, Jamf, or spreadsheet)"),
        ("Staging", "Enroll in MDM, apply configuration profiles, install required apps, name device per naming convention"),
        ("Deployment", "Assign to user in MDM and asset system, deliver with accessories, confirm enrollment and policy compliance"),
        ("Refresh", "Typically on 3–4 year cycle. Evaluate device performance, OS support end-of-life, battery health"),
        ("Offboarding", "Collect from departing employee, wipe, unenroll from MDM, mark 'available' or 'decommissioned' in asset system"),
    ]
    for stage, desc in stages:
        elems.append(bullet_item(f"<b>{stage}:</b> {desc}", styles))

    elems += sub_header("Tracking and Inventory", styles)
    elems.append(bullet_item("Serial number is the canonical asset identifier — use it everywhere", styles))
    elems.append(bullet_item("<b>MDM</b> provides real-time device state; <b>asset management system</b> tracks ownership and location history", styles))
    elems.append(bullet_item("Regular audits: reconcile MDM inventory against asset records quarterly", styles))
    elems.append(bullet_item("<b>Loaner management</b>: maintain a pool of spare devices. Track with check-out/check-in log", styles))

    elems += sub_header("Vendor Coordination", styles)
    elems.append(bullet_item("Maintain approved vendor list: Apple (direct or authorized reseller), Dell, Lenovo", styles))
    elems.append(bullet_item("For Apple: work with authorized reseller to register devices to ABM for zero-touch enrollment", styles))
    elems.append(bullet_item("Lead times matter — order 2–3 weeks before hire date for new headcount", styles))
    elems.append(bullet_item("Purchase orders: understand your org's approval threshold. Know when to loop in finance", styles))

    elems += note_box(
        "<b>Key talking point:</b> 'Asset management is an extension of onboarding and offboarding. "
        "The same automation that provisions access also triggers staging a device. The same offboarding "
        "workflow that revokes access triggers the device collection and wipe process.'",
        styles, bg=GREEN_SOFT
    )
    return elems


def section_11(styles):
    elems = []
    elems += section_banner("11. Security Best Practices", styles, required=True)

    elems += sub_header("MFA Enforcement", styles)
    elems.append(bullet_item("<b>Enforce MFA for all users, all apps, no exceptions</b> — including IT admins (especially IT admins)", styles))
    elems.append(bullet_item("Use Okta Verify with biometric or push — avoid SMS OTP for privileged accounts (SIM swap risk)", styles))
    elems.append(bullet_item("Authentication policies in Okta: require phishing-resistant MFA for admin access", styles))
    elems.append(bullet_item("Step-up authentication: require re-verification for sensitive operations (password reset, admin app access)", styles))

    elems += sub_header("Least Privilege Access Principle", styles)
    elems.append(bullet_item("Users get <b>only</b> the access their role requires — nothing more by default", styles))
    elems.append(bullet_item("Enforce through RBAC group rules — access requires a justification (role attribute)", styles))
    elems.append(bullet_item("Privileged access (admin roles, production systems) requires separate approval workflow", styles))
    elems.append(bullet_item("Periodic access reviews: verify that access is still justified quarterly or semi-annually", styles))

    elems += sub_header("Okta Authentication Policies", styles)
    elems.append(bullet_item("<b>Authentication policies</b>: define which MFA factors are required for which apps", styles))
    elems.append(bullet_item("<b>Device trust</b>: require managed device (MDM-enrolled) for access to sensitive apps", styles))
    elems.append(bullet_item("<b>Network zone restrictions</b>: block access from unexpected geolocations or allow only corporate IPs for admin console", styles))
    elems.append(bullet_item("<b>Session policies</b>: set session lifetime and idle timeout per application risk level", styles))

    elems += sub_header("Offboarding as a Security Event", styles)
    elems.append(bullet_item("Treat every offboarding as a potential security incident — act fast", styles))
    elems.append(bullet_item("Target: <b>Okta account deactivated within 15 minutes of HR notification</b>", styles))
    elems.append(bullet_item("Document time from termination to deactivation for compliance reporting", styles))
    elems.append(bullet_item("For involuntary terminations: have IT on standby — coordinate deactivation to coincide with the HR conversation", styles))

    elems += sub_header("Audit Logs and Access Reviews", styles)
    elems.append(bullet_item("Enable and retain Okta system logs (recommend 12-month retention minimum)", styles))
    elems.append(bullet_item("Regular log reviews: look for impossible travel, unusual login hours, privilege escalation attempts", styles))
    elems.append(bullet_item("Access review cadence: quarterly for privileged users, semi-annual for general access", styles))
    elems.append(bullet_item("Integrate logs with SIEM (Splunk, Datadog, Elastic) for alerting and correlation", styles))

    elems += sub_header("Zero Trust Framing", styles)
    elems.append(bullet_item("<b>Verify every user</b>: MFA on every authentication, no implicit trust", styles))
    elems.append(bullet_item("<b>Verify every device</b>: device trust policies — only managed, compliant devices access sensitive resources", styles))
    elems.append(bullet_item("<b>Verify every access request</b>: least privilege + just-in-time access for privileged roles", styles))
    elems.append(bullet_item("Network perimeter is gone — identity is the new perimeter", styles))
    return elems


def section_12(styles):
    elems = []
    elems += section_banner("12. Ticket Prioritization and Help Desk Communication", styles, required=True)

    elems += sub_header("Triaging Multiple Urgent Tickets", styles)
    elems.append(bullet_item("<b>First pass</b>: scan all new tickets in under 2 minutes. Identify any P1s (business-down, executive-blocked)", styles))
    elems.append(bullet_item("<b>Impact vs Urgency matrix</b>: High impact + High urgency = P1. High impact + Low urgency = P2. Triage accordingly", styles))
    elems.append(bullet_item("<b>Look for patterns first</b>: 10 tickets about email? Likely a systemic issue. Fix the root cause, not 10 individual tickets", styles))
    elems.append(bullet_item("<b>Acknowledge everything within 15 minutes</b>: even 'I received this and am looking into it' reduces anxiety and sets expectations", styles))
    elems.append(bullet_item("<b>Delegate or escalate</b>: if queue is overwhelming, surface to team lead and redistribute", styles))

    elems += sub_header("Impact vs Urgency Matrix", styles)
    data = [
        ["", "High Urgency", "Low Urgency"],
        ["High Impact", "P1 — Drop everything", "P2 — Address today"],
        ["Low Impact",  "P3 — Queue normally", "P4 — When capacity allows"],
    ]
    t = Table(data, colWidths=[1.5 * inch, 2.5 * inch, 2.5 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), DARK_BLUE),
        ("BACKGROUND",   (0, 0), (0, -1), DARK_BLUE),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("TEXTCOLOR",    (0, 0), (0, -1), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME",     (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9.5),
        ("BACKGROUND",   (1, 1), (1, 1), RED_SOFT),
        ("BACKGROUND",   (2, 1), (2, 1), LIGHT_BLUE),
        ("BACKGROUND",   (1, 2), (1, 2), LIGHT_BLUE),
        ("BACKGROUND",   (2, 2), (2, 2), GRAY_LIGHT),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
    ]))
    elems.append(Spacer(1, 4))
    elems.append(t)
    elems.append(Spacer(1, 8))

    elems += sub_header("Communicating with Executives", styles)
    elems.append(bullet_item("Executives want: <b>What happened, what you're doing, when it will be fixed</b>", styles))
    elems.append(bullet_item("Skip the technical cause — they don't need it and it erodes confidence", styles))
    elems.append(bullet_item("Lead with impact, not diagnosis", styles))

    elems += note_box(
        '<b>Template:</b> "Your [system] is [experiencing issue]. This is affecting [scope]. '
        'I am [action being taken] and expect resolution by [time]. '
        'In the meantime, here is your workaround: [simple step]."',
        styles, bg=LIGHT_BLUE
    )

    elems.append(Spacer(1, 4))
    elems += note_box(
        '<b>Example:</b> "Your email is delayed due to a routing configuration update. '
        'It will be fully restored by 3:00 PM today. In the meantime, you can access '
        'email via the web browser at mail.google.com."',
        styles, bg=GREEN_SOFT
    )
    return elems


def section_13(styles):
    elems = []
    elems += section_banner("13. Interview Performance Tips", styles, required=False)

    tips = [
        ("Say 'I don't know' when you don't know",
         "Interviewers respect honesty and can tell when you're guessing without flagging it. "
         "It builds trust. Follow with 'but here's how I'd find out' when possible."),
        ("Educated guesses are fine — flag them as guesses",
         "There's a difference between 'I'm not certain, but I believe SCIM uses REST/JSON' "
         "and stating it as fact. Flag uncertainty and it becomes a strength."),
        ("Pause before answering — form your first point, then speak",
         "Silence is not weakness. Two seconds of thinking produces a structured answer. "
         "Rambling while thinking produces a weak one."),
        ("Stop when your answer is done — don't fill silence",
         "The urge to keep talking after a complete answer is the enemy. "
         "A complete, clean answer followed by silence reads as confidence."),
        ("After the interview: log every question asked",
         "Write them down within 30 minutes. Review the gaps. Study them before any follow-up round."),
    ]

    for title, body in tips:
        elems.append(Paragraph(f"<b>{title}</b>", styles["subsection_header"]))
        elems.append(Paragraph(body, styles["body"]))
        elems.append(Spacer(1, 4))

    elems += note_box(
        "<b>Mindset:</b> This interview is a conversation between two professionals, not a test. "
        "You are evaluating them as much as they are evaluating you. "
        "Bring curiosity and calm — you've done the prep work.",
        styles, bg=LIGHT_BLUE
    )
    return elems


def section_14(styles):
    """Quick Reference Card."""
    elems = []
    elems += section_banner("14. Quick Reference Card", styles, required=False)

    elems.append(Paragraph(
        "Keep this card open during final review. These are the core mental models.",
        styles["body"]
    ))
    elems.append(Spacer(1, 8))

    cards = [
        ("ONBOARDING FLOW", [
            "HRIS trigger (BambooHR/Workday)",
            "→ Webhook/API to Okta (or automation layer)",
            "→ Okta account created (SCIM or API)",
            "→ Group rules evaluate → RBAC auto-assigns",
            "→ Apps provisioned via group membership",
            "→ Manual checklist generated (Jira)",
            "→ MDM enrolls laptop → Staged and delivered",
        ]),
        ("OFFBOARDING FLOW", [
            "HRIS deactivation event fires",
            "→ Okta account deactivated (target: < 15 min)",
            "→ Group memberships removed",
            "→ All app access revoked (SCIM deprovisioning)",
            "→ MDM sends remote lock/wipe",
            "→ Asset marked 'pending return'",
            "→ Account suspended → archived per retention policy",
        ]),
        ("SAML vs SCIM", [
            "SAML = Authentication (who you are)",
            "  XML assertion | Okta = IdP | App = SP",
            "  Breaks: expired cert, metadata mismatch, clock skew",
            "  Fix: re-pull metadata, re-upload both sides",
            "SCIM = Provisioning (create/update/delete users)",
            "  REST/JSON payload | Okta pushes to app",
            "  Breaks: expired token, attribute mapping drift",
            "  Fix: regenerate token, verify field mappings",
        ]),
        ("RBAC RULE LOGIC", [
            "IF [attribute] AND [attribute] → assign group",
            "IF [attribute] AND NOT [attribute] → assign group",
            "Goal: ZERO manual group membership",
            "Rule of thumb: if you can write a rule for it, you should",
            "Manual assignment = drift = tickets = tech debt",
        ]),
        ("INTEGRATION BROKEN", [
            "1. Check Okta System Log — when did it stop?",
            "2. Check SAML assertion or SCIM payload",
            "3. Check both sides (Okta logs + app logs)",
            "4. Refresh expired cert or token",
            "5. Open vendor/Okta support ticket in parallel",
        ]),
        ("EXECUTIVE COMMUNICATION", [
            "Format: Impact + Action + Timeline",
            "Skip: technical cause, jargon, uncertainty",
            'Template: "[System] is [issue]. I am [action].',
            'Resolution by [time]. Workaround: [simple step]."',
        ]),
        ("MDM QUICK REF", [
            "macOS: Kandji (blueprints) | Jamf Pro (policies/scripts)",
            "Windows: Intune (compliance + config policies)",
            "Zero-touch Mac: ABM + MDM → auto-enroll on first boot",
            "Zero-touch Windows: Autopilot → AADJ + Intune auto-enroll",
            "Offboard: Remote lock → Wipe → Unenroll → Reassign",
        ]),
        ("SECURITY BASELINE", [
            "MFA: enforce for ALL users, ALL apps",
            "Least privilege: access requires a justified role",
            "Fast offboarding: < 15 min from HR action to deactivation",
            "Device trust: only managed devices access sensitive apps",
            "Audit logs: retain 12 months, review quarterly",
            "Zero trust: verify every user, every device, every access",
        ]),
    ]

    col_w = (PAGE_W - 2 * MARGIN - 0.1 * inch) / 2

    for i in range(0, len(cards), 2):
        row_cards = cards[i:i + 2]
        row_data = []
        for title, items in row_cards:
            cell_content = [Paragraph(title, styles["card_header"])]
            for item in items:
                cell_content.append(Paragraph(f"•  {item}", styles["card_body"]))
            row_data.append(cell_content)

        while len(row_data) < 2:
            row_data.append([Paragraph("", styles["card_body"])])

        t = Table([row_data], colWidths=[col_w, col_w])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (0, 0), LIGHT_BLUE),
            ("BACKGROUND",   (1, 0), (1, 0), GRAY_LIGHT),
            ("TOPPADDING",   (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
            ("LEFTPADDING",  (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
            ("BOX",          (0, 0), (0, 0), 0.5, MID_BLUE),
            ("BOX",          (1, 0), (1, 0), 0.5, colors.HexColor("#D1D5DB")),
            ("ROUNDEDCORNERS", [3]),
        ]))
        elems.append(t)
        elems.append(Spacer(1, 6))

    return elems


def section_15(styles):
    """Mock Q&A."""
    elems = []
    elems += section_banner("15. Mock Q&A — Practice Questions with Model Answers", styles, required=False)

    elems.append(Paragraph(
        "Read each question, cover the answer, and respond aloud before checking. "
        "<b>Drill these until the answers feel like your own words, not memorized text.</b>",
        styles["body"]
    ))
    elems.append(Spacer(1, 8))

    # ── Okta ─────────────────────────────────────────────────────────────────
    data = [[Paragraph("OKTA", styles["section_header"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [3]),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 6))

    okta_qa = [
        ("Walk me through how you would onboard a new employee in Okta end to end.",
         "The process starts with the HRIS. When a new employee record is created in BambooHR or Workday, "
         "a webhook fires to our automation layer — either Okta Workflows or a middleware tool like Workato. "
         "That trigger creates the Okta account, and our group rules evaluate the user's department, location, "
         "and role attributes to auto-assign them to the right groups. Group membership drives app provisioning "
         "via SCIM. Any apps outside RBAC go through a manager request flow. In parallel, a Jira checklist "
         "generates for manual steps like badge access, and MDM starts staging the laptop. By day one, "
         "the user boots their machine, completes Okta Verify enrollment, and everything is ready."),
        ("How would you structure groups in Okta to manage role-based access control?",
         "I structure groups around roles, not individuals. Each group maps to a specific job function or "
         "access tier — for example, 'eng-team', 'sales-team', 'it-admin'. Groups are assigned apps, "
         "not users directly. Group membership is driven entirely by Okta Group Rules that evaluate profile "
         "attributes like department, title, and employeeType. That way, adding a new employee to the right "
         "department automatically grants the right access. No manual group assignment needed."),
        ("An app integration broke overnight. Walk me through how you would troubleshoot it.",
         "First, I go to Okta's System Log and filter for the affected app around the time it stopped working. "
         "I'm looking for authentication failures, provisioning errors, or any configuration changes. "
         "Next, I check whether it's SAML or SCIM — for SAML I'll capture an assertion and verify the cert "
         "and attribute mapping; for SCIM I'll check the provisioning logs for payload errors or expired tokens. "
         "I always check both sides: Okta's logs show what it sent, the app's logs show what it received. "
         "If I find an expired cert or token, I rotate it and test. If I'm not resolved in 20 minutes, "
         "I open a vendor support ticket in parallel while I keep investigating."),
        ("What is the difference between SAML and SCIM and when would you use each?",
         "SAML handles authentication — it's the protocol that lets a user log into an app through Okta SSO. "
         "Okta sends a signed XML assertion to the app, the app validates it, and the user gets in. "
         "SCIM handles provisioning — it's how Okta creates, updates, and deactivates user accounts in "
         "downstream apps automatically. You use SAML so users don't need separate passwords for each app, "
         "and SCIM so you don't have to manually manage user accounts in every system."),
        ("How do you avoid manual group membership drift in Okta?",
         "By writing group rules for everything I can. Okta Group Rules evaluate user profile attributes "
         "and assign group membership automatically, so there's no manual step to drift. If a use case "
         "doesn't fit a rule, I create a named exception group with documented membership and a Jira ticket "
         "to revisit it. I also run periodic access reviews to catch any manual assignments that crept in "
         "and convert them to rule-based access."),
        ("Walk me through how you would offboard a terminated employee.",
         "Offboarding is onboarding in reverse. The moment HR marks the employee terminated in the HRIS, "
         "a webhook fires to Okta and deactivates the account — my target is under 15 minutes from HR action. "
         "Deactivation removes all group memberships, which revokes group-based app access. "
         "SCIM then sends deprovisioning calls to each connected app. Any apps not on SCIM get manually "
         "revoked via a Jira checklist. Simultaneously, MDM sends a remote lock to the laptop and marks "
         "the device as pending return in the asset system."),
        ("What is an authentication policy and why does it matter?",
         "An authentication policy in Okta defines what factors are required to access a specific app or "
         "group of apps. For example, I might require phishing-resistant MFA for the admin console but "
         "allow push notification for lower-risk apps. Policies also enforce device trust — requiring that "
         "only MDM-managed devices can access sensitive systems. They matter because not all apps carry "
         "the same risk, and a one-size policy either over-restricts or under-secures. Authentication "
         "policies let you calibrate access to actual risk."),
    ]
    for q, a in okta_qa:
        elems += qa_pair(q, a, styles)

    # ── Google Workspace ──────────────────────────────────────────────────────
    data = [[Paragraph("GOOGLE WORKSPACE", styles["section_header"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [3]),
    ]))
    elems.append(Spacer(1, 8))
    elems.append(t)
    elems.append(Spacer(1, 6))

    gws_qa = [
        ("How have you used Google Workspace admin in a previous role?",
         "I've managed the full user lifecycle — creating, suspending, and deleting accounts, managing OU "
         "structure to apply different security policies by department, and controlling third-party app "
         "access through API controls. I've set up Google Groups for role-based access to Shared Drives "
         "and enforced 2-Step Verification org-wide. I also used the audit logs regularly to investigate "
         "suspicious login activity and file sharing events."),
        ("How would you manage app access for different departments in Google Workspace?",
         "I use a combination of OU structure and Google Groups. For broad policy differences — like "
         "contractors not getting access to certain Google services — I put them in a separate OU with "
         "those services disabled. For finer-grained app access, like Shared Drive membership or "
         "distribution lists, I use Google Groups. For third-party OAuth apps, I control which apps "
         "are trusted and what scopes they can access through the API Controls section."),
        ("How do you enforce security policies across a Google Workspace org?",
         "Through a combination of OU-level settings and org-wide policies. I enforce 2-Step Verification "
         "as mandatory for all users — no exemptions except specific service accounts. I set session "
         "length limits so that access doesn't persist indefinitely on unmanaged devices. For file sharing, "
         "I restrict external sharing to specific approved domains unless users request an exception. "
         "I also review the Alert Center regularly for suspicious login patterns."),
        ("How does Google Workspace integrate with Okta?",
         "Okta integrates with Google Workspace via SAML for SSO and SCIM for provisioning. "
         "Okta becomes the identity provider — users authenticate through Okta, and Google accepts "
         "Okta's SAML assertion to grant access. On the provisioning side, Okta's SCIM integration "
         "creates and deactivates Google accounts based on Okta user status, and can set the OU "
         "assignment based on Okta group attributes. This means Google user management is largely "
         "automated through Okta."),
    ]
    for q, a in gws_qa:
        elems += qa_pair(q, a, styles)

    # ── MDM ───────────────────────────────────────────────────────────────────
    data = [[Paragraph("MDM — macOS AND WINDOWS", styles["section_header"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [3]),
    ]))
    elems.append(Spacer(1, 8))
    elems.append(t)
    elems.append(Spacer(1, 6))

    mdm_qa = [
        ("What MDM platforms have you worked with and what did you manage in them?",
         "On the Mac side I've worked with Kandji and Jamf. In Kandji I use blueprints to manage "
         "configuration profiles, app deployments, and OS enforcement policies. In Jamf I've built "
         "policies and used scripts for more complex workflows. On Windows I've used Intune for device "
         "enrollment, compliance policies, and app deployment. Across both I manage the full device "
         "lifecycle — enrollment at staging through wipe at offboarding."),
        ("Walk me through how you would enroll a new Mac into your MDM.",
         "For zero-touch: the device is purchased through our Apple Authorized Reseller who registers "
         "the serial to our Apple Business Manager account. The ABM is connected to Kandji or Jamf, "
         "so when the device powers on for the first time it receives the MDM enrollment profile "
         "automatically. The user goes through setup, and by the time they're at the desktop our "
         "configuration profiles and required apps are already installing silently. For manual enrollment, "
         "I download the MDM enrollment profile and install it, or use Apple Configurator 2 for staging."),
        ("How do you handle a device when an employee is terminated?",
         "MDM is part of the offboarding automation. When the offboarding workflow fires, I send a remote "
         "lock command through MDM immediately to prevent the employee from accessing the device. "
         "Once the device is physically returned, I perform a remote wipe to factory reset it. "
         "Then I unenroll it from MDM, remove the user assignment in the asset management system, "
         "and mark it as available for reassignment or decommission."),
        ("What is zero-touch enrollment and have you worked with it?",
         "Zero-touch enrollment means a device arrives at the employee's door or desk and enrolls in MDM "
         "automatically on first boot — no IT hands-on required. For Macs, this works through Apple "
         "Business Manager: the reseller registers the device to ABM, ABM is connected to the MDM, "
         "and on first power-on the enrollment profile installs automatically. For Windows, it's "
         "Autopilot: the hardware hash is registered to Intune, and the device Azure AD joins and "
         "enrolls into Intune during initial setup. Yes, I've set this up and it's a major operational "
         "win for scaling without adding IT headcount."),
    ]
    for q, a in mdm_qa:
        elems += qa_pair(q, a, styles)

    # ── Security ──────────────────────────────────────────────────────────────
    data = [[Paragraph("SECURITY", styles["section_header"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [3]),
    ]))
    elems.append(Spacer(1, 8))
    elems.append(t)
    elems.append(Spacer(1, 6))

    sec_qa = [
        ("How do you think about least privilege access in your day to day work?",
         "Least privilege means users start with nothing and earn access through their role, "
         "not through asking. In practice, I implement it through RBAC group rules in Okta — "
         "your job function determines your access automatically. For anything above standard access, "
         "I require a manager approval workflow and time-bound grants where possible. "
         "I also run quarterly access reviews to catch access that was granted but is no longer justified."),
        ("What steps do you take when an employee is terminated from a security standpoint?",
         "Speed is the priority. I coordinate with HR so that IT is ready to act the moment termination "
         "is confirmed — for involuntary exits we're standing by. The HRIS event fires, Okta deactivates "
         "the account, SCIM deprovisions app access across all connected systems. Any non-SCIM apps get "
         "manually revoked via checklist. MDM locks the device. I document the time from termination to "
         "full deactivation for our compliance records. Any shared credentials the employee had access "
         "to get rotated immediately."),
        ("How do you enforce MFA across your org?",
         "In Okta, I use authentication policies to require MFA for all apps — no exceptions. "
         "I prefer Okta Verify with push or biometric over SMS because of SIM swap risk. "
         "For admin access I require phishing-resistant factors like hardware keys or "
         "passkeys where supported. In Google Workspace I enforce 2-Step Verification at "
         "the OU level with no exemption. New users are prompted to enroll MFA on their first login, "
         "and accounts can't fully activate until enrollment is complete."),
    ]
    for q, a in sec_qa:
        elems += qa_pair(q, a, styles)

    # ── Help Desk ─────────────────────────────────────────────────────────────
    data = [[Paragraph("HELP DESK AND COMMUNICATION", styles["section_header"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [3]),
    ]))
    elems.append(Spacer(1, 8))
    elems.append(t)
    elems.append(Spacer(1, 6))

    hd_qa = [
        ("How do you prioritize multiple urgent tickets coming in at the same time?",
         "I do a fast first pass on all incoming tickets before touching any of them — I'm looking for "
         "anything that's business-down or blocking an executive. Then I apply the impact vs urgency "
         "matrix: high impact plus high urgency gets immediate attention, everything else queues in order. "
         "Critically, I look for patterns — if multiple people are reporting the same issue, I treat it as "
         "one systemic incident rather than individual tickets. I acknowledge everything within 15 minutes "
         "even if I can't resolve it yet, because a silent ticket creates more anxiety than a slow one."),
        ("How would you explain a technical issue to a non-technical executive?",
         "I use the impact-action-timeline format and skip the technical cause entirely. "
         "Something like: 'Your calendar invites are not sending. I'm resolving a configuration issue "
         "and expect it fixed by 2 PM. In the meantime, you can send invites directly from your phone.' "
         "The executive wants to know if they need to reschedule their day — not why DNS propagation "
         "is inconsistent. I keep it under three sentences."),
        ("Tell me about a time an integration or system broke. How did you identify and fix it?",
         "We had a SAML integration to our expense management platform stop working overnight — "
         "users were getting authentication errors. I pulled Okta's system log first and saw failed "
         "SAML assertions timestamped around 11 PM, which matched a scheduled cert rotation window. "
         "I confirmed the app's signing cert had been auto-renewed on Okta's side but the SP hadn't "
         "received updated metadata. I re-exported the metadata from Okta, uploaded it to the expense "
         "platform's SSO settings, and tested. Login was restored in about 20 minutes. "
         "I documented the fix and set a calendar reminder 30 days before the next cert expiry."),
    ]
    for q, a in hd_qa:
        elems += qa_pair(q, a, styles)

    # ── Asset Management ──────────────────────────────────────────────────────
    data = [[Paragraph("ASSET MANAGEMENT", styles["section_header"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [3]),
    ]))
    elems.append(Spacer(1, 8))
    elems.append(t)
    elems.append(Spacer(1, 6))

    asset_qa = [
        ("Walk me through your hardware lifecycle process from procurement to offboarding.",
         "It starts with procurement — I submit a PO through our vendor, ensuring the reseller "
         "registers devices to Apple Business Manager for zero-touch. When devices arrive I verify "
         "serials, tag them, and log them in the asset system. Staging means enrolling in MDM, "
         "applying profiles and apps, and naming the device. I assign to the user, deliver, and "
         "confirm MDM enrollment and compliance. At refresh time — typically every 3-4 years — "
         "I evaluate battery and performance metrics from MDM to prioritize replacements. "
         "At offboarding, the device is locked via MDM, collected, wiped, unenrolled, and "
         "marked available for reassignment."),
        ("How do you track and manage IT assets across a growing organization?",
         "MDM is the live source of truth for device state — OS version, last check-in, compliance. "
         "Asset management (whether that's Snipe-IT, a Jamf record, or a dedicated tool) tracks "
         "ownership history, purchase dates, and location. The serial number is the link between both. "
         "I run quarterly reconciliation: compare MDM inventory to the asset system and investigate "
         "any gaps. As the org grows, the key is automation — MDM enrollment automatically creates "
         "the asset record so nothing gets missed. I also maintain a loaner pool with a "
         "check-out/check-in log for temporary devices."),
    ]
    for q, a in asset_qa:
        elems += qa_pair(q, a, styles)

    # ── Behavioral ────────────────────────────────────────────────────────────
    data = [[Paragraph("BEHAVIORAL / SITUATIONAL", styles["section_header"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [3]),
    ]))
    elems.append(Spacer(1, 8))
    elems.append(t)
    elems.append(Spacer(1, 6))

    beh_qa = [
        ("Tell me about a time you had to learn something technical quickly. How did you approach it?",
         "When I was first handed ownership of our Okta environment I had hands-on experience but "
         "hadn't managed it solo before. I broke the learning down: I spent the first week on "
         "the current config — documented what existed, understood why each group rule and policy "
         "was there. I ran through Okta's admin certification material in parallel. I identified "
         "the three most likely failure points and made sure I knew how to diagnose and resolve each one. "
         "Within two weeks I was making configuration changes confidently. The approach is always: "
         "understand what exists before building anything new."),
        ("Describe a time you improved or automated a manual IT process.",
         "Our onboarding process was almost entirely manual — IT received a Slack message when someone "
         "was hired, then manually created accounts, assigned apps, and generated a checklist by hand. "
         "I mapped out every step, identified which ones were rule-based, and built group rules in Okta "
         "to handle RBAC automatically. I connected BambooHR to Okta Workflows to trigger account "
         "creation from HRIS events. I replaced the manual checklist with a Jira automation that "
         "generated the ticket with subtasks on trigger. Total manual IT time per hire went from "
         "about 45 minutes to under 5 minutes for standard roles."),
        ("How do you stay current with new tools and technologies?",
         "I follow vendor release notes for Okta, Kandji, and Google Workspace — they publish "
         "changelogs and I have them in an RSS reader. For broader trends I follow a handful of "
         "IT ops and identity security communities. When I hear about a new tool I try to get hands "
         "on with it in a sandbox or trial before evaluating whether it solves a real problem. "
         "I also stay connected to peers in the space — sometimes a 10-minute conversation with "
         "someone who's already implemented something saves two weeks of research."),
        ("What does good IT documentation look like to you and why does it matter?",
         "Good documentation is something a new team member can follow without asking anyone a question. "
         "It has a clear purpose statement, numbered steps with expected outcomes at each step, "
         "and a 'what to do if this breaks' section. It lives in a searchable system — Confluence — "
         "not in someone's head or a personal doc. It matters because documentation is a force multiplier: "
         "a well-written runbook means the second person to hit an issue resolves it in 5 minutes "
         "instead of 45. It also means the team can operate safely when any one person is out."),
    ]
    for q, a in beh_qa:
        elems += qa_pair(q, a, styles)

    return elems


def section_16(styles):
    """Questions to ask the interviewer."""
    elems = []
    elems += section_banner("16. Questions to Ask the Interviewer", styles, required=False)

    elems.append(Paragraph(
        "Ask 2–3 of these at the end of the interview. Choose based on what's come up in conversation. "
        "<b>These signal strategic thinking, not just job-seeking.</b>",
        styles["body"]
    ))
    elems.append(Spacer(1, 10))

    questions = [
        (
            "On automation maturity",
            "Where would you say the team sits on the spectrum from mostly manual to fully automated "
            "for onboarding and offboarding? And what's the biggest blocker to moving further along that spectrum?",
            "This shows you're thinking about the gap between current state and ideal state — "
            "and that you're already thinking about how to close it."
        ),
        (
            "On IT and engineering collaboration",
            "How does the IT team collaborate with engineering right now? Are there shared tools, "
            "shared runbooks, or joint ownership of things like identity and access infrastructure?",
            "This reveals whether IT is a service desk or a technical peer to engineering — "
            "and whether you'd have room to do real infrastructure work."
        ),
        (
            "On 90-day success",
            "What would success look like at 90 days for someone in this role? "
            "What's the difference between someone who's doing the job and someone who's "
            "already making the team better?",
            "This frames you as someone who thinks in outcomes, not tasks. "
            "It also gives you a roadmap if you get the offer."
        ),
        (
            "On AI and tooling direction",
            "Is the team thinking about how AI tooling fits into IT operations — "
            "things like AI-assisted ticket routing, automated diagnostics, or workflow generation? "
            "Where does that conversation stand right now?",
            "This signals forward-thinking awareness without overclaiming. "
            "It also shows genuine curiosity about where the company is heading."
        ),
        (
            "On biggest infrastructure challenges",
            "What's the biggest infrastructure or identity challenge the team is working through "
            "right now that the person in this role would be expected to contribute to?",
            "This is the most valuable question you can ask. The answer tells you exactly "
            "what the real job is — not just what's in the job description."
        ),
    ]

    for i, (theme, question, rationale) in enumerate(questions, 1):
        # Question box
        data = [[Paragraph(f"Question {i} — {theme}", styles["subsection_header"])]]
        t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), LIGHT_BLUE),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("ROUNDEDCORNERS", [3]),
        ]))
        elems.append(KeepTogether([
            t,
            Spacer(1, 4),
            Paragraph(f'<i>"{question}"</i>', styles["body"]),
            Spacer(1, 4),
            Paragraph(f"<b>Why this works:</b> {rationale}", styles["interviewer_note"]),
            Spacer(1, 8),
        ]))

    elems += note_box(
        "<b>Final reminder:</b> You don't have to ask all five. Pick the two that align most naturally "
        "with what came up in the conversation. A question that connects back to something they said "
        "earlier is worth more than any question from this list.",
        styles, bg=GREEN_SOFT
    )
    return elems


# ── Build document ────────────────────────────────────────────────────────────
def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=0.85 * inch,
        title="Okta Interview Study Guide",
        author="Prepared for Interview Preparation",
        subject="Okta, Google Workspace, MDM, Security",
    )

    styles = make_styles()
    story = []

    # ── Cover page ────────────────────────────────────────────────────────────
    story += cover_flowables(styles)
    story.append(PageBreak())

    # ── Table of Contents ─────────────────────────────────────────────────────
    story += toc_page(styles)
    story.append(PageBreak())

    # ── Sections ──────────────────────────────────────────────────────────────
    sections = [
        section_1, section_2, section_3, section_4, section_5,
        section_6, section_7, section_8, section_9, section_10,
        section_11, section_12, section_13,
    ]
    for fn in sections:
        story += fn(styles)
        story.append(PageBreak())

    story += section_14(styles)
    story.append(PageBreak())

    story += section_15(styles)
    story.append(PageBreak())

    story += section_16(styles)

    # ── Build with page-number callback ───────────────────────────────────────
    def on_page(canvas_obj, doc_obj):
        if doc_obj.page == 1:
            build_cover(canvas_obj, doc_obj)
        else:
            add_page_number(canvas_obj, doc_obj)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved to {output_path}")


if __name__ == "__main__":
    build_pdf("/home/user/AI-Automation-Workflows/okta_study_guide.pdf")
