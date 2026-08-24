---
name: humanize-copy
description: Use when writing or editing any human-facing prose — essays, newsletters, blog posts, website copy, marketing text, customer emails, proposals, ads, bios, product descriptions, social posts, taglines — or when someone says copy "sounds like AI", needs to sound human, or asks for a slop check on a draft. Not for code comments or internal technical docs.
---

# Humanize Copy

Write prose a reader can't clock as AI, and that reads as the writer's own rather than as competent-generic. **`eval.md` in this directory is the pass/fail gate. Run it after every draft and loop until green.**

Pick the lane first:
- **Business copy** (website, proposals, customer email, ads) → Draft rules + Integrity + guard.
- **Editorial long-form** (essays, build writeups, opinion, newsletters) → add Structure + Ownership. This is the strict lane.

**Two modes.** Default is *edit*: rewrite and deliver. *Detect-only* (the user asks for an audit, a slop check, or "what's wrong with this") names each pattern, quotes the line, gives the fix in a few words, and stops. No rewriting, no AI-detection scoring, no authorship guessing.

## Voice — make it the writer's
If `voice.md` exists in this directory, load it with every draft and judge eval §4 against it rather than against a generic target. If it doesn't exist yet, the first time you finish an edit for this user, offer once to build it: ask for 2–3 pieces they wrote themselves and are happy with (emails, posts, anything), then write down what recurs — cadence and typical sentence length, how blunt or warm, humor if any, pet words and phrases, how casual, who they usually write for. Words they'd never use go in only when the user states them or corrects an edit — never inferred from samples, which only show what they do write. Save it to `voice.md`, a page at most. If they decline the offer, write `voice.md` with the single line `declined — don't offer again` so later sessions don't re-ask. Create or update it whenever the user corrects an edit ("I'd never say that") — those corrections are better voice data than the samples. Never put invented preferences in it; only what the samples show or the user says.

**Tells are diagnostic triggers, not bans.** When one fires, ask: is it earned here, is it characteristic of this writer, does it do work at this point? If yes to all three, keep it and note `PASS — intentional: <reason>`. Judge recurrence and function, not presence. Exception: nothing in Integrity gets this escape.

## Draft rules
- Em-dashes: no clusters, no repeated grammatical use, none replacing punctuation you'd have chosen anyway. Titles and quotes fine.
- Never the antithesis patterns: "not just X, it's Y", "Not because A. Because B.", "more than X, it's Y".
- No staccato triples, no triplet adjectives, no "No X. No Y. Just Z." stacks. Enumerate only real lists of real things.
- Ban-list: the canonical word/phrase list lives in `eval.md` §1 — same list, one home.
- Cut hedging adverbs: really, just, actually, truly, simply, quite, rather.
- No trailing "-ing" analysis clauses ("…, ensuring/protecting/preserving…").
- No colon reveals ("The detail that makes it work: a separate agent grades it"), faux-insight setups ("here's what nobody tells you"), or audience flattery ("whether you're a solo founder or a Fortune 500 exec").
- No weasel attribution ("studies show", "experts agree"). Name the source or cut the claim.
- No importance puffery ("stands as a testament"), synonym cycling (rotating words for the same thing), or abstract-noun fog ("created a shift in my relationship to ambition").
- No reader simulation ("you can probably imagine how that felt").
- No both-sides hedging ("while X offers benefits, challenges remain"). A named trade-off is honest; a symmetric hedge is filler.
- Formatting follows content: no emoji headings, no decorative mid-sentence bold, no bullets where two sentences read better, no headers over two-sentence sections.
- One punchy short sentence per page max. No verbatim repeats across paragraphs or pages.

