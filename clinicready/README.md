# ClinicReady — Clinical Workflow Simulator (Phase 1)

A personal, single-user training tool for rehearsing complete outpatient
encounters — intake through documentation and follow-up — with objective,
inspectable scoring. Built to the *ClinicReady Build Brief (v2)*.

## How to open it

Double-click **`index.html`**, or open it in any modern browser on a desktop
or tablet. That is the whole app — one file, no install, no server, no
accounts, no internet required. Everything runs on your own device.

## What Phase 1 includes

- **The full encounter loop.** Chart review → identity → chief complaint &
  agenda-setting → HPI → medication reconciliation → allergies → PMH/PSH/FH/SH
  → review of systems → preventive care → vitals → focused exam → orders →
  problem representation → differential → red-flag check → diagnosis →
  management → patient education → disposition → follow-up → return
  precautions → documentation. Nothing is revealed until you take the action
  that would elicit it.
- **Three deeply built cases:**
  1. **New-patient establishment with multimorbidity** — HTN + type 2 diabetes
     with medication nonadherence to uncover and preventive-care gaps to close,
     plus a genuine cardiovascular red flag hiding under a "refill" visit.
  2. **Undifferentiated chest pain requiring escalation** — a "just squeeze me
     in" complaint that is an acute coronary syndrome until proven otherwise;
     the safe path is aspirin + EMS, not a heartburn trial.
  3. **Viral upper-respiratory illness with an antibiotic demand** — stewardship
     and communication, with a documented penicillin allergy that turns the
     wrong prescription into a real medication-safety event.
- **Two modes** — Guided Practice (objectives, a live critical-actions
  checklist, per-panel hints) and Independent Encounter (no help until you
  submit) — plus a **Timed** toggle that makes exceeding the appointment slot
  cost points.
- **A 100-point scoring engine and after-action report** where every point
  gained, lost, or forgone is inspectable, with guideline citations and dates,
  a medication-safety analysis, an expert walk-through, three lessons, and a
  replay button. Critical safety misses cap the score with a clear,
  non-shaming explanation of the risk.
- **Save / load progress** and a **Case Review** screen where you read a
  case's full clinical content and sources and mark it **Approved**.

## A note on "Draft" cases and clinical sourcing

Every case ships marked **Draft**. Open it in the **Case Library**, read the
full authored content, learning objectives, guideline sources (with issuing
body and date), and the expert walk-through, then mark it **Approved** once you
have verified the clinical content. Guidelines change — please confirm each
source against its current published version before relying on a case. The
guideline names and dates in each case are starting points for your review,
not a substitute for it.

## Saving your progress

Your approvals and encounter history are kept automatically in **this browser**
only. That is convenient but not a file — it will not follow you to another
device and will be lost if you clear your browser data. Use **Settings → Save
my progress** to download a portable backup file, and **Load progress** to
restore it here or on another device.

## Safety

For professional education and simulation only. Not a substitute for clinical
judgment, institutional policy, or current medical references. All patients are
synthetic — do not enter any real patient information anywhere.

## What comes next (not yet built)

Phase 2: an in-app case-authoring template, a larger case library, protocol
drills, a performance dashboard with a Clinic-Readiness score, and structured
documentation practice. Phase 3: follow-up mode, a full clinic day with
interruptions, weakness review with spaced repetition, a red-flag challenge,
light gamification, and a protocol manager.
