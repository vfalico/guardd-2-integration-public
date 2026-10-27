# Patch commit policy

This integration's source-series commits and exported mail patches must carry
a proper `Signed-off-by:` trailer from the responsible contributor, matching
the commit author. Signing certifies the [Developer Certificate of Origin
1.1](https://developercertificate.org/); do not sign on another contributor's
behalf without their explicit authorization.

Do not add `Co-authored-by: Copilot` or `Copilot-Session:` trailers, use an
assistant as the author/committer/signatory, or include assistant session
identifiers in patch metadata. Preserve legitimate human attribution and
upstream history outside this review series.

Keep each message specific to the change and its rationale. Do not append
repeated `Dependencies:`, `Validation:` or `Limits:` scaffold blocks. Put
series-wide dependencies and qualification details in the review map and
qualification document; retain necessary technical explanation in the body.

The source verifier enforces this policy for all 26 series commits and the
two explicitly listed Guardd baseline prerequisites:

```sh
python3 tools/verify-source.py --root /path/to/source-parent
```

Use the same policy for changes to this guide. Configure normal Git identity
locally and use `git commit -s`; do not put private keys, tokens or machine
state in commits. A DCO sign-off is a contributor certification, not a
cryptographic signature or a claim that tests ran.

## Metadata-only replacement

The initial publication was replaced at the owner's request to correct author,
committer and DCO metadata and remove assistant trailers. Source files,
every intermediate source tree and every binary patch payload are unchanged.
[`commit-rewrite-map.json`](commit-rewrite-map.json) preserves that first
replacement. The subsequent
[`commit-message-cleanup-map.json`](commit-message-cleanup-map.json) maps those
published identities to the current commits after removing repeated message
scaffolding. Both replacements preserve source trees and binary patch payloads.

The manifest keeps the original qualified source identities as provenance
alongside the current published tips. Existing real E2E results are reused
because the source/payload identity was checked, not relabeled as new tests.
Git-derived build metadata and a Git-archive envelope can still differ.
