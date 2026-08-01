#!/usr/bin/env python3
"""Dump theorem-like statements from the master manuscript beside their Lean counterparts.

The matcher is deliberately conservative.  A blank Lean column is preferable
to claiming that a scalar ``*_core`` lemma formalizes a complete manuscript
theorem.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import asdict, dataclass, replace
from difflib import SequenceMatcher
from pathlib import Path


THEOREM_ENVS = ("theorem", "lemma", "proposition", "corollary", "conjecture")
STOP_WORDS = {
    "a", "an", "and", "at", "bound", "by", "constant", "core", "exact",
    "for", "from", "in", "inequality", "lemma", "of", "on", "one", "part",
    "proposition", "the", "theorem", "to", "under", "with",
}
LEAN_DECL = re.compile(
    r"(?m)^(?P<kw>theorem|lemma|example)\s+(?P<name>[A-Za-z_][\w'.]*)"
)
PART_RE = re.compile(r"\\part\{Part\s+([A-G])\b", re.I)
BEGIN_RE = re.compile(
    r"\\begin\{(" + "|".join(THEOREM_ENVS) + r")\}"
    r"(?:\[(?P<title>[^\]]*)\])?",
    re.I,
)
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
DOC_RE = re.compile(r"/--(?P<body>.*?)--/\s*$", re.S)


@dataclass
class ManuscriptItem:
    index: int
    part: str
    kind: str
    title: str
    label: str
    line: int
    source: str
    remark: str = ""


@dataclass
class LeanItem:
    name: str
    line: int
    file: str
    doc: str
    source: str
    remark: str = ""
    status: str = ""


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def strip_tex(value: str) -> str:
    value = re.sub(r"\\(?:Cref|cref|eqref|ref)\{([^}]*)\}", r"\1", value)
    value = re.sub(r"\\[A-Za-z@]+(?:\[[^\]]*\])?", " ", value)
    value = value.replace("{", " ").replace("}", " ").replace("~", " ")
    return re.sub(r"\s+", " ", value).strip()


def tokens(value: str) -> set[str]:
    value = re.sub(r"([a-z])([A-Z])", r"\1 \2", value)
    words = re.findall(r"[a-z0-9]+", value.lower().replace("_", " "))
    return {word for word in words if len(word) > 1 and word not in STOP_WORDS}


def extract_manuscript(path: Path) -> list[ManuscriptItem]:
    text = path.read_text(encoding="utf-8")
    parts = [(m.start(), m.group(1).upper()) for m in PART_RE.finditer(text)]
    # Part A is the front part of this manuscript and has no explicit \part
    # command.  Material after \appendix is supporting material, not Part G.
    appendix_match = re.search(r"(?m)^\\appendix\b", text)
    parts_end = appendix_match.start() if appendix_match else len(text)
    items: list[ManuscriptItem] = []
    for match in BEGIN_RE.finditer(text):
        if match.start() >= parts_end:
            continue
        end_marker = rf"\end{{{match.group(1)}}}"
        end = text.find(end_marker, match.end())
        if end < 0:
            raise ValueError(f"unclosed {match.group(1)} at {path}:{line_number(text, match.start())}")
        end += len(end_marker)
        part = "A"
        for offset, candidate in parts:
            if offset > match.start():
                break
            part = candidate
        if part not in "ABCDEFG":
            continue
        source = text[match.start():end].strip()
        label_match = LABEL_RE.search(source)
        label = label_match.group(1) if label_match else ""
        title = strip_tex(match.group("title") or label.replace("-", " "))
        kind = match.group(1).lower()
        notes = []
        if kind == "conjecture":
            notes.append("Open conjecture; a Lean theorem should only encode a conditional implication.")
        if not label:
            notes.append("No manuscript label; automatic matching is less reliable.")
        items.append(ManuscriptItem(
            index=len(items) + 1, part=part, kind=kind, title=title,
            label=label, line=line_number(text, match.start()), source=source,
            remark=" ".join(notes),
        ))
    return items


def declaration_end(text: str, start: int) -> int:
    next_decl = re.search(
        r"(?m)^(?:/--|theorem\s+|lemma\s+|example\s+|def\s+|"
        r"noncomputable\s+def\s+|inductive\s+|structure\s+|namespace\s+|end\b)",
        text[start + 1:],
    )
    return len(text) if next_decl is None else start + 1 + next_decl.start()


def extract_lean(lean_dir: Path) -> list[LeanItem]:
    result: list[LeanItem] = []
    for path in sorted(lean_dir.glob("*.lean")):
        text = path.read_text(encoding="utf-8")
        for match in LEAN_DECL.finditer(text):
            # Attach the immediately preceding doc comment, when present.
            prefix = text[:match.start()]
            doc_match = DOC_RE.search(prefix)
            block_start = doc_match.start() if doc_match else match.start()
            doc = re.sub(r"\s+", " ", doc_match.group("body")).strip() if doc_match else ""
            end = declaration_end(text, match.start())
            source = text[block_start:end].strip()
            lowered = f"{match.group('name')} {doc}".lower()
            notes = []
            if any(word in lowered for word in (" core", "_core", "scalar endpoint", "abstract ")):
                notes.append("Partial counterpart: algebraic/scalar core only.")
            if any(word in lowered for word in ("explicit hypothesis", "under the hypothesis", "assumed")):
                notes.append("Conditional counterpart: the open input is an explicit hypothesis.")
            result.append(LeanItem(
                name=match.group("name"), line=line_number(text, match.start()),
                file=path.as_posix(), doc=doc, source=source,
                remark=" ".join(notes),
            ))
    return result


def part_hint(item: LeanItem) -> str:
    match = re.search(r"(?:part|fei_part_)([a-g])", f"{item.name} {item.file}", re.I)
    return match.group(1).upper() if match else ""


def similarity(manuscript: ManuscriptItem, lean: LeanItem) -> float:
    left = " ".join((manuscript.title, manuscript.label.replace("-", " ")))
    right = " ".join((lean.name, lean.doc))
    lt, rt = tokens(left), tokens(right)
    if not lt or not rt:
        return 0.0
    overlap = len(lt & rt) / len(lt | rt)
    sequence = SequenceMatcher(None, " ".join(sorted(lt)), " ".join(sorted(rt))).ratio()
    containment = len(lt & rt) / len(lt)
    score = 0.45 * overlap + 0.25 * sequence + 0.30 * containment
    hint = part_hint(lean)
    if hint and hint != manuscript.part:
        score *= 0.25
    elif hint == manuscript.part:
        score += 0.08
    return min(score, 1.0)


def load_overrides(path: Path | None) -> dict[str, object]:
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("correspondence file must be a JSON object")
    return data


def manuscript_key(item: ManuscriptItem) -> str:
    return item.label or f"{item.part}:{item.index}"


def match_items(
    manuscripts: list[ManuscriptItem],
    lean_items: list[LeanItem],
    overrides: dict[str, object],
    threshold: float,
) -> list[tuple[ManuscriptItem, LeanItem | None, float]]:
    by_name = {item.name: item for item in lean_items}
    matches = []
    for manuscript in manuscripts:
        key = manuscript_key(manuscript)
        if key in overrides:
            entry = overrides[key]
            if isinstance(entry, dict):
                name = entry.get("lean")
                manuscript = replace(
                    manuscript,
                    remark=str(entry.get("manuscript_remark", manuscript.remark)),
                )
                curated_lean_remark = str(entry.get("lean_remark", ""))
                status = str(entry.get("status", "curated"))
            else:
                name = entry
                curated_lean_remark = ""
                status = "curated"
            if name is None:
                if not manuscript.remark:
                    manuscript = replace(
                        manuscript,
                        remark="No corresponding Lean declaration was found in the current repository.",
                    )
                matches.append((manuscript, None, 1.0))
                continue
            if not isinstance(name, str):
                raise ValueError(f"correspondence for {key!r} must use a Lean name string or null")
            if name not in by_name:
                raise ValueError(f"correspondence for {key!r} names unknown Lean declaration {name!r}")
            lean = by_name[name]
            scope = f"Curated classification: {status} counterpart."
            lean = replace(
                lean,
                remark=" ".join(filter(None, (scope, curated_lean_remark, lean.remark))),
                status=status,
            )
            matches.append((manuscript, lean, 1.0))
            continue
        candidates = sorted(
            ((similarity(manuscript, lean), lean) for lean in lean_items),
            key=lambda pair: pair[0], reverse=True,
        )
        score, lean = candidates[0] if candidates else (0.0, None)
        matches.append((manuscript, lean if score >= threshold else None, score))
    return matches


def combined_remarks(
    manuscript: ManuscriptItem, lean: LeanItem | None, score: float, threshold: float
) -> tuple[str, str]:
    manuscript_note = manuscript.remark
    if lean is None:
        extra = "No sufficiently confident Lean counterpart was found."
        manuscript_note = f"{manuscript_note} {extra}".strip()
        return manuscript_note, "Missing counterpart."
    lean_note = lean.remark
    if manuscript.kind == "conjecture":
        lean_note = (
            f"{lean_note} This is at most a conditional encoding; it does not "
            "constitute a proof of the manuscript conjecture."
        ).strip()
    if score < threshold + 0.12:
        lean_note = f"{lean_note} Heuristic match; review this pairing.".strip()
    if not lean_note:
        lean_note = "Candidate full counterpart; verify semantic scope before citing formalization."
    return manuscript_note or "No special manuscript-side remark.", lean_note


def status_group(manuscript: ManuscriptItem, lean: LeanItem | None) -> str:
    """Coarse display class without weakening the exact ledger wording."""
    if lean is None:
        return "unmatched"
    if lean.status == "full":
        return "complete"
    if manuscript.kind == "conjecture" or "open" in lean.status.lower():
        return "open"
    return "incomplete"


def render_markdown(
    matches: list[tuple[ManuscriptItem, LeanItem | None, float]],
    manuscript_path: Path,
    threshold: float,
) -> str:
    lines = [
        "# Manuscript theorems and Lean counterparts",
        "",
        f"Generated from `{manuscript_path.as_posix()}`. Matches below 100% are "
        "heuristic unless supplied through an override file. “Partial counterpart” "
        "does not certify the complete manuscript statement.",
        "",
    ]
    current_part = ""
    for manuscript, lean, score in matches:
        if manuscript.part != current_part:
            current_part = manuscript.part
            lines += [f"## Part {current_part}", ""]
        title = manuscript.title or manuscript.label or f"unnamed {manuscript.kind}"
        manuscript_note, lean_note = combined_remarks(manuscript, lean, score, threshold)
        lean_location = (
            f"`{lean.file}:{lean.line}` · "
            + ("curated correspondence" if score == 1.0 else f"match score `{score:.2f}`")
            if lean else f"No match · best score `{score:.2f}`"
        )
        left = (
            f"<b>{html.escape(manuscript.kind.title())}</b><br>"
            f"<code>{html.escape(manuscript.label or '(no label)')}</code><br>"
            f"<small>{html.escape(manuscript_path.as_posix())}:{manuscript.line}</small>"
            f"<pre>{html.escape(manuscript.source)}</pre>"
            f"<b>Remark:</b> {html.escape(manuscript_note)}"
        )
        right_source = html.escape(lean.source) if lean else "(none)"
        right_name = html.escape(lean.name) if lean else "No Lean counterpart found"
        status_line = (
            f"<b>Ledger status:</b> <code>{html.escape(lean.status)}</code><br>"
            if lean and lean.status else ""
        )
        right = (
            f"<b>{right_name}</b><br><small>{html.escape(lean_location)}</small>"
            f"<br>{status_line}<pre>{right_source}</pre>"
            f"<b>Remark:</b> {html.escape(lean_note)}"
        )
        lines += [
            f"### {manuscript.index}. {title}",
            "",
            "<table><tr><th width=\"50%\">Manuscript</th>"
            "<th width=\"50%\">Lean counterpart</th></tr>",
            f"<tr><td valign=\"top\">{left}</td><td valign=\"top\">{right}</td></tr></table>",
            "",
        ]
    return "\n".join(lines)


def render_html(
    matches: list[tuple[ManuscriptItem, LeanItem | None, float]],
    manuscript_path: Path,
    threshold: float,
) -> str:
    rows: list[str] = []
    current_part = ""
    for manuscript, lean, score in matches:
        if manuscript.part != current_part:
            current_part = manuscript.part
            rows.append(f'<h2 id="part-{current_part.lower()}">Part {current_part}</h2>')
        title = manuscript.title or manuscript.label or f"unnamed {manuscript.kind}"
        manuscript_note, lean_note = combined_remarks(manuscript, lean, score, threshold)
        lean_location = (
            f"{lean.file}:{lean.line} · "
            + ("curated correspondence" if score == 1.0 else f"match score {score:.2f}")
            if lean else f"No match · best score {score:.2f}"
        )
        lean_name = lean.name if lean else "No Lean counterpart found"
        lean_source = lean.source if lean else "(none)"
        group = status_group(manuscript, lean)
        ledger_status = lean.status if lean and lean.status else "unmatched"
        rows.append(
            f"""
