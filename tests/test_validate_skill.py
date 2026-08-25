from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_skill", ROOT / "scripts/validate_skill.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateSkillTests(unittest.TestCase):
    def make_copy(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        destination = Path(temporary.name) / "skill"
        shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return temporary, destination

    def test_repository_is_valid(self) -> None:
        self.assertEqual(VALIDATOR.validate(ROOT), [])

    def test_missing_fixture_fails(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        (root / "evals/files/customer-email.md").unlink()
        errors = VALIDATOR.validate(root)
        self.assertTrue(any("references missing file" in error for error in errors))

    def test_duplicate_eval_id_fails(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        path = root / "evals/evals.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["evals"][1]["id"] = data["evals"][0]["id"]
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = VALIDATOR.validate(root)
        self.assertTrue(any("unique integer id" in error for error in errors))

    def test_private_mail_archive_fails(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        (root / "sample.mbox").write_text("private", encoding="utf-8")
        errors = VALIDATOR.validate(root)
        self.assertTrue(any("private mail archive" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
