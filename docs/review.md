# Review map

## Fetch pinned source, without touching upstream

Run these commands in a new directory. Only owner-controlled public
repositories are cloned; no command publishes anything or opens a PR.

```sh
git clone --branch guardd-2 https://github.com/vfalico/orka-public.git orka
git clone --branch guardd-2 https://github.com/vfalico/kaimahi-public.git kaimahi
git clone --branch guardd-2 https://github.com/vfalico/agentsuite-guardd-public.git guardd

git -C orka switch --detach e53dd073cb11b36263f4ad09e26623eb213cc2f8
git -C kaimahi switch --detach aa106fd382de9fee2fee7397ad6044250c02a152
git -C guardd switch --detach 2a4354af5ecf18198275f0501154c9d578a23ba4
```

Put this guide alongside those directories, then run:

```sh
python3 guardd-2-integration-public/tools/verify-source.py --root .
```

The verifier checks tracked cleanliness, exact tip/tree, ancestry, every
ordered series commit and the [commit policy](../CONTRIBUTING.md). It does not
run tests, inspect ignored build outputs, verify a binary or establish live
enforcement.

Preserve canonical Go module paths. A fork URL is a source/review location,
not a reason to rewrite imports. Do not push to an upstream repository or open
an upstream PR merely because these commits are structured for review.

## Start with independent fixes

| Orka commit | Purpose | Applicability |
| --- | --- | --- |
| `3b664ab0f289587be0562b6e70901dd000f299de` | Fall back when Responses rejects tool use before any output. | Ordinary compatibility fix; no Guardd or enforcement provider required. |
| `ec5a41e8bbed368fb7d838bbbbb0570cd39e788d` | Retire an exact cancelled standalone reservation without waiting for a nonexistent session acknowledgement. | Ordinary lifecycle fix; independent of the first fix and of Guardd. |

Inspect each with `git -C orka show <commit>`. For a standalone trial, use a
separate review copy at Orka baseline
`2026da6ad6e890070de4b28309d478319bc28cb7` and cherry-pick just the selected
fix. The fallback is narrow: it is not permission to replay arbitrary failures
or responses that have already produced output.

## Then review the feature series

The exact ordered commit IDs and subjects are in `release-manifest.json`.

| Slice | Review responsibility and dependencies |
| --- | --- |
| Orka 03 | Generated release-schema synchronization from APIs already present in its baseline; not a new enforcement capability or independent runtime bug. |
| Guardd 01-03 | Held physical identity, bounded filesystem snapshots and one combined filesystem/IPv4 native object. |
| Orka 04 + Guardd 04 | Opaque whole-requirement contract and authenticated provider client/server wire agreement. |
| Guardd 05-07 | Exact node/container resolution; durable mTLS lifecycle; optional retained-ownership installation. |
| Orka 05-08 | Native worker admission wait; ACP prepare-before-launch; publication/retirement intent; shared physical runtime lifecycle. |
| Orka 09 | Atomic activation of complete native/ACP admission, dispatch and cleanup. The larger controller slice deliberately keeps the trust boundary together. |
| Orka 10-12 | Actual optional chart composition, safe UI input/observations, examples and limitations. |
| Kaimahi 01-03 | Typed observations, verified installer/result foundations, candidate-bound evaluation and digest Deploy. |
| Kaimahi 04-07 | Immutable native Run/Chat forwarding, guided setup/namespace placement, complete public flags and documentation. |

Apply commits in order within a project. Only the two ordinary Orka fixes
above are advertised as independently applicable. Prefixes are review/build
units, not separately qualified deployment releases. Earlier Orka feature
prefixes preserve a protected request but refuse dispatch until the complete
controller integration arrives; they do not temporarily run it unprotected.

Guardd's baseline is
`75fead512389cdbe37d766c875089ce8fd485505`. Its history retains:

1. `4bc4d1e`: whole-requirement reference PoC.
2. `75fead5`: held-native filesystem deny-write exposure.

Those prerequisites follow the preserved source repository's public
`499462908370d8f62543b8e93fa35f6fb93cb4ae`. They are visible baseline history,
not seven additional independent fixes or an invisible dependency.

## Export mail patches or inspect deltas

Use the manifest's baseline for each project:

```sh
mkdir orka-patches
git -C orka format-patch --output-directory ../orka-patches \
  2026da6ad6e890070de4b28309d478319bc28cb7..e53dd073cb11b36263f4ad09e26623eb213cc2f8
git -C orka diff --stat \
  2026da6ad6e890070de4b28309d478319bc28cb7..e53dd073cb11b36263f4ad09e26623eb213cc2f8
```

Repeat with the corresponding Guardd/Kaimahi baseline and tip. `git am` onto
that exact baseline reproduces the recorded tree; author/committer metadata
can give a different commit ID. Generated schemas, protobuf files and chart
outputs belong with their source-owning changes.

## Historical exactness versus this integration

The earlier decomposition reproduced its frozen large-patch final sources
exactly, including comments, modes, symlinks and unchanged files. This
publication subsequently integrated fresh mains and ran new E2E. It does not
claim that the newer whole Orka/Kaimahi trees equal the older frozen trees.
Additive conflict resolutions preserve fresh upstream functionality; the
manifest identifies the actual newly built and exercised sources.

Review feedback, RFCs and future upstream submission are separate decisions.
This publication itself creates no upstream branch, issue or pull request.
