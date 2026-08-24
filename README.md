# humanize-copy

An Agent Skill that edits prose so a reader can't clock it as AI, without sanding off the writer's own voice while it's at it.

Works in Claude Code, Claude Desktop, and anything else that reads Agent Skills. Two files, no dependencies.

## Install

```bash
git clone https://github.com/millwright-labs/humanize-copy-skill ~/.claude/skills/humanize-copy
```

Windows (PowerShell):

```powershell
git clone https://github.com/millwright-labs/humanize-copy-skill "$env:USERPROFILE\.claude\skills\humanize-copy"
```

Or hand the repo URL to your agent and ask it to install the skill. Restart your session and it's live.

## Use

It loads on its own whenever the agent writes or edits human-facing prose — website copy, emails, essays, newsletters, proposals, social posts. You can also invoke it directly:

```
Use the humanize-copy skill on this draft.
```

Two modes. The default is *edit*: it rewrites, then reports what changed and why. Ask for "a slop check" or "an audit" instead and it switches to *detect-only*. For each problem it names the pattern, quotes the offending line, and gives the fix in a few words, then stops and waits. It never scores a draft for "how AI it sounds" and never guesses who wrote something.

## Make it yours

The tell-stripping works with no setup. Knowing your voice is the part a fresh clone can't do, so the skill builds that knowledge itself: after its first edit it offers to make a voice profile. Paste two or three things you wrote yourself and liked, and it records what recurs — cadence, bluntness, pet words, words you'd never use — in a `voice.md` beside the skill. Every edit after that is judged against your voice instead of a generic target.

When it gets you wrong, tell it ("I'd never say that") and it updates the file. Corrections are better voice data than samples. You can also write `voice.md` by hand and skip the interview.

## What's inside

`SKILL.md` carries the rules. A sentence-level pass catches the recognizable machine patterns: em-dash pileups, "not just X, it's Y", staccato triples, a ban-list of words like *delve* and *seamless*, weasel attribution. A structure pass for long-form catches the subtler tells: symmetric essay skeletons, every anecdote getting its own interpretation paragraph, fake-profound kickers. An integrity section bars invented quotes, numbers, credentials, and experiences outright; gaps get a `[TK]` marker and a question instead of a plausible guess.

The check that matters most runs last. Stripping the obvious tells produces clean prose anyone could have written — which has become its own recognizable style. So every paragraph has to answer for what it contains that the writer specifically knows, noticed, or is willing to risk saying. A paragraph that could ship unchanged under a stranger's name gets revised or cut.

`eval.md` is a pass/fail checklist the agent runs on its own output. It loops until every applicable line passes, and an overcorrection guard keeps the fix from becoming the disease: no forced slang, no fragments-everywhere, no fake-casual.

## Known limits

The rules are calibrated for English business copy and editorial long-form. Code comments and internal technical docs are out of scope, and the skill says so rather than editing them anyway. The tell catalog reflects the models of 2025–2026; as house styles shift, expect the ban-list to need pruning.

## License

MIT — Millwright Labs.
