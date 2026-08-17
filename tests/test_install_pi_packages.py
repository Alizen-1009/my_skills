from __future__ import annotations

import importlib.util
import io
import json
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install-pi-packages.py"
SPEC = importlib.util.spec_from_file_location("install_pi_packages", SCRIPT_PATH)
assert SPEC and SPEC.loader
install_pi_packages = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = install_pi_packages
SPEC.loader.exec_module(install_pi_packages)


class JsonMergePatchTest(unittest.TestCase):
    def test_merges_nested_settings_and_deletes_null_keys(self) -> None:
        current = {
            "packages": ["npm:example@1.0.0"],
            "enabledModels": ["stale/*"],
            "compaction": {"enabled": True, "reserveTokens": 16_384},
        }
        patch = {
            "enabledModels": None,
            "compaction": {"reserveTokens": 54_400},
        }

        merged = install_pi_packages.merge_json_patch(current, patch)

        self.assertEqual(merged["packages"], ["npm:example@1.0.0"])
        self.assertNotIn("enabledModels", merged)
        self.assertEqual(
            merged["compaction"],
            {"enabled": True, "reserveTokens": 54_400},
        )


class SyncConfigTreeTest(unittest.TestCase):
    def test_copies_managed_config_to_matching_pi_home_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_root = root / "pi-config"
            source = config_root / "extensions/pi-continue.json"
            source.parent.mkdir(parents=True)
            source.write_text('{"enabled": true}\n', encoding="utf-8")
            home = root / "agent"

            with redirect_stdout(io.StringIO()):
                install_pi_packages.sync_config_tree(config_root, home, dry_run=False)

            self.assertEqual(
                (home / "extensions/pi-continue.json").read_text(encoding="utf-8"),
                source.read_text(encoding="utf-8"),
            )

    def test_merges_settings_patch_without_copying_patch_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_root = root / "pi-config"
            config_root.mkdir()
            (config_root / "settings.patch.json").write_text(
                json.dumps(
                    {
                        "enabledModels": None,
                        "compaction": {"reserveTokens": 54_400},
                    }
                ),
                encoding="utf-8",
            )
            home = root / "agent"
            home.mkdir()
            (home / "settings.json").write_text(
                json.dumps(
                    {
                        "packages": ["npm:example@1.0.0"],
                        "enabledModels": ["stale/*"],
                        "compaction": {"enabled": True, "reserveTokens": 16_384},
                    }
                ),
                encoding="utf-8",
            )

            with redirect_stdout(io.StringIO()):
                install_pi_packages.sync_config_tree(config_root, home, dry_run=False)

            installed = json.loads((home / "settings.json").read_text(encoding="utf-8"))
            self.assertEqual(installed["packages"], ["npm:example@1.0.0"])
            self.assertNotIn("enabledModels", installed)
            self.assertEqual(installed["compaction"]["enabled"], True)
            self.assertEqual(installed["compaction"]["reserveTokens"], 54_400)
            self.assertFalse((home / "settings.patch.json").exists())

    def test_preserves_existing_settings_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_root = root / "pi-config"
            config_root.mkdir()
            (config_root / "settings.patch.json").write_text(
                json.dumps({"theme": "dark"}),
                encoding="utf-8",
            )
            settings = root / "agent/settings.json"
            settings.parent.mkdir()
            settings.write_text(json.dumps({"theme": "light"}), encoding="utf-8")
            settings.chmod(0o600)

            with redirect_stdout(io.StringIO()):
                install_pi_packages.sync_config_tree(
                    config_root,
                    root / "agent",
                    dry_run=False,
                )

            self.assertEqual(stat.S_IMODE(settings.stat().st_mode), 0o600)

    def test_rejects_protected_keys_in_settings_patch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_root = root / "pi-config"
            config_root.mkdir()
            (config_root / "settings.patch.json").write_text(
                json.dumps({"packages": ["npm:replacement@1.0.0"]}),
                encoding="utf-8",
            )
            settings = root / "agent/settings.json"
            settings.parent.mkdir()
            settings.write_text(
                json.dumps({"packages": ["npm:local@1.0.0"]}),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "protected Pi setting"):
                install_pi_packages.sync_config_tree(
                    config_root,
                    root / "agent",
                    dry_run=False,
                )

            self.assertEqual(
                json.loads(settings.read_text(encoding="utf-8"))["packages"],
                ["npm:local@1.0.0"],
            )

    def test_refuses_to_sync_credentials_or_runtime_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_root = root / "pi-config"
            config_root.mkdir()
            (config_root / "auth.json").write_text("{}\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Refusing to sync unmanaged Pi state"):
                install_pi_packages.sync_config_tree(
                    config_root,
                    root / "agent",
                    dry_run=False,
                )

            self.assertFalse((root / "agent" / "auth.json").exists())

    def test_refuses_every_config_path_outside_the_allowlist(self) -> None:
        unmanaged_paths = (
            "cache/index.json",
            "cookies.json",
            "models.json",
            "sessions/example.json",
            "trust.json",
        )
        for unmanaged_path in unmanaged_paths:
            with self.subTest(unmanaged_path=unmanaged_path):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    config_root = root / "pi-config"
                    source = config_root / unmanaged_path
                    source.parent.mkdir(parents=True)
                    source.write_text("{}\n", encoding="utf-8")

                    with self.assertRaisesRegex(
                        ValueError,
                        "Refusing to sync unmanaged Pi state",
                    ):
                        install_pi_packages.sync_config_tree(
                            config_root,
                            root / "agent",
                            dry_run=False,
                        )

    def test_dry_run_reports_change_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_root = root / "pi-config"
            source = config_root / "extensions/pi-continue.json"
            source.parent.mkdir(parents=True)
            source.write_text('{"enabled": true}\n', encoding="utf-8")
            home = root / "agent"
            output = io.StringIO()

            with redirect_stdout(output):
                install_pi_packages.sync_config_tree(config_root, home, dry_run=True)

            self.assertFalse((home / "extensions/pi-continue.json").exists())
            self.assertIn("[DRY]", output.getvalue())

    def test_reports_matching_config_without_rewriting_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_root = root / "pi-config"
            source = config_root / "extensions/pi-continue.json"
            source.parent.mkdir(parents=True)
            source.write_text('{"enabled": true}\n', encoding="utf-8")
            destination = root / "agent/extensions/pi-continue.json"
            destination.parent.mkdir(parents=True)
            destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            original_mtime = destination.stat().st_mtime_ns
            output = io.StringIO()

            with redirect_stdout(output):
                install_pi_packages.sync_config_tree(config_root, root / "agent", dry_run=False)

            self.assertEqual(destination.stat().st_mtime_ns, original_mtime)
            self.assertIn("[OK]", output.getvalue())


