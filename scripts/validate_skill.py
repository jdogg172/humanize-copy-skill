#!/usr/bin/env python3
"""Dependency-free structural validation for the humanize-copy skill."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")
REQUIRED_FILES = (
    "SKILL.md",
    "eval.md",
    "README.md",
    "LICENSE",
    "evals/evals.json",
    "references/patterns.md",
    "references/integrity.md",
    "references/voice-profiles.md",
)
PRIVATE_EXTENSIONS = {".mbox", ".pst", ".ost"}
PRIVATE_NAMES = {"corpus.jsonl", "metrics.json", "voice-profile-draft.md"}


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) < 4 or lines[0].strip() != "---":
        return {}, ["SKILL.md must begin with YAML frontmatter"]

    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, ["SKILL.md frontmatter is missing its closing delimiter"]

    metadata: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"SKILL.md:{number}: malformed frontmatter line")
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, errors


def validate_evals(root: Path) -> list[str]:
    errors: list[str] = []
    path = root / "evals/evals.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"evals/evals.json is not readable JSON: {exc}"]

    if data.get("skill_name") != "humanize-copy":
        errors.append("evals/evals.json skill_name must be humanize-copy")

    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 5:
        return errors + ["evals/evals.json must contain at least five behavioral cases"]

    ids: set[int] = set()
    for index, case in enumerate(evals, start=1):
        label = f"eval case {index}"
        if not isinstance(case, dict):
            errors.append(f"{label} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, int) or case_id in ids:
            errors.append(f"{label} must have a unique integer id")
        else:
            ids.add(case_id)
        for field in ("prompt", "expected_output"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{label} requires a non-empty {field}")
        expectations = case.get("expectations")
        if not isinstance(expectations, list) or len(expectations) < 3:
            errors.append(f"{label} requires at least three expectations")
        files = case.get("files", [])
        if not isinstance(files, list):
            errors.append(f"{label} files must be a list")
            continue
        for relative in files:
            if not isinstance(relative, str):
                errors.append(f"{label} contains a non-string file path")
                continue
            candidate = Path(relative)
            if candidate.is_absolute() or ".." in candidate.parts:
                errors.append(f"{label} contains unsafe file path: {relative}")
            elif not (root / candidate).is_file():
                errors.append(f"{label} references missing file: {relative}")
    return errors


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if errors:
        return errors

    metadata, frontmatter_errors = parse_frontmatter(root / "SKILL.md")
    errors.extend(frontmatter_errors)
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != "humanize-copy" or not NAME_PATTERN.fullmatch(name):
        errors.append("SKILL.md name must be humanize-copy")
    if not description or len(description) > 1024:
        errors.append("SKILL.md description must be between 1 and 1024 characters")

    for markdown in (root / "SKILL.md", root / "README.md"):
        text = markdown.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_PATTERN.findall(text):
            if "://" in target or target.startswith("#"):
                continue
            if not (markdown.parent / target).resolve().is_file():
                errors.append(f"{markdown.name} references missing Markdown file: {target}")

    errors.extend(validate_evals(root))

    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in PRIVATE_EXTENSIONS:
            errors.append(f"private mail archive must not be committed: {path.relative_to(root)}")
        if path.is_file() and "profiles/private" in path.as_posix():
            errors.append(f"private profile must not be committed: {path.relative_to(root)}")
        if path.is_file() and path.name.lower() in PRIVATE_NAMES and "evals/files" not in path.as_posix():
            errors.append(f"derived private voice data must not be committed: {path.relative_to(root)}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed: frontmatter, references, privacy boundaries, and behavioral eval fixtures are structurally sound.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
