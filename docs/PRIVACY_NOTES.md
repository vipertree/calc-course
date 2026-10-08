# Privacy notes for Adder (COPPA, FERPA, GDPR)

Not legal advice, and nothing here claims the site is compliant with anything. It lists what the site
collects, what was built to keep that small, and the open questions only you (or a lawyer, or a school's
privacy office) can answer. The public pages are `/privacy/` and `/terms/` (templates
`web/templates/accounts/privacy.html` and `terms.html`); both show a "Draft" notice until
`LEGAL_PAGES_REVIEWED=true` is set in `.env`. Review notes for you are `{# ADDER: ... #}` comments in them.

## What the site stores

| Data | Who | Why |
|---|---|---|
| username, display name, password hash, join date, last login | everyone | the account |
| email (+ confirmed flag) | self sign-ups and teachers; class students only if they add one | password reset, confirmation links |
| school name | teachers who give it | checking teacher requests |
| finished lesson steps, checked answers (what was typed), drafts of answer boxes, quiz/test attempts with answers, FRQ self-scores | students | progress, the teacher dashboard, resuming work |
| packet IDs (printed on the PDF with the person's display name) | anyone who prints | tracing leaked copies |
| `theme` / `design` cookies | anyone who picks one | remembering the look |
| nginx access logs (IP, URL, time) | everyone | operations; retention is the server's logrotate setting |

No analytics, no ads, no third-party trackers, no profiling. Nothing is sold or shared.

## What was built to keep it small

- **Class-code students give no email.** Teachers reset their passwords (Manage students on the dashboard;
  the temporary password is shown to the teacher once and is not stored in a cookie).
- Display-name help text suggests "first name and last initial".
- Self sign-up requires ticking "I am 13 or older"; younger students come in only through a class.
- **Data export**: Account settings, "Download my data" (JSON of everything above for that account).
- **Self-service deletion**: Account settings, password + checkbox. Cascades to all of the user's work.
  A teacher deleting their account deletes their classes; students keep their accounts and work.
- Students can leave a class; teachers can remove a student from a class.
- `manage.py purge_unverified` deletes self sign-ups that never confirmed their email and did nothing, after
  14 days (cron line in DEPLOYMENT.md). Nothing deletes long-inactive accounts yet (your call).
- Backups roll off after `BACKUP_DAYS` (14); the privacy page states that number.
- Only essential cookies, so no cookie banner (the theme/design cookies are set only when the person picks one,
  which counts as a request for that feature).

## COPPA (US, children under 13)

- AP Calculus students are almost all 15-18, but some districts accelerate, and the site can't know ages.
- The design relies on two things: self sign-up is 13+ by checkbox (an age screen, not verification), and
  under-13 students only arrive through a teacher's class. The FTC has said schools may consent on parents'
  behalf **only** for educational use and only when the operator uses the data for nothing else. The site uses
  student data only for the course, which fits that; but whether a given school has actually given that
  consent is between you and the school. Many districts require a signed data privacy agreement first (see below).
- The 2025 amendments to the COPPA Rule (effective June 2025, most compliance due April 2026; check the current text) tightened
  written data-retention policies and security programs. The retention bullets on the privacy page are a start;
  a written security/retention policy is not done.
- Open: do you want an explicit "teachers confirm they have school authorization" checkbox on the teacher
  request form? Cheap to add.

## FERPA (US schools)

- FERPA binds schools, not you directly. A school can share student records with you under the "school
  official" exception if you are under its direct control for that data, use it only for the school's
  purpose, and don't re-disclose it. In practice this means **the district's contract or data privacy
  agreement** (many states use the Student Data Privacy Consortium's NDPA template).
- Things the site already does that such agreements ask about: no sale or advertising use, export and
  deletion on request, access limited to the student, their own teacher and the operator, TLS everywhere,
  hashed passwords, backups with a fixed retention.
- Things they often ask that are **not** done: a named breach-notification process and timeline, encryption of
  backups at rest, an off-server backup copy (DEPLOYMENT.md recommends one), audit logs of admin access,
  a list of subprocessors (hosting: Hetzner; email: TBD; fonts/scripts: Google Fonts, jsDelivr, Desmos).
- State laws (California SOPIPA, New York Ed Law 2-d, Illinois SOPPA, and others) add their own terms,
  often via the same agreements. Worth knowing which states your first teachers are in.

## GDPR (if anyone in the EU/UK uses it)

- The server is at Hetzner (check which location; EU locations keep the data in the EU).
- Lawful basis would be contract (running the account) for adults; for under-16s in many EU countries, consent
  needs a parent. The 13+ self sign-up rule does **not** satisfy that everywhere in the EU. If EU users matter,
  this needs a decision (raise the self sign-up age for the EU, or keep the site US-focused and say so).
- Pages load Google Fonts, jsDelivr and Desmos directly from the visitor's browser, which sends them the
  visitor's IP. A Munich court awarded a visitor damages over a site's use of Google Fonts in 2022. **Self-hosting the fonts, KaTeX and
  MathLive** would remove two of the three; Desmos can't be self-hosted. Recommended either way: it also
  tightens the Content-Security-Policy.
- Rights covered: access/portability (export), erasure (delete), rectification (edit name/email). Objection
  and restriction would be by email to CONTACT_EMAIL.

## Decisions for Adder

1. Contact address for the privacy page (`CONTACT_EMAIL`). It is empty now on purpose.
2. Email provider (it becomes a subprocessor; name it on the privacy page).
3. Who reviews the legal drafts, and whether to target schools' data privacy agreements before launch.
4. Self-host fonts/KaTeX/MathLive (privacy and CSP win) or keep the CDNs.
5. Delete long-inactive accounts? After how long?
6. EU users in scope or not.
