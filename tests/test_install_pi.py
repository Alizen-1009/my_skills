from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install-pi.py"
SPEC = importlib.util.spec_from_file_location("install_pi", SCRIPT_PATH)
assert SPEC and SPEC.loader
install_pi = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = install_pi
SPEC.loader.exec_module(install_pi)


class TargetSelectionTest(unittest.TestCase):
    def test_manages_pi_by_default_or_when_explicitly_requested(self) -> None:
        self.assertTrue(install_pi.should_manage_pi(None, None))
        self.assertTrue(install_pi.should_manage_pi("pi,codex", None))

    def test_skips_pi_for_other_agents_or_explicit_skill_destination(self) -> None:
        self.assertFalse(install_pi.should_manage_pi("codex", None))
        self.assertFalse(install_pi.should_manage_pi(None, "/tmp/skills"))


class PinnedVersionTest(unittest.TestCase):
    def test_reads_pi_version_from_package_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "pi-packages.json").write_text(
                json.dumps({"piVersion": "0.84.2", "packages": []}),
                encoding="utf-8",
            )
            with patch.object(install_pi, "repo_root", return_value=root):
                version = install_pi.load_pinned_version()

        self.assertEqual(version, "0.84.2")


class EnsurePiTest(unittest.TestCase):
    def test_keeps_matching_pi_without_invoking_npm(self) -> None:
        with (
            patch.object(install_pi.shutil, "which", return_value="/usr/local/bin/pi"),
            patch.object(install_pi, "get_pi_version", return_value="0.84.2"),
            patch.object(install_pi.subprocess, "run") as run,
            redirect_stdout(io.StringIO()),
        ):
            result = install_pi.ensure_pi("0.84.2", dry_run=False)

        self.assertEqual(result, 0)
        run.assert_not_called()

    def test_dry_run_reports_install_when_pi_is_missing(self) -> None:
        def which(name: str) -> str | None:
            return "/usr/local/bin/npm" if name == "npm" else None

        output = io.StringIO()
        with (
            patch.object(install_pi.shutil, "which", side_effect=which),
            patch.object(install_pi.subprocess, "run") as run,
            redirect_stdout(output),
        ):
            result = install_pi.ensure_pi("0.84.2", dry_run=True)

        self.assertEqual(result, 0)
        run.assert_not_called()
        self.assertIn("@earendil-works/pi-coding-agent@0.84.2", output.getvalue())

    def test_reconciles_a_different_pi_version_with_npm(self) -> None:
        def which(name: str) -> str | None:
            return f"/usr/local/bin/{name}" if name in {"pi", "npm"} else None

        with (
            patch.object(install_pi.shutil, "which", side_effect=which),
            patch.object(install_pi, "get_pi_version", side_effect=["0.80.0", "0.84.2"]),
            patch.object(install_pi.subprocess, "run") as run,
            redirect_stdout(io.StringIO()),
        ):
            result = install_pi.ensure_pi("0.84.2", dry_run=False)

        self.assertEqual(result, 0)
        run.assert_called_once_with(
            [
                "/usr/local/bin/npm",
                "install",
                "--global",
                "--ignore-scripts",
                "@earendil-works/pi-coding-agent@0.84.2",
            ],
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
