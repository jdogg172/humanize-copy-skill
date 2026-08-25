# Private Voice Profiles

Use this workflow only when the user explicitly asks to create or update a profile.

## Data boundaries

- Confirm which person or brand the profile represents and the channels it covers.
- Use only samples the user is authorized to provide.
- Keep raw email, chat, and document exports outside the skill repository.
- Do not upload samples to another service or share them with a subagent unless the user explicitly approves that use.
- Exclude secrets, credentials, private keys, tokens, CUI, regulated records, and unnecessary third-party personal information.
- Prefer local processing. Read source files in place when possible; do not duplicate the corpus merely for analysis.
- A profile is derived data and may still be sensitive. Store it in a user-controlled private location.

## Sample selection

Prefer 10–30 representative samples across the channels the profile will cover. Separate profiles when the writer uses materially different voices, such as personal email, executive communication, social posts, and brand marketing.

Avoid building a profile mainly from:

- AI-assisted drafts unless they were substantially rewritten by the user.
- Quoted or forwarded text written by someone else.
- Boilerplate signatures, disclaimers, ticket templates, or auto-replies.
- Highly constrained legal, compliance, or technical forms.

## Derivation

Record patterns supported by multiple samples:

- Audience and channels
- Register, warmth, directness, and typical level of polish
- Sentence and paragraph cadence described as ranges, not rigid rules
- Openings, transitions, closings, and calls to action
- Vocabulary, terminology, humor, contractions, and punctuation habits
- How the writer expresses uncertainty, disagreement, urgency, and trade-offs
- Strong examples or short excerpts only when needed to explain a pattern
- Explicit corrections and explicit “never use” preferences

Do not infer personality, protected characteristics, health, politics, relationships, or other sensitive traits. Do not convert absence into a prohibition.

## Profile format

```markdown
# Voice Profile: <writer or brand>

## Scope
- Owner:
- Channels:
- Intended audiences:
- Derived from:
- Last reviewed:

## Voice
- Register:
- Directness and warmth:
- Cadence:
- Paragraph shape:
- Openings and transitions:
- Closings and calls to action:

## Language
- Recurring terms and phrases:
- Technical or domain language:
- Humor and idiom:
- Punctuation and formatting:

## Decision patterns
- Uncertainty:
- Disagreement:
- Urgency:
- Trade-offs:

## Explicit preferences
- Preserve:
- Avoid:

## Confidence and gaps
- High-confidence observations:
- Channel gaps:
- Questions for review:
```

## Review and persistence

Show the derived profile to the user before saving it. Distinguish observations from explicit preferences and identify weakly supported conclusions. Persist only after approval.

Do not place the profile beside `SKILL.md`. Use a private path selected by the user or the host application's approved configuration storage. Never commit it to the public skill repository.
