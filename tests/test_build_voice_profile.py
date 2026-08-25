from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_voice_profile", ROOT / "scripts/build_voice_profile.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load voice profile builder")
BUILDER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BUILDER
SPEC.loader.exec_module(BUILDER)


class VoiceProfileBuilderTests(unittest.TestCase):
    def test_clean_text_removes_quotes_and_redacts_identifiers(self) -> None:
        value = BUILDER.clean_text("Call me at 202-555-0100. See https://example.com\nOn Tuesday, Pat wrote:\nprivate quote")
        self.assertEqual(value, "Call me at [PHONE]. See [URL]")

    def test_teams_parser_keeps_only_author_messages(self) -> None:
        parser = BUILDER.TeamsParser()
        parser.feed("""<div class='message message--author'><div class='message__content'><p>My direct note.</p></div></div><div class='message message--responder'><div class='message__content'><p>Someone else.</p></div></div>""")
        self.assertEqual(parser.messages, ["My direct note."])

    def test_profile_is_aggregate_only(self) -> None:
        samples = [BUILDER.Sample("chat", "Can you check this?", "one"), BUILDER.Sample("chat", "Yep, on it.", "two")]
        result = BUILDER.profile(samples, "chat")
        self.assertEqual(result["samples"], 2)
        self.assertNotIn("text", result)

    def test_deduplicate_samples_is_channel_local(self) -> None:
        samples = [
            BUILDER.Sample("chat", "On it.", "one"),
            BUILDER.Sample("chat", " on   it. ", "two"),
            BUILDER.Sample("email", "On it.", "three"),
        ]
        self.assertEqual(len(BUILDER.deduplicate_samples(samples)), 2)


if __name__ == "__main__":
    unittest.main()
