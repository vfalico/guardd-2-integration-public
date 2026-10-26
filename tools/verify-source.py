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
    options = parser.parse_args()
    manifest = json.loads((Path(__file__).resolve().parents[1] / "release-manifest.json").read_bytes())
    for name, expected in manifest["projects"].items():
        repository = options.root / name

        def git(*args):
            return subprocess.check_output(["git", "-C", str(repository), *args], text=True).strip()

        if git("status", "--porcelain"):
            raise SystemExit(f"{name}: working tree has changes")
        if git("rev-parse", "HEAD") != expected["tip"]:
            raise SystemExit(f"{name}: HEAD differs from the tested tip")
        if git("rev-parse", "HEAD^{tree}") != expected["tree"]:
            raise SystemExit(f"{name}: tracked tree differs")
        subprocess.run(["git", "-C", str(repository), "merge-base", "--is-ancestor",
                        expected["baseline"], "HEAD"], check=True)
        actual = git("rev-list", "--reverse", expected["baseline"] + "..HEAD").splitlines()
        if actual != [entry["commit"] for entry in expected["series"]]:
            raise SystemExit(f"{name}: ordered review series differs")
        commits = [entry["commit"] for entry in expected.get("baselinePrerequisites", [])] + actual
        for commit in commits:
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
