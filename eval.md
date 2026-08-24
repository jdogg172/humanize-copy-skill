# Humanize-Copy Eval Gate

Run after every draft or edit. This is a **gate**, not a habit: fix failures and re-run until every applicable line passes.

**Verdicts:** `PASS` · `FAIL` · `PASS — intentional: <one-line reason>` (style layers only — never available in §3) · `N/A` (wrong medium).

Scoring a draft for "how AI does this sound" is not a verdict. Don't do it, and don't guess whether AI wrote something.

---

## 1. Sentence-level

- [ ] Em-dashes: no clusters, no repeated grammatical use, none standing in for punctuation the writer would have picked
- [ ] No antithesis ("not just X, it's Y" / "Not because A. Because B.")
- [ ] No staccato triples, triplet adjectives, or "No X. No Y. Just Z." stacks
- [ ] Ban-list clear: dramatically, seamless, elevate, unrivaled, meticulous, utmost, delve, leverage, harness, foster, unlock, transform, boasts, nestled, testament, tapestry, time-honored, "the result is", "stands as", "stand the test of time", "In today's…", "the ideal solution", "peace of mind", "look no further"
- [ ] Hedging adverbs cut: really, just, actually, truly, simply, quite, rather
- [ ] No trailing "-ing" analysis clauses ("…, ensuring/protecting/preserving…")
- [ ] No colon reveals, faux-insight setups, or audience flattery
- [ ] No weasel attribution ("studies show", "experts agree") — source named or claim cut
- [ ] No importance puffery, synonym cycling, or abstract-noun fog
- [ ] No reader simulation ("you can probably imagine", "we've all been there")
- [ ] No both-sides hedging (a *named* trade-off passes; a symmetric hedge fails)
- [ ] Formatting clean: no emoji headings, no decorative mid-sentence bold, no bullets where prose reads better, no headers over two-sentence sections
- [ ] No verbatim repeats across paragraphs or pages

## 2. Structure — long-form only

- [ ] Outlined the draft after writing. Outline is **not** symmetric (no setup → three parallel sections → distilled lesson)
- [ ] Section lengths uneven; at least one anecdote left without an interpretation paragraph
- [ ] Transitions express real relationships, not tour-guide signposting
- [ ] No premature meaning-making; ambiguity and unresolved tension survived where honest
- [ ] Examples test or complicate the claim rather than covering categories
- [ ] Epistemic history preserved (what was suspected, what's still unresolved) instead of seamless certainty
- [ ] Opening is not a cinematic cold open or a throat-clearing universal; first screen gives a concrete reason to continue
- [ ] Subhead adds information rather than restating the title
- [ ] **Ends on a concrete point or next action** — no recap, no "In conclusion", and no fake-profound kicker. A kicker gets **deleted**, never rewritten into a better metaphor
- [ ] No reader-service padding at section ends

## 3. Integrity — no `PASS — intentional` available on any line here

- [ ] Zero invented experience: nothing the writer saw, said, felt, thought, or remembers was manufactured. No reconstructed dialogue, motives, or emotions
- [ ] Zero synthetic scene detail added for literary texture
- [ ] Zero invented numbers, claims, comparisons, or dates. Every gap is a `[TK]` with a question, not a plausible guess
- [ ] Every quote, attribution, title, date, and link verified. Primary sources linked. Quotation distinguished from paraphrase
- [ ] No paraphrase inflation — boundary labeled between what the source says and what the writer infers
- [ ] No interpretive overreach beyond what the evidence supports

## 4. Voice and proportion

- [ ] Writer would recognize this as theirs: vocabulary, cadence, bluntness, humor, uncertainty, digressions, polish level intact
- [ ] If `voice.md` exists, the draft was checked against it — pet words preserved where they occurred (never inserted to satisfy this line), never-words absent, register matches
- [ ] Strong human sentences left alone rather than flattened for consistency
- [ ] Cutting proportional to actual slop — no aggressive compression that stripped character
- [ ] Useful edge preserved; no opinion sanded into balance
- [ ] Overcorrection guard clean: no forced slang, no fragments-everywhere, no fake-casual, no typos-on-purpose
- [ ] Not merely "anti-slop-processed": the draft doesn't read as uniform short declaratives with rationed specificity
- [ ] Reads naturally aloud (business copy: to a customer face to face. Editorial: to a sharp friend who'd push back)

## 5. Ownership — run last, weigh heaviest

- [ ] Every paragraph answers: **what does this contain that the writer specifically knows, noticed, believes, remembers, or is willing to risk saying?**
- [ ] No paragraph could be published unchanged under a competent stranger's name
- [ ] Nothing personal was invented to make a paragraph pass this test

## 6. Newsletter — email sends only

- [ ] Subject line represents the piece accurately. No clickbait, no false intimacy
- [ ] Preview text complements the subject rather than repeating it
- [ ] CTA reflects a real desired action, or is absent. No reflexive "What do you think? Reply and let me know"
- [ ] Sign-off sounds habitual and personal, not like a brand template

## 7. Delivery

- [ ] Edit checked against the actual source (file or pasted draft), not a remembered version
- [ ] Output includes the full draft plus a short **What changed** section
- [ ] Any `PASS — intentional` verdicts listed with their reasons

---

## Detect-only mode

Same rules, no rewriting. For each hit: **name the pattern · quote the offending line · give the fix in a few words.** Then stop. Do not rewrite the draft, do not score it, do not speculate about authorship. Wait for the user to ask for the edit.
