from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install-skills.py"
SPEC = importlib.util.spec_from_file_location("install_skills", SCRIPT_PATH)
assert SPEC and SPEC.loader
install_skills = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = install_skills
SPEC.loader.exec_module(install_skills)


class DetectTargetsTest(unittest.TestCase):
    def test_defaults_to_pi_when_no_agent_is_requested(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            targets = [
                install_skills.Target("codex", root / "codex", root / "codex/skills", ""),
                install_skills.Target("pi", root / "pi", root / "pi/skills", ""),
                install_skills.Target("claude", root / "claude", root / "claude/skills", ""),
            ]
            for target in targets:
                target.home.mkdir()

            with patch.object(install_skills, "known_targets", return_value=targets):
                selected, unknown = install_skills.detect_targets(None)

        self.assertEqual([target.id for target in selected], ["pi"])
        self.assertEqual(unknown, [])


if __name__ == "__main__":
    unittest.main()