<article class="statement status-{group}" data-status="{html.escape(group)}">
  <h3>{manuscript.index}. {html.escape(title)}
    <span class="status-badge">{html.escape(ledger_status)}</span></h3>
  <div class="columns">
    <section>
      <h4>Manuscript</h4>
      <div class="meta"><strong>{html.escape(manuscript.kind.title())}</strong>
        · <code>{html.escape(manuscript.label or "(no label)")}</code>
        · {html.escape(manuscript_path.as_posix())}:{manuscript.line}</div>
      <pre>{html.escape(manuscript.source)}</pre>
      <p class="remark"><strong>Remark:</strong> {html.escape(manuscript_note)}</p>
    </section>
    <section>
      <h4>Lean counterpart</h4>
      <div class="meta"><strong>{html.escape(lean_name)}</strong>
        · {html.escape(lean_location)}</div>
      <pre>{html.escape(lean_source)}</pre>
      <p class="remark"><strong>Remark:</strong> {html.escape(lean_note)}</p>
    </section>
  </div>
</article>"""
        )
    matched = sum(lean is not None for _, lean, _ in matches)
    complete = sum(
        status_group(manuscript, lean) == "complete"
        for manuscript, lean, _ in matches
    )
    open_count = sum(
        status_group(manuscript, lean) == "open"
        for manuscript, lean, _ in matches
    )
    incomplete = len(matches) - complete - open_count - (len(matches) - matched)
    navigation = " ".join(
        f'<a href="#part-{part.lower()}">Part {part}</a>' for part in "ABCDEFG"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Manuscript theorems and Lean counterparts</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, sans-serif; }}
    body {{ margin: 0 auto; max-width: 1800px; padding: 1.5rem; line-height: 1.45; }}
    header {{ position: sticky; top: 0; z-index: 2; padding: 1rem;
      background: Canvas; border-bottom: 1px solid color-mix(in srgb, CanvasText 25%, transparent); }}
    nav a {{ margin-right: .8rem; }}
    h2 {{ margin-top: 2.5rem; border-bottom: 2px solid #6b7cff; padding-bottom: .3rem; }}
    .statement {{ margin: 1.25rem 0 2rem; }}
    .status-badge {{ display: inline-block; margin-left: .5rem; padding: .12rem .45rem;
      border-radius: 999px; font-size: .72em; font-weight: 600; vertical-align: middle;
      background: color-mix(in srgb, CanvasText 10%, Canvas); }}
    .status-complete .status-badge {{ background: color-mix(in srgb, #2fa866 28%, Canvas); }}
    .status-incomplete .status-badge {{ background: color-mix(in srgb, #e8a832 28%, Canvas); }}
    .status-open .status-badge {{ background: color-mix(in srgb, #c46b32 28%, Canvas); }}
    .columns {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 1rem; }}
    section {{ min-width: 0; padding: 1rem; border: 1px solid color-mix(in srgb, CanvasText 22%, transparent);
      border-radius: .6rem; }}
    .status-unmatched section:last-child {{ border-color: #c46b32; }}
    .meta {{ margin-bottom: .75rem; opacity: .8; overflow-wrap: anywhere; }}
    pre {{ margin: 0; padding: .9rem; overflow: auto; white-space: pre-wrap; overflow-wrap: anywhere;
      background: color-mix(in srgb, CanvasText 7%, Canvas); border-radius: .35rem; tab-size: 2; }}
    .remark {{ padding: .65rem; background: color-mix(in srgb, #e8a832 15%, Canvas); border-radius: .35rem; }}
    @media (max-width: 900px) {{ .columns {{ grid-template-columns: 1fr; }} header {{ position: static; }} }}
    @media print {{ header {{ position: static; }} .statement {{ break-inside: avoid; }} }}
  </style>
</head>
<body>
<header>
  <h1>Manuscript theorems and Lean counterparts</h1>
  <p>{len(matches)} statements: {complete} complete formalizations,
    {incomplete} partial/conditional or special-case links, {open_count} open conjectural
    interfaces, and {len(matches) - matched} with no declaration. A linked declaration is
    not automatically a complete counterpart.</p>
  <nav>{navigation}</nav>
</header>
<main>
{''.join(rows)}
</main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuscript", type=Path, default=Path("master.tex"))
    parser.add_argument("--lean-dir", type=Path, default=Path("lean"))
    parser.add_argument("--output", type=Path, default=Path("theorems_with_lean.md"))
    parser.add_argument(
        "--overrides", type=Path,
        help="curated JSON correspondence ledger (defaults to scripts/theorem_lean_correspondence.json)",
    )
    parser.add_argument("--threshold", type=float, default=0.55)
    parser.add_argument("--format", choices=("markdown", "html", "json"), default="markdown")
    args = parser.parse_args()

    manuscripts = extract_manuscript(args.manuscript)
    lean_items = extract_lean(args.lean_dir)
    correspondence = args.overrides
    if correspondence is None:
        default_correspondence = Path(__file__).with_name("theorem_lean_correspondence.json")
        correspondence = default_correspondence if default_correspondence.exists() else None
    matches = match_items(
        manuscripts, lean_items, load_overrides(correspondence), args.threshold
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "json":
        payload = []
        for manuscript, lean, score in matches:
            manuscript_note, lean_note = combined_remarks(manuscript, lean, score, args.threshold)
            row = {
                "manuscript": asdict(manuscript),
                "lean": asdict(lean) if lean else None,
                "score": round(score, 4),
                "manuscript_remark": manuscript_note,
                "lean_remark": lean_note,
            }
            payload.append(row)
        output = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    elif args.format == "html":
        output = render_html(matches, args.manuscript, args.threshold)
    else:
        output = render_markdown(matches, args.manuscript, args.threshold)
    args.output.write_text(output, encoding="utf-8")
    matched = sum(lean is not None for _, lean, _ in matches)
    print(f"Wrote {len(matches)} statements ({matched} matched, {len(matches) - matched} unmatched) to {args.output}")


if __name__ == "__main__":
    main()
