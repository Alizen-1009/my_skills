from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install-skills.py"
SPEC = importlib.util.spec_from_file_location("install_skills", SCRIPT_PATH)
assert SPEC and SPEC.loader
install_skills = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = install_skills
SPEC.loader.exec_module(install_skills)


class CuratedSkillSetTest(unittest.TestCase):
    def test_redundant_skills_are_excluded_from_default_install(self) -> None:
        skills, warnings = install_skills.discover_all(SCRIPT_PATH.parents[1])
        names = {skill.name for skill in skills}
        excluded = {
            "ask-matt",
            "benchmark-paper-template",
            "claude-handoff",
            "deep-research",
            "git-guardrails-claude-code",
            "grill-me",
            "idea-evaluator",
            "implement",
            "intro-drafter",
            "improve-codebase-architecture",
            "loop-me",
            "migrate-to-shoehorn",
            "paper-polish",
            "paper-writer",
            "pre-submission-reviewer",
            "scaffold-exercises",
            "setup-matt-pocock-skills",
            "setup-ts-deep-modules",
            "skill-creator",
            "tdd",
            "tech-paper-template",
            "teach",
            "to-questionnaire",
            "to-spec",
            "to-tickets",
            "triage",
            "using-agent-skills",
            "vibe-research-workflow",
            "wait-what",
        }

        self.assertEqual(warnings, [])
        self.assertTrue(excluded.isdisjoint(names))
        self.assertTrue({"drawio-reconstruction", "figure-designer"}.issubset(names))
        self.assertEqual(len(skills), 62)

    def test_generated_catalog_matches_discovered_skills(self) -> None:
        root = SCRIPT_PATH.parents[1]
        skills, warnings = install_skills.discover_all(root)

        self.assertEqual(warnings, [])
        self.assertEqual(
            (root / "SKILLS.md").read_text(encoding="utf-8"),
            install_skills.render_skill_catalog(skills),
        )


class DescriptionParsingTest(unittest.TestCase):
    def test_preserves_unquoted_description_ending_in_a_quote(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "quoted"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                '---\nname: quoted\ndescription: Example like "do this."\n---\n',
                encoding="utf-8",
            )
            skill = install_skills.Skill("quoted", skill_dir, "local")

            self.assertEqual(
                install_skills.read_description(skill),
                'Example like "do this."',
            )

    def test_folds_multiline_yaml_description(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "multiline"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: multiline\n"
                "description: >-\n"
                "  Designs research figures and audits their quality.\n"
                "  Use when a paper figure needs improvement.\n"
                "license: CC-BY-4.0\n"
                "---\n",
                encoding="utf-8",
            )
            skill = install_skills.Skill("multiline", skill_dir, "upstream")

            self.assertEqual(
                install_skills.read_description(skill),
                "Designs research figures and audits their quality. "
                "Use when a paper figure needs improvement.",
            )


class MissingSourceSafetyTest(unittest.TestCase):
    def test_incomplete_sources_do_not_trigger_partial_install_or_pruning(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            local_skill = root / "skills/keep"
            local_skill.mkdir(parents=True)
            (local_skill / "SKILL.md").write_text(
                "---\nname: keep\ndescription: Keep this skill.\n---\n",
                encoding="utf-8",
            )
            (root / "skill-sources.json").write_text(
                """{
  "sources": [
    {"id": "local", "kind": "local", "path": "skills"},
    {
      "id": "missing",
      "kind": "git-submodule",
      "path": "external/missing",
      "skills_path": "skills"
    }
  ]
}
""",
                encoding="utf-8",
            )
            stale_source = root / "external/missing/skills/old"
            stale_source.parent.mkdir(parents=True)
            destination = Path(temp_dir) / "installed"
            destination.mkdir()
            stale = destination / "old"
            stale.symlink_to(stale_source, target_is_directory=True)

            with (
                patch.object(install_skills, "repo_root", return_value=root),
                patch.object(
                    install_skills.sys,
                    "argv",
                    [str(SCRIPT_PATH), "--dest", str(destination)],
                ),
                redirect_stderr(io.StringIO()),
            ):
                result = install_skills.main()

            self.assertEqual(result, 1)
            self.assertTrue(stale.is_symlink())

    def test_invalid_enabled_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "skill-sources.json").write_text(
                '{"sources": [{"id": "bad", "kind": "unknown", "path": "skills"}]}',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "unknown kind"):
                install_skills.load_sources(root)


class PruneManagedLinksTest(unittest.TestCase):
    def test_removes_only_stale_links_managed_by_this_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            desired_source = root / "skills/keep"
            stale_source = root / "external/source/skills/remove"
            external_source = Path(temp_dir) / "other/keep-external"
            for source in (desired_source, stale_source, external_source):
                source.mkdir(parents=True)

            destination = Path(temp_dir) / "installed"
            destination.mkdir()
            (destination / "keep").symlink_to(desired_source, target_is_directory=True)
            (destination / "remove").symlink_to(stale_source, target_is_directory=True)
            (destination / "keep-external").symlink_to(
                external_source,
                target_is_directory=True,
            )
            unrelated_alias = destination / "manual-alias"
            unrelated_alias.symlink_to(desired_source, target_is_directory=True)
            prunable = {"remove": frozenset({stale_source.resolve()})}

            messages = install_skills.prune_stale_managed_links(
                destination,
                prunable,
                dry_run=False,
            )

            self.assertTrue((destination / "keep").is_symlink())
            self.assertFalse((destination / "remove").exists())
            self.assertFalse((destination / "remove").is_symlink())
            self.assertTrue((destination / "keep-external").is_symlink())
            self.assertTrue(unrelated_alias.is_symlink())
            self.assertEqual(messages, ["[PRUNE] remove"])

    def test_full_dry_run_previews_pruning_without_a_conflicting_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            for name in ("keep", "remove"):
                skill_dir = root / "skills" / name
                skill_dir.mkdir(parents=True)
                (skill_dir / "SKILL.md").write_text(
                    f"---\nname: {name}\ndescription: Test skill.\n---\n",
                    encoding="utf-8",
                )
            (root / "skill-sources.json").write_text(
                """{
  "sources": [
    {
      "id": "local",
      "kind": "local",
      "path": "skills",
      "exclude": ["remove"]
    }
  ]
}
""",
                encoding="utf-8",
            )
            destination = Path(temp_dir) / "installed"
            destination.mkdir()
            stale = destination / "remove"
            stale.symlink_to(root / "skills/remove", target_is_directory=True)
            output = io.StringIO()

            with (
                patch.object(install_skills, "repo_root", return_value=root),
                patch.object(
                    install_skills.sys,
                    "argv",
                    [
                        str(SCRIPT_PATH),
                        "--dest",
                        str(destination),
                        "--dry-run",
                    ],
                ),
                redirect_stdout(output),
            ):
                result = install_skills.main()

            self.assertEqual(result, 0)
            self.assertTrue(stale.is_symlink())
            self.assertIn("[DRY] prune remove", output.getvalue())
            self.assertNotIn("[SKIP] remove", output.getvalue())

    def test_dry_run_does_not_remove_stale_link(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            source = root / "skills/remove"
            source.mkdir(parents=True)
            destination = Path(temp_dir) / "installed"
            destination.mkdir()
            stale = destination / "remove"
            stale.symlink_to(source, target_is_directory=True)

            messages = install_skills.prune_stale_managed_links(
                destination,
                {"remove": frozenset({source.resolve()})},
                dry_run=True,
            )

            self.assertTrue(stale.is_symlink())
            self.assertEqual(messages, ["[DRY] prune remove"])


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
