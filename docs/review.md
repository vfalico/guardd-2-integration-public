# Review map

## Upstream review

The submitted review entry points are:

- [orka-agents/orka#952](https://github.com/orka-agents/orka/pull/952):
  native and managed ACP Task admission and enforcement integration.
- [kaimahi-agents/kaimahi#781](https://github.com/kaimahi-agents/kaimahi/pull/781):
  native Run/Chat requirement authoring, forwarding and observations.

See the [posted response to Sertac](https://github.com/orka-agents/orka/pull/831#issuecomment-6436965569)
on the original RFC for the approach and its relationship to his feedback.
Historical pins and qualification records are retained below. Follow-up pins
are additive, not a relabeling of those records.

## Follow-up source selection

Clone only the owner-controlled repositories into a new directory:

```sh
git clone --branch guardd-2 https://github.com/vfalico/orka-public.git orka
git clone --branch guardd-2 https://github.com/vfalico/kaimahi-public.git kaimahi
git clone --branch guardd-2 https://github.com/vfalico/agentsuite-guardd-public.git guardd

git -C orka switch --detach 673de3962dd42de39ef7b212c0be2b6e9b3c681b
git -C kaimahi switch --detach 1286b13b9a89d380e420c795859270ce9a10e881
git -C guardd switch --detach 73e7576b8382ded9d593d921cf4b12c55c0b997e
python3 guardd-2-integration-public/tools/verify-source.py --root . --followup
```

Orka integrates main `075437a99f4f96ee2614cef28884c9a1ece05568`.
Its later normal child `673de396` adds only the source/generated chart
namespace guard and its behavioral regression. It rejects a configuration
already refused by controller startup; valid fixed-input renders are unchanged.
These files are excluded from the five unchanged runtime image build contexts.
Observed Orka images and chart remain bound to `3419c905`/tree `52a5a16f`;
this is not another image build or physical qualification.
Kaimahi integrates `c5fa94eed6e46fefb0d7050b9632febff97c83a6`;
`3bca56eaf1ff916b5cedd4639d78bd2f71816074` is instead the separate
Linux CI merge target recorded in the manifest. Do not claim it is an
ancestor of the published Kaimahi tip.
The later target `6da5db77f44b775cbbdb91962b3e156e9d4917ea` is separately
tested in synthetic merge `e1aaf699`, not integrated into the review branch.
The final frozen Linux supplement tests target
`78026866daccf84b8e8112a7018d45ebee0ef54a` in synthetic merge `e050df6`,
tree `e6b8b9a`, including its complete agentfile package and 95 compiled
file-preview App declarations. It does not qualify subsequent main advances.
The final review commit moves four ordinary package-comment lines only,
resolving their shared insertion anchor without importing new upstream behavior.
All executable source is unchanged from EA; the artifact record remains bound
to EA/tree `d038383f`, not the later review tree. Synthetic CI hashes identify
private receipts, not public downloadable objects or an artifact attestation.

The follow-up verifier checks exact tips/trees, baseline and integrated-main
ancestry, and the complete ordered owner series after excluding those mains.
It preserves legitimate upstream attribution and applies the contributor
policy to owner commits only. It does not validate artifact digests or establish
test execution, binary provenance or live enforcement.

These histories contain merges. To preserve their actual commit graph, export
a Git bundle from a complete clone, for example:

```sh
git -C orka bundle create ../orka-guardd2.bundle HEAD
```

A binary `git diff --binary --full-index <baseline> <tip>` can reproduce
tracked content on its exact baseline, including integrated upstream changes;
it does not preserve merge topology or replace commit/DCO provenance. Do not
apply the historical linear mail-patch recipe below to the new merge graph
and assume `git am` reproduces it.

## Original pinned source, without touching upstream

Run these commands in a new directory. Only owner-controlled public
repositories are cloned; no command publishes anything or opens a PR.

```sh
git clone --branch guardd-2 https://github.com/vfalico/orka-public.git orka
git clone --branch guardd-2 https://github.com/vfalico/kaimahi-public.git kaimahi
git clone --branch guardd-2 https://github.com/vfalico/agentsuite-guardd-public.git guardd

git -C orka switch --detach aaed0ef89d78207d4ae66192ba432b7707e6321c
git -C kaimahi switch --detach 019e0de701c1a3ab32149c53dfe08db830b2af94
git -C guardd switch --detach 73e7576b8382ded9d593d921cf4b12c55c0b997e
```

Put this guide alongside those directories, then run:

```sh
python3 guardd-2-integration-public/tools/verify-source.py --root .
```

The verifier checks tracked cleanliness, exact tip/tree, ancestry, every
ordered series commit and the [commit policy](../CONTRIBUTING.md). It does not
run tests, inspect ignored build outputs, verify a binary or establish live
enforcement.

Kaimahi's original refreshed review baseline is
`3a0ab5695201e088acda79a4f4981f8e40da1cb2`. Its seven commits preserve six
feature patches unchanged; the CLI patch integrates current FILE semantics,
refusal regressions and a release-note fragment. See
[qualification](qualification.md#current-kaimahi-review-refresh) for the exact
boundary between fresh hermetic checks and historical live E2E evidence.

For the original qualified Kaimahi sources, use a separate clone and select
`guardd-2-qualified-20261026`. Its exact tip and tree are recorded under
`projects.kaimahi.qualifiedReviewSnapshot`. The verifier above checks current
review pins, not that historical checkout.

Preserve canonical Go module paths. A fork URL is a source/review location,
not a reason to rewrite imports. Do not push to an upstream repository or open
an upstream PR merely because these commits are structured for review.

## Start with independent fixes

| Orka commit | Purpose | Applicability |
| --- | --- | --- |
| `cd0c8ff44310c6180709a55868b4a7686dd1f64c` | Fall back when Responses rejects tool use before any output. | Ordinary compatibility fix; no Guardd or enforcement provider required. |
| `8e11b57868e13d1baa1b6bbbe90aea9fd617c568` | Retire an exact cancelled standalone reservation without waiting for a nonexistent session acknowledgement. | Ordinary lifecycle fix; independent of the first fix and of Guardd. |

Inspect each with `git -C orka show <commit>`. For a standalone trial, use a
separate review copy at Orka baseline
`2026da6ad6e890070de4b28309d478319bc28cb7` and cherry-pick just the selected
fix. The fallback is narrow: it is not permission to replay arbitrary failures
or responses that have already produced output.

## Then review the feature series

The exact ordered commit IDs and subjects are in `release-manifest.json`.
Messages contain change-specific rationale, not repeated dependency,
validation or limitation boilerplate. This review map owns series dependencies;
the qualification document owns the evidence and its boundaries.

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

## Historical linear mail-patch export

This recipe applies to the original `projects` records, not the merged
`followupPublication` histories. Use the original baseline for each project:

```sh
mkdir orka-patches
git -C orka format-patch --output-directory ../orka-patches \
  2026da6ad6e890070de4b28309d478319bc28cb7..aaed0ef89d78207d4ae66192ba432b7707e6321c
git -C orka diff --stat \
  2026da6ad6e890070de4b28309d478319bc28cb7..aaed0ef89d78207d4ae66192ba432b7707e6321c
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
manifest retains the actual built/exercised sources separately from the later
Kaimahi review refresh. That refresh has hermetic verification, not new live
E2E qualification.

Upstream review takes place in the linked PRs. The reproduction commands above
remain read-only: they do not publish branches, issues or additional PRs.
