---
name: research-dossier
description: Turns a set of research papers (and optionally extracted claims and conflicts) into a documented, visual literature review — a single print-ready HTML report with charts, thematic synthesis, a debates section, an evidence table, a timeline, an annotated bibliography and a reproducible methods section, plus Markdown, pandoc-ready Markdown and BibTeX. Every citation is checked against the paper set, so nothing is invented. Use when a student or researcher asks to write up a literature review, related-work section, annotated bibliography, research summary or state-of-the-art report.
---

# Research Dossier

Write the literature review a supervisor would want to read: an answer first, organised by theme, honest about disagreements, with every citation traceable to a real record.

Last step of the Research Suite: `paper-scout` → `claim-conflict-finder` → `research-dossier`. Schema: `references/schema.md`.

## Non-negotiable rules

1. **Cite only papers in `papers.json`**, always as `[@key]`. The build refuses unknown keys. Never write a citation as plain text like "(Smith, 2020)".
2. Say only what the papers support. If a statement comes from your general knowledge rather than the set, either drop it or label it plainly ("Background, not from the reviewed papers: …").
3. Represent disagreement fairly: if `conflicts.json` shows a contested relationship, the review must say so.

## 1. Gather inputs

From the project folder (default `research/<slug>/`):

- `papers.json` — required. If it does not exist, run `paper-scout` first, or build it from papers the user provides.
- `claims.json` and `conflicts.json` — optional but strongly recommended; they power the debates section and the evidence table. Offer `claim-conflict-finder` if they are missing and the user has time.

Ask the user (once, briefly) for anything that changes the writing: **audience and purpose** (thesis chapter, class assignment, grant background, lab onboarding), **length** (default ~1,200–1,800 words of synthesis), **language**, and **author name** for the byline. Write in the user's language; keep paper titles as published.

## 2. Plan the review

Read the included papers' abstracts (and claims, if present). Then decide:

- **The answer**: 2–4 sentences that answer the research question directly, with citations.
- **3–6 themes**: group papers by what they contribute (method family, population, outcome, mechanism, era), not by paper. A theme with one paper is a sentence, not a section.
- **Debates**: take each `contested` or `context-dependent` topic from `conflicts.json` and explain *why* the papers disagree. Reference the claim pairs as `"C004~C005"` so the report shows them side by side.
- **Open questions**: gaps that follow from the evidence — missing populations, short follow-up, no replication, unresolved conflicts.

## 3. Write `synthesis.json`

Follow the schema exactly:

```json
{
  "schema": "research-suite/synthesis@1",
  "title": "A specific title, not 'Literature review'",
  "question": "The research question",
  "author": "Name from the user, or empty",
  "summary": "The direct answer, with [@key] citations.",
  "takeaways": ["3–5 one-sentence takeaways, each cited."],
  "themes": [ { "name": "…", "summary": "1–3 paragraphs separated by spaces, cited.", "papers": ["key1", "key2"] } ],
  "debates": [ { "topic": "subject | object (the topic id from conflicts.json)", "summary": "…", "pairs": ["C004~C005"] } ],
  "open_questions": ["…"],
  "methods_note": "How papers were found, screened and read; what was not covered.",
  "annotations": { "key1": "1–3 sentences: what the paper did, what it found, why it matters here." }
}
```

Writing style:
- Synthesise across papers ("Three trials found…, whereas…"), do not summarise one paper per paragraph.
- Put the claim first, then the citation: "Adherence was lower under fasting regimens [@a; @b]."
- Report numbers when the papers give them; give sample sizes for key studies.
- Mark preprints in the text when a conclusion rests on one.
- `**bold**` and `*italic*` are supported; nothing else.
- Write an annotation for every paper you cite in the summary or themes.

## 4. Build

Standard-library Python, no network. Run exactly as shipped:

```bash
python3 scripts/dossier.py check --out research/<slug>    # fix every ERROR
python3 scripts/dossier.py build --out research/<slug>
```

Outputs:
- `dossier.html` — the report. Single file, works offline, light/dark, prints cleanly to PDF, has a "Download BibTeX" button.
- `dossier.md` — numbered citations and an APA-style reference list, ready to paste into Word or Google Docs.
- `dossier.pandoc.md` — `[@key]` citations; `pandoc dossier.pandoc.md --citeproc -o review.docx` (or `.pdf`, `.tex`) uses `references.bib` and any citation style the student needs.
- `references.bib` — every cited and included paper.

Open `dossier.html` (or screenshot it if you can) and check: citations render as numbers, every theme has text, charts are not empty.

## 5. Deliver

1. The short answer in chat (2–3 sentences) so the user gets value without opening a file.
2. The files, with one line each on what to use them for.
3. **What to check before submitting**: claims extracted from abstracts only, preprints relied on, any paper the user should read in full before citing.
4. Offer one concrete next step: expand a theme, convert to a specific citation style, or turn the review into slides.

## If the earlier skills were not used

You can still build a dossier from a list of papers the user provides: create `papers.json` by hand (one entry per paper, real metadata only), skip claims and conflicts, and write `synthesis.json`. The debates section will then come only from what you write in `debates`.

## No terminal

Write the review directly as Markdown with numbered citations and an APA-style reference list built from `papers.json`. Say that the HTML report and charts need the script.