## Structure — long-form only
- Outline the draft **after** writing it. A symmetric outline (setup → three parallel sections → distilled lesson) means it's a template. Merge, reorder, or cut sections that exist only for neatness.
- Uneven section lengths. Let at least one anecdote end without an interpretation paragraph.
- Transitions express real relationships (contradiction, consequence, time jump), not "First," / "This brings us to,".
- No premature meaning-making. Not every event becomes a lesson; ambiguity and unresolved tension are allowed to stand.
- Keep the example that tests or complicates the claim. Delete category coverage ("in business, relationships, and creative work").
- Preserve epistemic history — what was suspected, what's still unresolved — instead of seamless certainty ("I realized the real problem was…").
- Openings: no cinematic cold open, no throat-clearing universal ("We live in an age of…"). First screen needs a concrete reason to keep reading.
- Subhead adds information; it doesn't restate the title.
- **End on a concrete point or next action.** No recap, no "In conclusion", no reader-service padding. A fake-profound kicker gets **deleted**, never rewritten into a better metaphor. This is the highest-value rule here.
- Don't front-load every unit. Delayed context is fine when it creates real discovery, not manufactured suspense.

## Integrity — no exceptions, no `PASS — intentional`
An invented number in a proposal is a business problem, not a style problem.

- Never manufacture what the writer saw, said, felt, thought, or remembers. No reconstructed dialogue, motives, or emotions. Gaps get `[TK — ask]` and a question.
- No synthetic scene detail ("the coffee had gone cold as rain tapped the window") added for literary texture.
- Facts, numbers, claims, comparisons, dates come from source material or the writer. Missing specific → `[TK]` and ask. Never a plausible guess.
- No invented credentials, capabilities, past clients, or results.
- Verify every quote, attribution, title, date, and link. Link primary sources. Distinguish quotation from paraphrase. Say why a source is in the piece.
- No paraphrase inflation: label what the source says vs. what the writer infers.
- No interpretive overreach past what the evidence supports.

## What to do instead
- Concrete specifics carry the piece: numbers, street and neighborhood names, materials, years, named jobs, commands, failures. Keep facts, cut rhetoric.
- Protect the specific fact — never smooth a useful number into generic importance.
- One idea per sentence, one topic per paragraph. Make verbs do the work ("made a decision" → "decided"). Active voice with human subjects.
- Preserve useful edge. An opinion sanded into balance is worse than no opinion.
- Vary sentence length. Contractions. Plain words: use, help, fix.
- Read-aloud test — business copy: would you say it to a customer face to face? Editorial: would you say it to a sharp friend who'd push back?
- State trade-offs honestly. Trade jargon used casually, explained once.

## Ownership test — run last, weigh heaviest
For every paragraph: **what does this contain that the writer specifically knows, noticed, believes, remembers, or is willing to risk saying?** Any paragraph that could be published unchanged under a competent stranger's name gets revised with verified experience, sharper judgment, or real evidence — or deleted. Never invent personal material to make it pass; that fails Integrity, which outranks this.

This is the check that survives everything else. Stripping tells produces clean prose anyone could have written, and the tell list is now itself a recognizable machine style (uniform short declaratives, sparse punctuation, rationed specificity). Clearing the list is the floor.

## Newsletter mechanics — email sends only
Subject line represents the piece accurately; no clickbait, no false intimacy, no fake re:/fwd:. Preview text complements rather than repeats it. CTA only when there's a real action wanted — reflexive "What do you think? Reply and let me know" is slop, and not every issue needs one. Sign-off sounds habitual, not like a brand template.

## Overcorrection guard
No forced slang, no fragments-everywhere, no fake-casual, no typos-on-purpose. Target voice: plain, confident, concrete, lightly warm. Cutting stays proportional to the actual slop — aggressive compression strips character, and a strong human sentence gets left alone.

## Delegating to a subagent
Skills don't auto-load for subagents. Paste Draft rules + Integrity + Overcorrection guard into any subagent brief that writes prose, plus Structure + Ownership for long-form.

## Before delivering
Run **`eval.md`**. Fix every FAIL, re-run, and don't deliver until it's green. Output the full draft plus a short **What changed** section, and list any `PASS — intentional` calls with their reasons.
