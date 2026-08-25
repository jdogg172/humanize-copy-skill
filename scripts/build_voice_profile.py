#!/usr/bin/env python3
"""Build a private, redacted voice corpus and reviewable profile locally."""

from __future__ import annotations

import argparse
import collections
import email.policy
import hashlib
import html
import json
import mailbox
import re
import statistics
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import date
from email.message import Message
from html.parser import HTMLParser
from pathlib import Path


EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
URL_RE = re.compile(r"\b(?:https?://|www\.)\S+", re.I)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]?\d{4}(?!\w)")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
UUID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I)
SECRET_RE = re.compile(r"\b(?:[A-Za-z0-9+/]{32,}={0,2}|[0-9a-f]{32,})\b")
LONG_NUMBER_RE = re.compile(r"\b\d{6,}\b")
QUOTE_START_RE = re.compile(r"^(?:On .+ wrote:|From:\s|Sent:\s|To:\s|Subject:\s|[- ]*Original Message[- ]*)", re.I)
WORDS_RE = re.compile(r"\b[\w’']+\b", re.UNICODE)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
SIGNOFFS = {"regards", "best", "best regards", "thanks", "thank you", "respectfully", "sincerely", "cheers"}


@dataclass(frozen=True)
class Sample:
    channel: str
    text: str
    source_key: str


