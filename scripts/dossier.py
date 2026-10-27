#!/usr/bin/env python3
"""research-dossier: build a documented, visual literature review from the Research Suite files.

Standard library only. No network access.

Reads (from the project folder):
  papers.json      required — from paper-scout or written by hand
  synthesis.json   required — written by the agent (see references/schema.md)
  claims.json      optional — from claim-conflict-finder
  conflicts.json   optional — from claim-conflict-finder

Writes:
  dossier.html         single self-contained, print-ready report
  dossier.md           Markdown with numbered citations
  dossier.pandoc.md    Markdown with [@key] citations for pandoc + references.bib
  references.bib       BibTeX for every cited or included paper

Subcommands: check, build
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "1.0.0"
CITE_RE = re.compile(r"\[(@[\w\-:.]+(?:\s*;\s*@[\w\-:.]+)*)\]")


def log(m: str) -> None:
    print(m, file=sys.stderr)


def load(p: Path, required=True):
    if not p.exists():
        if required:
            sys.exit(f"missing {p}")
        return None
    return json.loads(p.read_text("utf-8"))


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""), quote=True)


# ----------------------------------------------------------------------------- citations

def keys_in(text: str) -> list[str]:
    out = []
    for m in CITE_RE.finditer(text or ""):
        out += [k.strip()[1:] for k in m.group(1).split(";")]
    return out


def all_texts(syn: dict) -> list[str]:
    t = [syn.get("summary", "")] + list(syn.get("takeaways", []))
    for th in syn.get("themes", []):
        t.append(th.get("summary", ""))
    for d in syn.get("debates", []):
        t.append(d.get("summary", ""))
    t += list(syn.get("open_questions", []))
    t.append(syn.get("methods_note", ""))
    return t


def cmd_check(a) -> int:
    root = Path(a.out)
    papers = {p["key"]: p for p in load(root / "papers.json")["papers"]}
    syn = load(root / "synthesis.json")
    errors, warns = [], []
    cited = []
    for t in all_texts(syn):
        cited += keys_in(t)
    for th in syn.get("themes", []):
        cited += th.get("papers", [])
    unknown = sorted({k for k in cited if k not in papers})
    for k in unknown:
        errors.append(f"citation [@{k}] is not in papers.json — never cite a paper that is not in the set")
    for k in syn.get("annotations", {}):
        if k not in papers:
            errors.append(f"annotation for unknown paper '{k}'")
    excl = sorted({k for k in cited if k in papers and papers[k].get("status") == "excluded"})
    for k in excl:
        warns.append(f"[@{k}] is marked excluded in papers.json but is cited")
    inc = [k for k, p in papers.items() if p.get("status") == "included"]
    uncited = [k for k in inc if k not in set(cited)]
    if uncited:
        warns.append(f"{len(uncited)} included papers are never cited (they will appear under Further reading): "
                     + ", ".join(uncited[:10]) + (" …" if len(uncited) > 10 else ""))
    if not syn.get("summary"):
        errors.append("synthesis.summary is empty")
    if not syn.get("themes"):
        warns.append("no themes — the review will have no body sections")
    for t in all_texts(syn):
        for m in re.finditer(r"\(([A-Z][A-Za-z\-]+(?: et al\.)?,? (?:19|20)\d\d)\)", t or ""):
            warns.append(f"hand-written citation '{m.group(1)}' — use [@key] so it is checked and numbered")
    for w in warns:
        print("warn ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(set(cited))} distinct papers cited, {len(errors)} errors, {len(warns)} warnings")
    return 1 if errors else 0


class Numberer:
    def __init__(self, papers: dict):
        self.papers = papers
        self.order: list[str] = []

    def n(self, k: str) -> int:
        if k not in self.order:
            self.order.append(k)
        return self.order.index(k) + 1

    def html(self, text: str) -> str:
        """Escape text, keep **bold** and *italic*, turn [@a; @b] into numbered links."""
        out, last = [], 0
        for m in CITE_RE.finditer(text or ""):
            out.append(inline_md(esc(text[last:m.start()])))
            ks = [k.strip()[1:] for k in m.group(1).split(";")]
            links = []
            for k in ks:
                p = self.papers.get(k)
                if not p:
                    links.append(f'<span class="bad">?{esc(k)}</span>')
                    continue
                links.append(f'<a class="ref" href="#ref-{esc(k)}" data-tip="{esc(short_ref(p))}">{self.n(k)}</a>')
            out.append('<sup class="cite">[' + ", ".join(links) + "]</sup>")
            last = m.end()
        out.append(inline_md(esc((text or "")[last:])))
        return "".join(out)

    def md(self, text: str) -> str:
        def rep(m):
            ks = [k.strip()[1:] for k in m.group(1).split(";")]
            return "[" + ", ".join(str(self.n(k)) for k in ks if k in self.papers) + "]"
        return CITE_RE.sub(rep, text or "")


def inline_md(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def last_name(a: str) -> str:
    a = a.strip()
    if "," in a:
        return a.split(",")[0].strip()
    parts = a.split()
    return parts[-1] if parts else "Anon"


def initials(a: str) -> str:
    a = a.strip()
    first = a.split(",", 1)[1] if "," in a else " ".join(a.split()[:-1])
    return " ".join(w[0] + "." for w in re.split(r"[\s\-]+", first) if w)


def short_ref(p: dict) -> str:
    au = p.get("authors") or ["Anon"]
    who = last_name(au[0]) + (" et al." if len(au) > 2 else (f" & {last_name(au[1])}" if len(au) == 2 else ""))
    return f"{who} ({p.get('year') or 'n.d.'}). {p.get('title', '')}"


def author_year(p: dict) -> str:
    """"Naidu et al. (2021)" — the "Author (Year)" part of short_ref."""
    return short_ref(p).split(f" ({p.get('year') or 'n.d.'})")[0] + f" ({p.get('year') or 'n.d.'})"


def apa(p: dict) -> tuple[str, str]:
    """(html, markdown) reference in an APA-like style."""
    au = [a for a in (p.get("authors") or []) if a]
    names = [f"{last_name(a)}, {initials(a)}".strip().rstrip(",") for a in au]
    if len(names) > 7:
        names = names[:6] + ["…", names[-1]]
    if len(names) > 1:
        who = ", ".join(names[:-1]) + ", & " + names[-1]
    else:
        who = names[0] if names else "Anonymous"
    yr = p.get("year") or "n.d."
    title = (p.get("title") or "").rstrip(".")
    venue = p.get("venue") or ""
    link = f"https://doi.org/{p['doi']}" if p.get("doi") else (p.get("url") or "")
    pre = " [Preprint — not peer-reviewed]" if p.get("is_preprint") else ""
    h = f"{esc(who)} ({esc(yr)}). {esc(title)}.{' <em>' + esc(venue) + '</em>.' if venue else ''}{esc(pre)}"
    if link:
        h += f' <a href="{esc(link)}" target="_blank" rel="noopener">{esc(link)}</a>'
    m = f"{who} ({yr}). {title}.{' *' + venue + '*.' if venue else ''}{pre}{' ' + link if link else ''}"
    return h, m


# ----------------------------------------------------------------------------- charts (inline SVG)

def chart_years(papers: list[dict]) -> str:
    yrs = Counter()
    pre = Counter()
    for p in papers:
        if p.get("year"):
            yrs[p["year"]] += 1
            if p.get("is_preprint"):
                pre[p["year"]] += 1
    if not yrs:
        return ""
    y0, y1 = min(yrs), max(yrs)
    span = list(range(y0, y1 + 1))
    W, H, pl, pb, pt = 640, 200, 34, 26, 12
    bw = (W - pl - 10) / len(span)
    mx = max(yrs.values())
    step = max(1, math.ceil(mx / 4))
    s = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Papers per year">']
    for v in range(0, mx + 1, step):
        y = H - pb - (H - pb - pt) * v / mx
        s.append(f'<line x1="{pl}" x2="{W - 6}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/><text x="{pl - 6}" y="{y + 4:.1f}" class="tick" text-anchor="end">{v}</text>')
    lab_every = max(1, math.ceil(len(span) / 12))
    for i, yv in enumerate(span):
        n, np_ = yrs.get(yv, 0), pre.get(yv, 0)
        x = pl + i * bw + bw * 0.15
        w = bw * 0.7
        h1 = (H - pb - pt) * (n - np_) / mx
        h2 = (H - pb - pt) * np_ / mx
        y = H - pb - h1
        if n:
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h1:.1f}" class="bar"><title>{yv}: {n} papers</title></rect>')
            if np_:
                s.append(f'<rect x="{x:.1f}" y="{y - h2:.1f}" width="{w:.1f}" height="{h2:.1f}" class="bar pre"><title>{yv}: {np_} preprints</title></rect>')
        if i % lab_every == 0:
            s.append(f'<text x="{x + w / 2:.1f}" y="{H - 8}" class="tick" text-anchor="middle">{yv}</text>')
    s.append("</svg>")
    return "".join(s)


def chart_bars(items: list[tuple[str, int]], label: str) -> str:
    if not items:
        return ""
    W, row = 640, 26
    H = row * len(items) + 8
    mx = max(v for _, v in items) or 1
    s = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="{esc(label)}">']
    for i, (name, v) in enumerate(items):
        y = 4 + i * row
        w = (W - 300) * v / mx
        nm = name if len(name) <= 38 else name[:36] + "…"
        s.append(f'<text x="0" y="{y + 16}" class="lab">{esc(nm)}</text>'
                 f'<rect x="250" y="{y + 4}" width="{max(2, w):.1f}" height="16" rx="3" class="bar"><title>{esc(name)}: {v}</title></rect>'
                 f'<text x="{256 + w:.1f}" y="{y + 16}" class="tick">{v}</text>')
    s.append("</svg>")
    return "".join(s)


def balance(dirs: dict) -> str:
    tot = sum(dirs.values()) or 1
    seg = []
    for k, cls in (("positive", "pos"), ("null", "nul"), ("mixed", "mix"), ("negative", "neg")):
        if dirs.get(k):
            seg.append(f'<i class="{cls}" style="width:{100 * dirs[k] / tot:.1f}%" title="{k}: {dirs[k]}"></i>')
    return '<div class="balance">' + "".join(seg) + "</div>"


GLYPH = {"positive": "▲", "negative": "▼", "null": "●", "mixed": "◆"}


# ----------------------------------------------------------------------------- build

def cmd_build(a) -> None:
    root = Path(a.out)
    if cmd_check(a) and not a.force:
        sys.exit("fix the errors above (or pass --force to build anyway)")
    pdoc = load(root / "papers.json")
    papers = {p["key"]: p for p in pdoc["papers"]}
    syn = load(root / "synthesis.json")
    claims = (load(root / "claims.json", False) or {}).get("claims", [])
    conf = load(root / "conflicts.json", False) or {}
    N = Numberer(papers)
    included = [p for p in pdoc["papers"] if p.get("status") == "included"]
    base = included or [p for p in pdoc["papers"] if p.get("status") != "excluded"]

    # citations are numbered in reading order as sections render
    title = syn.get("title") or pdoc.get("query") or "Literature dossier"
    today = _dt.date.today().isoformat()
    years = [p["year"] for p in base if p.get("year")]
    topics = conf.get("topics", [])
    contested = [t for t in topics if t.get("verdict") in ("contested", "context-dependent")]

    H = []  # html body parts
    toc = []

    def section(sid, heading, inner):
        toc.append((sid, heading))
        H.append(f'<section id="{sid}"><h2>{esc(heading)}</h2>{inner}</section>')

    # summary
    lead = N.html(syn.get("summary", ""))  # number the summary's citations first
    tk = "".join(f"<li>{N.html(t)}</li>" for t in syn.get("takeaways", []))
    section("answer", "The short answer",
            f'<p class="lead">{lead}</p>' + (f'<h3>Key takeaways</h3><ol class="takeaways">{tk}</ol>' if tk else ""))

    # at a glance
    venues = Counter(p.get("venue") for p in base if p.get("venue"))
    glance = [f'<figure><figcaption>Papers per year <span class="key"><i class="sw bar"></i>peer-reviewed <i class="sw pre"></i>preprint</span></figcaption>{chart_years(base)}</figure>']
    if venues:
        glance.append(f'<figure><figcaption>Most frequent venues</figcaption>{chart_bars(venues.most_common(8), "Venues")}</figure>')
    if syn.get("themes"):
        tc = [(t["name"], len(t.get("papers", [])) or len(set(keys_in(t.get("summary", ""))))) for t in syn["themes"]]
        glance.append(f'<figure><figcaption>Papers per theme</figcaption>{chart_bars(tc, "Themes")}</figure>')
    section("glance", "The literature at a glance", '<div class="figs">' + "".join(glance) + "</div>")

    # themes
    th_html = []
    for i, t in enumerate(syn.get("themes", []), 1):
        kp = [papers[k] for k in t.get("papers", []) if k in papers]
        kp.sort(key=lambda p: p.get("year") or 0)
        lst = "".join(f'<li><span class="yr">{p.get("year") or ""}</span><a href="#ref-{esc(p["key"])}">{esc(p.get("title", ""))}</a> <sup class="cite">[{N.n(p["key"])}]</sup></li>' for p in kp)
        th_html.append(f'<article class="theme"><h3><span class="num">{i:02d}</span>{esc(t.get("name", ""))}</h3><p>{N.html(t.get("summary", ""))}</p>'
                       + (f'<details><summary>Key papers ({len(kp)})</summary><ul class="kp">{lst}</ul></details>' if kp else "") + "</article>")
    if th_html:
        section("themes", "What the literature says", "".join(th_html))

    # debates
    deb = []
    cmap = {c["id"]: c for c in claims}
    for d in syn.get("debates", []):
        topic = next((t for t in topics if t["topic"] == d.get("topic") or t.get("label") == d.get("topic")), None)
        pairs_html = ""
        for pid in d.get("pairs", []):
            if "~" not in pid:
                continue
            x, y = pid.split("~", 1)
            if x in cmap and y in cmap:
                cx, cy = cmap[x], cmap[y]
                pairs_html += ('<div class="vs">' + "".join(
                    f'<div class="side"><div class="who"><span class="g {esc(c.get("direction"))}">{GLYPH.get(c.get("direction"), "")}</span> '
                    f'{esc(author_year(papers[c["paper"]]))} <sup class="cite">[{N.n(c["paper"])}]</sup></div>'
                    f'<div>{esc(c.get("statement", ""))}</div>'
                    f'<div class="ctx">{esc(" · ".join(v for v in [c.get("population"), c.get("dataset"), c.get("method")] + list(c.get("conditions") or []) if v))}</div></div>'
                    for c in (cx, cy)) + "</div>")
        deb.append(f'<article class="debate"><h3>{esc(topic["label"] if topic else d.get("topic", ""))}</h3>'
                   + (balance(topic["directions"]) if topic else "")
                   + f'<p>{N.html(d.get("summary", ""))}</p>{pairs_html}</article>')
    if not deb and contested:
        for t in contested[:6]:
            deb.append(f'<article class="debate"><h3>{esc(t["label"])}</h3>{balance(t["directions"])}'
                       f'<p class="muted">{len(t["papers"])} papers · verdict: {esc(t["verdict"])}. See the conflict map for details.</p></article>')
    if deb:
        section("debates", "Where the evidence disagrees", "".join(deb))

    # evidence table
    if claims:
        by_topic = defaultdict(list)
        lab = {cid: t["label"] for t in topics for cid in t["claims"]}
        for c in claims:
            if c.get("paper") in papers:
                by_topic[lab.get(c["id"], f"{c.get('subject')} → {c.get('object')}")].append(c)
        rows = []
        for tl, cs in sorted(by_topic.items(), key=lambda kv: -len(kv[1])):
            rows.append(f'<tr class="grp"><th colspan="4">{esc(tl)}</th></tr>')
            for c in sorted(cs, key=lambda c: papers[c["paper"]].get("year") or 0):
                ctx = " · ".join(v for v in [c.get("population"), c.get("dataset"), c.get("method")] if v)
                rows.append(f'<tr><td><span class="g {esc(c.get("direction"))}">{GLYPH.get(c.get("direction"), "?")}</span></td>'
                            f'<td>{esc(c.get("statement", ""))}</td><td class="muted">{esc(ctx)}</td>'
                            f'<td><a href="#ref-{esc(c["paper"])}">[{N.n(c["paper"])}]</a></td></tr>')
        section("evidence", "Evidence table",
                f'<p class="muted">{len(claims)} findings extracted from the papers, grouped by relationship. ▲ positive · ▼ negative · ● no effect · ◆ depends on conditions.</p>'
                f'<div class="tbl"><table><thead><tr><th></th><th>Finding</th><th>Context</th><th>Ref</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

    # timeline
    tl = sorted([p for p in base if p.get("year")], key=lambda p: (p["year"], -(p.get("cited_by") or 0)))
    if tl:
        ann = syn.get("annotations", {})
        cut = sorted(tl, key=lambda p: -(p.get("score") or 0))[: a.timeline]
        keep = {p["key"] for p in cut}
        items, cur = [], None
        for p in tl:
            if p["key"] not in keep:
                continue
            if p["year"] != cur:
                cur = p["year"]
                items.append(f'<li class="y">{cur}</li>')
            note = ann.get(p["key"], "")
            items.append(f'<li><a href="#ref-{esc(p["key"])}">{esc(p.get("title", ""))}</a> <sup class="cite">[{N.n(p["key"])}]</sup>'
                         + (f'<div class="muted">{esc(note)}</div>' if note else "") + "</li>")
        section("timeline", "How the field developed", f'<ol class="timeline">{"".join(items)}</ol>')

    # open questions
    oq = syn.get("open_questions", [])
    if oq:
        section("open", "Open questions", '<ol class="oq">' + "".join(f"<li>{N.html(q)}</li>" for q in oq) + "</ol>")

    # bibliography — cited first (in order), then remaining included
    cited_set = list(N.order)
    rest = [p["key"] for p in base if p["key"] not in cited_set]
    for k in rest:
        N.n(k)
    bib = []
    for i, k in enumerate(N.order, 1):
        p = papers[k]
        h, _ = apa(p)
        note = syn.get("annotations", {}).get(k, "")
        bib.append(f'<li id="ref-{esc(k)}" value="{i}"><div>{h}</div>'
                   + (f'<div class="ann">{N.html(note)}</div>' if note else "")
                   + f'<div class="kk">@{esc(k)}{" · " + str(p.get("cited_by")) + " citations" if p.get("cited_by") else ""}</div></li>')
    section("refs", "Annotated bibliography", f'<ol class="bib">{"".join(bib)}</ol>')

    # methods
    slog = pdoc.get("search_log", [])
    log_rows = "".join(f'<tr><td>{esc(r.get("term"))}</td><td>{esc(r.get("source"))}</td><td>{esc(r.get("found"))}</td><td>{esc(r.get("new"))}</td><td>{esc(r.get("error", ""))}</td></tr>' for r in slog)
    st = Counter(p.get("status") for p in pdoc["papers"])
    flow = (f'<div class="flow"><div><b>{len(pdoc["papers"])}</b>records found</div><span>→</span>'
            f'<div><b>{len(pdoc["papers"]) - st.get("excluded", 0)}</b>after screening</div><span>→</span>'
            f'<div><b>{len(base)}</b>included</div><span>→</span><div><b>{len(cited_set)}</b>cited here</div></div>')
    mnote = N.html(syn.get("methods_note", "")) if syn.get("methods_note") else ""
    terms = ", ".join(f"“{esc(t)}”" for t in pdoc.get("search_terms", []))
    excl = [p for p in pdoc["papers"] if p.get("status") == "excluded" and p.get("note")]
    excl_html = ("<details><summary>Excluded papers and reasons (" + str(len(excl)) + ")</summary><ul class='kp'>"
                 + "".join(f"<li>{esc(p.get('title', ''))} — <span class='muted'>{esc(p['note'])}</span></li>" for p in excl)
                 + "</ul></details>") if excl else ""
    section("methods", "How this review was made",
            f'{flow}<p>{mnote}</p>' + (f'<p><b>Search strings:</b> {terms}</p>' if terms else "")
            + (f'<div class="tbl"><table><thead><tr><th>Search</th><th>Source</th><th>Found</th><th>New</th><th>Error</th></tr></thead><tbody>{log_rows}</tbody></table></div>' if log_rows else "")
            + excl_html
            + '<p class="muted">Paper metadata comes from OpenAlex, Semantic Scholar and arXiv records. Findings were extracted by an AI agent and should be checked against each paper before citing. Preprints are marked and have not been peer-reviewed.</p>')

    # ---- assemble html
    bibtex = bibtex_all([papers[k] for k in N.order])
    (root / "references.bib").write_text(bibtex, "utf-8")
    stats = [(len(base), "papers reviewed"), (f"{min(years)}–{max(years)}" if years else "—", "years covered")]
    if claims:
        stats.append((len(claims), "findings extracted"))
    if topics:
        stats.append((len(contested), "debates found"))
    tiles = "".join(f'<div class="tile"><b>{esc(v)}</b><span>{esc(l)}</span></div>' for v, l in stats)
    nav = "".join(f'<a href="#{sid}">{esc(h)}</a>' for sid, h in toc)
    tpl = load_template("dossier.html")
    page = (tpl.replace("__TITLE__", esc(title))
            .replace("__QUESTION__", esc(syn.get("question") or pdoc.get("query", "")))
            .replace("__BYLINE__", esc(" · ".join(x for x in [syn.get("author", ""), today] if x)))
            .replace("__TILES__", tiles).replace("__NAV__", nav).replace("__BODY__", "\n".join(H))
            .replace("/*__BIB__*/\"\"", json.dumps(bibtex).replace("</", "<\\/")))
    (root / "dossier.html").write_text(page, "utf-8")

    # ---- markdown (numbered) and pandoc
    (root / "dossier.md").write_text(build_md(syn, pdoc, papers, claims, topics, N, numbered=True), "utf-8")
    (root / "dossier.pandoc.md").write_text(build_md(syn, pdoc, papers, claims, topics, N, numbered=False), "utf-8")
    log(f"wrote dossier.html, dossier.md, dossier.pandoc.md, references.bib — {len(N.order)} references")


def build_md(syn, pdoc, papers, claims, topics, N: Numberer, numbered: bool) -> str:
    cv = (lambda t: N.md(t)) if numbered else (lambda t: t or "")
    L = []
    if not numbered:
        L += ["---", f"title: \"{(syn.get('title') or 'Literature review').replace(chr(34), '')}\"",
              f"author: \"{syn.get('author', '')}\"", f"date: {_dt.date.today().isoformat()}",
              "bibliography: references.bib", "link-citations: true", "---", ""]
    else:
        L += [f"# {syn.get('title') or 'Literature review'}", ""]
    if syn.get("question"):
        L += [f"> **Question:** {syn['question']}", ""]
    L += ["## The short answer", "", cv(syn.get("summary", "")), ""]
    if syn.get("takeaways"):
        L += ["**Key takeaways**", ""] + [f"{i}. {cv(t)}" for i, t in enumerate(syn["takeaways"], 1)] + [""]
    if syn.get("themes"):
        L += ["## What the literature says", ""]
        for t in syn["themes"]:
            L += [f"### {t.get('name', '')}", "", cv(t.get("summary", "")), ""]
    if syn.get("debates"):
        L += ["## Where the evidence disagrees", ""]
        for d in syn["debates"]:
            tp = next((t for t in topics if t["topic"] == d.get("topic") or t.get("label") == d.get("topic")), None)
            L += [f"### {tp['label'] if tp else d.get('topic', '')}", "", cv(d.get("summary", "")), ""]
    if syn.get("open_questions"):
        L += ["## Open questions", ""] + [f"{i}. {cv(q)}" for i, q in enumerate(syn["open_questions"], 1)] + [""]
    if syn.get("methods_note"):
        L += ["## How this review was made", "", cv(syn["methods_note"]), ""]
    if numbered:
        L += ["## References", ""]
        for i, k in enumerate(N.order, 1):
            _, m = apa(papers[k])
            L.append(f"{i}. {m}")
            ann = syn.get("annotations", {}).get(k)
            if ann:
                L.append(f"   - {N.md(ann)}")
        L.append("")
    else:
        L += ["## References", "", "::: {#refs}", ":::", ""]
    return "\n".join(L)


def bib_escape(s: str) -> str:
    s = s.replace("\\", "\\textbackslash{}")
    for ch in "&%$#_":
        s = s.replace(ch, "\\" + ch)
    return s


def bibtex_all(ps: list[dict]) -> str:
    out = []
    for p in ps:
        kind = "misc" if p.get("is_preprint") else ("inproceedings" if re.search(r"conference|proceedings|symposium|workshop", p.get("venue", ""), re.I) else "article")
        f = {"title": "{" + bib_escape(p.get("title", "")) + "}",
             "author": " and ".join(bib_escape(a) for a in p.get("authors", []) if a) or "Anonymous",
             "year": str(p.get("year") or "")}
        f["journal" if kind == "article" else "booktitle" if kind == "inproceedings" else "howpublished"] = bib_escape(p.get("venue") or ("Preprint" if kind == "misc" else ""))
        if p.get("doi"):
            f["doi"] = p["doi"]
        if p.get("arxiv_id"):
            f["eprint"], f["archivePrefix"] = p["arxiv_id"], "arXiv"
        if p.get("url"):
            f["url"] = p["url"]
        out.append(f"@{kind}{{{p['key']},\n" + ",\n".join(f"  {k} = {{{v}}}" for k, v in f.items() if v) + "\n}\n")
    return "\n".join(out)


def load_template(name: str) -> str:
    emb = globals().get("EMBEDDED_TEMPLATES", {})
    if name in emb:
        return emb[name]
    return (Path(__file__).resolve().parent.parent / "assets" / name).read_text("utf-8")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="dossier.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("check", help="validate synthesis.json citations")
    s.add_argument("--out", default="research")
    s.set_defaults(fn=cmd_check)
    s = sub.add_parser("build", help="write dossier.html, dossier.md, dossier.pandoc.md, references.bib")
    s.add_argument("--out", default="research")
    s.add_argument("--timeline", type=int, default=18, help="max papers on the timeline")
    s.add_argument("--force", action="store_true", help="build even if check finds errors")
    s.set_defaults(fn=cmd_build)
    a = ap.parse_args(argv)
    r = a.fn(a)
    if isinstance(r, int):
        sys.exit(r)


if __name__ == "__main__":
    main()