class MainDryRunTest(unittest.TestCase):
    def test_previews_packages_and_config_without_pi_or_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "pi-packages.json").write_text(
                json.dumps(
                    {
                        "packages": [
                            {
                                "id": "example",
                                "source": "npm:example@1.0.0",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            config_root = root / "pi-config"
            config_root.mkdir()
            (config_root / "settings.patch.json").write_text(
                json.dumps({"theme": "dark"}),
                encoding="utf-8",
            )
            output = io.StringIO()

            with (
                patch.object(install_pi_packages, "repo_root", return_value=root),
                patch.object(install_pi_packages, "pi_home", return_value=root / "agent"),
                patch.object(install_pi_packages.shutil, "which", return_value=None),
                patch.object(
                    install_pi_packages.sys,
                    "argv",
                    [str(SCRIPT_PATH), "--dry-run"],
                ),
                redirect_stdout(output),
            ):
                result = install_pi_packages.main()

            self.assertEqual(result, 0)
            self.assertIn("[DRY] pi install npm:example@1.0.0", output.getvalue())
            self.assertIn("[DRY] merge Pi config", output.getvalue())
            self.assertFalse((root / "agent").exists())


class PackageMaterializationTest(unittest.TestCase):
    def test_verifies_pinned_npm_package_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            package_dir = home / "npm/node_modules/@scope/example"
            package_dir.mkdir(parents=True)
            package_json = package_dir / "package.json"
            package_json.write_text(
                json.dumps({"name": "@scope/example", "version": "1.2.3"}),
                encoding="utf-8",
            )

            self.assertTrue(
                install_pi_packages.package_is_current(
                    "npm:@scope/example@1.2.3",
                    home,
                )
            )
            self.assertFalse(
                install_pi_packages.package_is_current(
                    "npm:@scope/example@1.2.4",
                    home,
                )
            )
            package_json.unlink()
            self.assertFalse(
                install_pi_packages.package_is_current(
                    "npm:@scope/example@1.2.3",
                    home,
                )
            )

    def test_verifies_pinned_git_checkout_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            checkout = home / "git/github.com/example/project"
            checkout.mkdir(parents=True)
            subprocess.run(["git", "init", "--quiet", str(checkout)], check=True)
            (checkout / "README.md").write_text("test\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(checkout), "add", "README.md"], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(checkout),
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.com",
                    "commit",
                    "--quiet",
                    "-m",
                    "test",
                ],
                check=True,
            )
            commit = subprocess.run(
                ["git", "-C", str(checkout), "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()

            self.assertTrue(
                install_pi_packages.package_is_current(
                    f"https://github.com/example/project@{commit}",
                    home,
                )
            )
            self.assertFalse(
                install_pi_packages.package_is_current(
                    "https://github.com/example/project@0000000000000000000000000000000000000000",
                    home,
                )
            )


class ResolveSourceTest(unittest.TestCase):
    def test_resolves_repo_relative_local_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with patch.object(install_pi_packages, "repo_root", return_value=root):
                source = install_pi_packages.resolve_source("./pi-packages/example")

        self.assertEqual(source, str((root / "pi-packages/example").resolve()))

    def test_leaves_registry_source_unchanged(self) -> None:
        source = "npm:pi-web-access@0.23.0"
        self.assertEqual(install_pi_packages.resolve_source(source), source)

    def test_installed_sources_normalizes_local_path_relative_to_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            settings_path = root / ".pi/settings.json"
            settings_path.parent.mkdir()
            settings_path.write_text(
                json.dumps({"packages": ["../../repo/proactive-compaction"]}),
                encoding="utf-8",
            )

            sources = install_pi_packages.installed_sources(settings_path)

        expected = str((settings_path.parent / "../../repo/proactive-compaction").resolve())
        self.assertEqual(sources, {expected})


if __name__ == "__main__":
    unittest.main()
