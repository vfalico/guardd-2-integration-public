#!/usr/bin/env python3
"""Exercise source verification against real temporary Git histories."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class SourceVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.guide = self.root / "guide"
        (self.guide / "tools").mkdir(parents=True)
        shutil.copyfile(Path(__file__).with_name("verify-source.py"),
                        self.guide / "tools/verify-source.py")
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_")}
        self.env.update({
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_AUTHOR_NAME": "Fixture Contributor",
            "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Fixture Contributor",
            "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            "GIT_TERMINAL_PROMPT": "0",
        })
        self.manifest = {"projects": {}, "followupPublication": {"projects": {}}}
        self.signed = "\n\nSigned-off-by: Fixture Contributor <fixture@example.invalid>\n"
        for name in ("orka", "kaimahi", "guardd"):
            repository = self.root / name
            repository.mkdir()
            self.git(name, "init", "--quiet", "--initial-branch=main")
            (repository / "baseline").write_text("baseline\n")
            self.git(name, "add", ".")
            self.git(name, "commit", "--quiet", "-m", "Baseline" + self.signed)
            baseline = self.git(name, "rev-parse", "HEAD")
            (repository / "feature").write_text("owned feature\n")
            self.git(name, "add", ".")
            self.git(name, "commit", "--quiet", "-m", "Feature" + self.signed)
            original = self.git(name, "rev-parse", "HEAD")
            project = {
                "baseline": baseline, "tip": original,
                "tree": self.git(name, "rev-parse", "HEAD^{tree}"),
                "series": [{"commit": original}],
            }
            if name == "guardd":
                project["baselinePrerequisites"] = [{"commit": baseline}]
            self.manifest["projects"][name] = project
            if name == "guardd":
                continue
            self.git(name, "checkout", "--quiet", "--detach", baseline)
            (repository / "upstream").write_text("upstream addition\n")
            self.git(name, "add", ".")
            self.git(name, "commit", "--quiet", "-m", "Upstream without owner-series DCO")
            upstream = self.git(name, "rev-parse", "HEAD")
            self.git(name, "checkout", "--quiet", "--detach", original)
            self.git(name, "merge", "--quiet", "--no-ff", upstream,
                     "-m", "Merge upstream" + self.signed)
            merged = self.git(name, "rev-parse", "HEAD")
            self.manifest["followupPublication"]["projects"][name] = {
                "tip": merged, "tree": self.git(name, "rev-parse", "HEAD^{tree}"),
                "integratedMains": [upstream], "additionalSeries": [{"commit": merged}],
            }

    def git(self, name, *args, input=None):
        return subprocess.check_output(
            ["git", "-C", str(self.root / name), *args], env=self.env,
            input=input, text=True, stderr=subprocess.PIPE,
        ).strip()

    def verify(self, manifest=None, followup=True):
        path = self.guide / "release-manifest.json"
        data = json.dumps(self.manifest if manifest is None else manifest).encode()
        path.write_bytes(data)
        command = [sys.executable, str(self.guide / "tools/verify-source.py"),
                   "--root", str(self.root)]
        if followup:
            command.append("--followup")
        result = subprocess.run(command, env=self.env, text=True, capture_output=True)
        self.assertEqual(path.read_bytes(), data)
        return result

    def test_original_and_followup_select_exact_sources(self):
        result = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotEqual(self.verify(followup=False).returncode, 0)
        for name in ("orka", "kaimahi"):
            self.git(name, "checkout", "--quiet", "--detach",
                     self.manifest["projects"][name]["tip"])
        result = self.verify(followup=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotEqual(self.verify().returncode, 0)

    def test_refuses_wrong_pins_series_and_ancestry(self):
        update = self.manifest["followupPublication"]["projects"]["orka"]
        unrelated = self.git("orka", "commit-tree", update["tree"],
                             input="Unrelated history" + self.signed)
        for field, value in (
            ("tip", self.manifest["projects"]["orka"]["tip"]),
            ("tree", self.git("orka", "rev-parse", "HEAD~1^{tree}")),
            ("integratedMains", [unrelated]),
            ("additionalSeries", []),
        ):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest["followupPublication"]["projects"]["orka"][field] = value
                self.assertNotEqual(self.verify(manifest).returncode, 0)

    def test_owner_metadata_policy_is_not_applied_to_excluded_upstream(self):
        result = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        update = self.manifest["followupPublication"]["projects"]["orka"]
        parent = update["tip"]
        for suffix, accepted in (
            (self.signed, True),
            ("", False),
            (self.signed + "\nCopilot-Session: fixture\n", False),
        ):
            with self.subTest(suffix=suffix):
                commit = self.git("orka", "commit-tree", update["tree"], "-p", parent,
                                  input="Additional owner change" + suffix)
                self.git("orka", "checkout", "--quiet", "--detach", commit)
                manifest = copy.deepcopy(self.manifest)
                proposed = manifest["followupPublication"]["projects"]["orka"]
                proposed["tip"] = commit
                proposed["additionalSeries"].append({"commit": commit})
                result = self.verify(manifest)
                if accepted:
                    self.assertEqual(result.returncode, 0, result.stderr)
                else:
                    self.assertNotEqual(result.returncode, 0)

    def test_followup_cannot_override_guardd_or_omit_a_project(self):
        for name in ("guardd", "kaimahi"):
            with self.subTest(name=name):
                manifest = copy.deepcopy(self.manifest)
                updates = manifest["followupPublication"]["projects"]
                if name == "guardd":
                    updates[name] = self.manifest["projects"][name]
                else:
                    del updates[name]
                self.assertNotEqual(self.verify(manifest).returncode, 0)


if __name__ == "__main__":
    unittest.main()
