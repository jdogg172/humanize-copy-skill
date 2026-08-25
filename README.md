# humanize-copy

An Agent Skill for revising English business and editorial prose without inventing facts, flattening the writer's voice, or pretending to detect authorship.

The skill has three explicit workflows:

- **Edit** rewrites a draft at the smallest useful depth.
- **Detect-only** identifies recurring machine-like patterns without rewriting.
- **Voice-profile setup** derives a reviewable profile from writing samples only when the user requests it.

## Why this skill is different

Most humanizers optimize a ban list. This one gives source fidelity and the writer's actual voice higher priority than stylistic cleanup. It treats common patterns as diagnostic triggers rather than universal prohibitions and requires missing facts to remain visible instead of being plausibly invented.

It does not assign an “AI score,” guess who wrote a passage, or promise to defeat detection tools.

## Install

Claude Code on Linux or macOS:

```bash
git clone https://github.com/jdogg172/humanize-copy-skill ~/.claude/skills/humanize-copy
```

Claude Code on Windows:

```powershell
git clone https://github.com/jdogg172/humanize-copy-skill "$env:USERPROFILE\.claude\skills\humanize-copy"
```

Other Agent Skills-compatible hosts may use a different skill directory. Install the repository as a folder named `humanize-copy` and confirm that the host discovers `SKILL.md`.

## Use

```text
Use the humanize-copy skill to edit this draft.
```

```text
Use the humanize-copy skill in detect-only mode. Do not rewrite it.
```

```text
Use the humanize-copy skill to build a private voice profile from these samples.
```

The description is intentionally narrow. Installing the skill should not silently apply a house style to every email, proposal, technical document, or compliance artifact.

## Privacy and voice profiles

Raw emails, chat exports, and writing samples should remain outside this repository. Profile creation is opt-in and produces a short, inspectable summary rather than a copy of the source corpus.

Store profiles in a private user-controlled location, use separate profiles for different people or brands, and review the generated profile before relying on it. See [references/voice-profiles.md](references/voice-profiles.md).

## Repository layout

```text
SKILL.md                    Runtime entrypoint and routing
eval.md                     Runtime self-review checklist
references/                 Guidance loaded only when relevant
evals/evals.json            Behavioral evaluation cases
evals/files/                Synthetic, non-private evaluation fixtures
scripts/validate_skill.py   Dependency-free structural validation
tests/                      Validator regression tests
```

`eval.md` checks one generated draft. `evals/evals.json` tests whether the skill improves behavior across realistic cases. They are deliberately separate.

## Validate

Requires Python 3.10 or newer and no third-party packages.

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
```

For behavioral evaluation, run every prompt in `evals/evals.json` both with this skill and against a no-skill baseline. Review factual preservation and instruction-boundary expectations before subjective style preferences. Re-run cases across multiple model executions because prose evaluation is variable.

## Known limits

- Calibrated for English business copy and editorial long-form.
- A self-review checklist cannot prove that prose is human-authored or universally natural.
- Voice matching depends on representative, lawfully available samples and human review.
- Required legal, compliance, technical, accessibility, and brand conventions override style heuristics.

## License

MIT — Millwright Labs.