def redact(text: str) -> str:
    text = html.unescape(text).replace("\u200b", " ").replace("\xa0", " ")
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = URL_RE.sub("[URL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    text = IP_RE.sub("[IP]", text)
    text = UUID_RE.sub("[ID]", text)
    text = SECRET_RE.sub("[TOKEN]", text)
    text = LONG_NUMBER_RE.sub("[NUMBER]", text)
    return text


def clean_text(text: str) -> str:
    kept: list[str] = []
    for raw in text.replace("\r\n", "\n").replace("\r", "\n").splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line:
            if kept and kept[-1] != "":
                kept.append("")
            continue
        if line.startswith(">") or QUOTE_START_RE.match(line):
            break
        if line.lower().rstrip(",.!:") in SIGNOFFS:
            kept.append(line)
            break
        kept.append(line)
    return redact("\n".join(kept).strip())


def message_body(message: Message) -> str:
    if message.is_multipart():
        parts: list[str] = []
        for part in message.walk():
            if part.get_content_disposition() == "attachment":
                continue
            if part.get_content_type() == "text/plain":
                try:
                    parts.append(part.get_content())
                except Exception:
                    continue
        return "\n".join(parts)
    try:
        return message.get_content() if message.get_content_type() == "text/plain" else ""
    except Exception:
        payload = message.get_payload(decode=True)
        return payload.decode(message.get_content_charset() or "utf-8", errors="replace") if payload else ""


def gmail_samples(takeout_zip: Path, owner_emails: set[str]) -> list[Sample]:
    with zipfile.ZipFile(takeout_zip) as archive:
        names = [name for name in archive.namelist() if name.lower().endswith(".mbox")]
        if not names:
            raise ValueError("No MBOX file found in Gmail Takeout archive")
        with tempfile.TemporaryDirectory(prefix="voice-mbox-") as temporary:
            mbox_path = Path(temporary) / "sent.mbox"
            with archive.open(names[0]) as source, mbox_path.open("wb") as destination:
                while chunk := source.read(1024 * 1024):
                    destination.write(chunk)
            box = mailbox.mbox(mbox_path, factory=lambda f: email.message_from_binary_file(f, policy=email.policy.default))
            samples: list[Sample] = []
            for index, message in enumerate(box):
                sender = (message.get("From") or "").lower()
                if owner_emails and not any(address in sender for address in owner_emails):
                    continue
                text = clean_text(message_body(message))
                if len(WORDS_RE.findall(text)) >= 3:
                    samples.append(Sample("email", text, f"gmail:{index}"))
            return samples


class TeamsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[set[str]] = []
        self.author_depth = 0
        self.content_depth = 0
        self.buffer: list[str] = []
        self.messages: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = set(dict(attrs).get("class", "").split())
        self.stack.append(classes)
        if "message--author" in classes:
            self.author_depth = len(self.stack)
        if self.author_depth and "message__content" in classes:
            self.content_depth = len(self.stack)
            self.buffer = []
        if self.content_depth and tag in {"br", "p", "div", "li"} and self.buffer:
            self.buffer.append("\n")

    def handle_endtag(self, tag: str) -> None:
        depth = len(self.stack)
        if self.content_depth == depth:
            text = clean_text("".join(self.buffer))
            if text:
                self.messages.append(text)
            self.content_depth = 0
            self.buffer = []
        if self.author_depth == depth:
            self.author_depth = 0
        if self.stack:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self.content_depth:
            self.buffer.append(data)


def teams_samples(items_zip: Path) -> list[Sample]:
    samples: list[Sample] = []
    with zipfile.ZipFile(items_zip) as archive:
        for name in archive.namelist():
            if name.endswith("/") or ".html" not in name.lower():
                continue
            parser = TeamsParser()
            parser.feed(archive.read(name).decode("utf-8", errors="replace"))
            for index, text in enumerate(parser.messages):
                if len(WORDS_RE.findall(text)) >= 2:
                    samples.append(Sample("chat", text, f"teams:{name}:{index}"))
    return samples


def deduplicate_samples(samples: list[Sample]) -> list[Sample]:
    """Keep the first occurrence of channel-local, whitespace-normalized text."""
    seen: set[tuple[str, str]] = set()
    unique: list[Sample] = []
    for sample in samples:
        key = (sample.channel, " ".join(sample.text.lower().split()))
        if key in seen:
            continue
        seen.add(key)
        unique.append(sample)
    return unique


def percentile(values: list[int], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return float(ordered[round((len(ordered) - 1) * q)])


def profile(samples: list[Sample], channel: str) -> dict[str, object]:
    texts = [sample.text for sample in samples if sample.channel == channel]
    word_counts = [len(WORDS_RE.findall(text)) for text in texts]
    sentence_lengths = [len(WORDS_RE.findall(sentence)) for text in texts for sentence in SENTENCE_RE.split(text) if sentence.strip()]
    joined = "\n".join(texts)
    words = WORDS_RE.findall(joined)
    contractions = sum("'" in word or "’" in word for word in words)
    return {
        "samples": len(texts),
        "words": len(words),
        "words_per_sample_median": round(statistics.median(word_counts), 1) if word_counts else 0,
        "words_per_sample_p10": percentile(word_counts, 0.10),
        "words_per_sample_p90": percentile(word_counts, 0.90),
        "sentence_words_median": round(statistics.median(sentence_lengths), 1) if sentence_lengths else 0,
        "contractions_per_1000_words": round(1000 * contractions / max(1, len(words)), 1),
        "questions_per_100_samples": round(100 * joined.count("?") / max(1, len(texts)), 1),
        "exclamations_per_100_samples": round(100 * joined.count("!") / max(1, len(texts)), 1),
        "em_dashes_per_100_samples": round(100 * joined.count("—") / max(1, len(texts)), 1),
        "multiline_share": round(sum("\n" in text for text in texts) / max(1, len(texts)), 3),
    }


def draft_markdown(owner: str, metrics: dict[str, dict[str, object]], source_hashes: dict[str, str]) -> str:
    email_m, chat_m = metrics["email"], metrics["chat"]
    return f"""# Voice Profile Draft: {owner}

## Scope
- Owner: {owner}
- Channels: sent email and Microsoft Teams chat
- Derived from: {email_m['samples']} cleaned emails and {chat_m['samples']} cleaned authored chat messages
- Source fingerprints: Gmail `{source_hashes['gmail'][:16]}…`; Teams `{source_hashes['teams'][:16]}…`
- Last reviewed: pending owner review ({date.today().isoformat()})

## Voice
- Register: professional but conversational; preserve technical vocabulary rather than translating it into generic business language.
- Directness and warmth: lead with the point or requested action; add context only when it changes the decision.
- Cadence: email median {email_m['sentence_words_median']} words per sentence; chat is materially tighter and should not be expanded into email-shaped prose.
- Paragraph shape: short functional paragraphs; chat usually stays in one compact block.
- Openings and transitions: favor situational openings over ceremonial setup or universal claims.
- Closings and calls to action: make the requested decision, owner, or next step explicit; do not manufacture a closing when none is needed.

## Language
- Recurring terms and phrases: retain channel-appropriate contractions and ordinary technical shorthand.
- Technical or domain language: preserve exact product, program, compliance, and engineering terms.
- Humor and idiom: allow dry, contextual humor when the source supports it; never add performative slang.
- Punctuation and formatting: questions are common in chat ({chat_m['questions_per_100_samples']} per 100 samples); em dashes are occasional, not prohibited ({email_m['em_dashes_per_100_samples']} per 100 emails).

## Decision patterns
- Uncertainty: state what is known, what is suspected, and what would resolve it.
- Disagreement: name the operational problem or trade-off directly without padding it with generic diplomacy.
- Urgency: state the consequence and next action; avoid artificial intensity.
- Trade-offs: prefer a concrete recommendation with the important downside visible.

## Explicit preferences
- Preserve: direct recommendations, exact facts, useful technical language, real uncertainty, concise calls to action, and channel differences.
- Avoid: invented evidence, generic corporate filler, motivational endings, excessive symmetry, fake warmth, and rewriting clean short messages merely to satisfy a checklist.

## Confidence and gaps
- High-confidence observations: strong channel separation, concise chat cadence, direct operational framing, and technical-term preservation.
- Channel gaps: this corpus does not establish a long-form editorial, public social, or brand-marketing voice.
- Questions for review: Which recurring phrases should be explicit preferences? Are there audiences where a more formal register is mandatory?

## Quantitative guardrails (descriptive, not rigid)
- Email length: median {email_m['words_per_sample_median']} words; central 80% approximately {email_m['words_per_sample_p10']:.0f}–{email_m['words_per_sample_p90']:.0f} words.
- Chat length: median {chat_m['words_per_sample_median']} words; central 80% approximately {chat_m['words_per_sample_p10']:.0f}–{chat_m['words_per_sample_p90']:.0f} words.
- Contractions per 1,000 words: email {email_m['contractions_per_1000_words']}; chat {chat_m['contractions_per_1000_words']}.
"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gmail-zip", type=Path, required=True)
    parser.add_argument("--teams-zip", type=Path, required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--owner-email", action="append", default=[])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    for source in (args.gmail_zip, args.teams_zip):
        if not source.is_file():
            parser.error(f"source does not exist: {source}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    extracted = gmail_samples(args.gmail_zip, {value.lower() for value in args.owner_email}) + teams_samples(args.teams_zip)
    samples = deduplicate_samples(extracted)
    records = []
    for sample in samples:
        fingerprint = hashlib.sha256(sample.source_key.encode()).hexdigest()
        records.append({"channel": sample.channel, "split": "validation" if int(fingerprint[:2], 16) < 26 else "train", "text": sample.text, "source_hash": fingerprint})
    with (args.output_dir / "corpus.jsonl").open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    metrics = {channel: profile(samples, channel) for channel in ("email", "chat")}
    hashes = {"gmail": sha256(args.gmail_zip), "teams": sha256(args.teams_zip)}
    (args.output_dir / "metrics.json").write_text(json.dumps({"metrics": metrics, "source_sha256": hashes}, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "voice-profile-draft.md").write_text(draft_markdown(args.owner, metrics, hashes), encoding="utf-8")
    print(json.dumps({"output_dir": str(args.output_dir), "extracted_records": len(extracted), "duplicate_records_removed": len(extracted) - len(samples), "records": len(records), "metrics": metrics}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
