#!/usr/bin/env python3
"""Verify pinned tracked sources and ordered review series without running tests."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True,
                        help="directory containing orka/, kaimahi/ and guardd/")
    parser.add_argument("--followup", action="store_true",
                        help="verify the follow-up review pins instead of the original publication")
    options = parser.parse_args()
    manifest = json.loads((Path(__file__).resolve().parents[1] / "release-manifest.json").read_bytes())
    projects = manifest["projects"]
    updates = {}
    if options.followup:
        updates = manifest["followupPublication"]["projects"]
        if set(updates) != {"orka", "kaimahi"}:
            raise SystemExit("follow-up must override exactly Orka and Kaimahi")
        projects = dict(projects)
        for name, update in updates.items():
            projects[name] = {
                **projects[name], **update,
                "series": projects[name]["series"] + update["additionalSeries"],
            }
    for name, expected in projects.items():
        repository = options.root / name

        def git(*args):
            return subprocess.check_output(["git", "-C", str(repository), *args], text=True).strip()

        if git("status", "--porcelain"):
            raise SystemExit(f"{name}: working tree has changes")
        if git("rev-parse", "HEAD") != expected["tip"]:
            raise SystemExit(f"{name}: HEAD differs from the pinned review tip")
        if git("rev-parse", "HEAD^{tree}") != expected["tree"]:
            raise SystemExit(f"{name}: tracked tree differs")
        subprocess.run(["git", "-C", str(repository), "merge-base", "--is-ancestor",
                        expected["baseline"], "HEAD"], check=True)
        if name in updates:
            for main in expected["integratedMains"]:
                subprocess.run(["git", "-C", str(repository), "merge-base", "--is-ancestor",
                                main, "HEAD"], check=True)
            actual = git("rev-list", "--topo-order", "--reverse",
                         expected["baseline"] + "..HEAD",
                         "--not", *expected["integratedMains"]).splitlines()
        else:
            actual = git("rev-list", "--reverse", expected["baseline"] + "..HEAD").splitlines()
        if actual != [entry["commit"] for entry in expected["series"]]:
            raise SystemExit(f"{name}: ordered review series differs")
        commits = [entry["commit"] for entry in expected.get("baselinePrerequisites", [])] + actual
        for commit in commits:
            message = git("show", "-s", "--format=%B", commit)
            if any(line.startswith(("Dependencies:", "Validation:", "Limits:"))
                   for line in message.splitlines()):
                raise SystemExit(f"{name}: {commit} contains repeated message scaffolding")
            author = git("show", "-s", "--format=%an <%ae>", commit)
            committer = git("show", "-s", "--format=%cn <%ce>", commit)
            signoffs = git("show", "-s", "--format=%(trailers:key=Signed-off-by,valueonly)", commit).splitlines()
            assistant_trailers = git(
                "show", "-s", "--format=%(trailers:key=Copilot-Session)", commit)
            coauthors = git(
                "show", "-s", "--format=%(trailers:key=Co-authored-by,valueonly)", commit)
            if author not in signoffs:
                raise SystemExit(f"{name}: {commit} lacks its author's DCO sign-off")
            if (assistant_trailers or "copilot" in coauthors.lower()
                    or "copilot" in (author + committer + "\n".join(signoffs)).lower()):
                raise SystemExit(f"{name}: {commit} contains assistant attribution")
        print(f"{name}: exact tracked tree, {len(actual)} ordered commits and DCO policy verified")
    print("Source identity only; no binary, image, test or live-enforcement claim.")


if __name__ == "__main__":
    main()
