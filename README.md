# Guardd 2: review, build, and qualification

This is the integration guide for the **`guardd-2` review series**, not a new
agent runtime or an automatic installer. It connects the existing Kaimahi
native workflow and Orka's native/managed-ACP execution to one optional,
provider-neutral, fail-closed container-enforcement boundary.

Both filesystem and network requirements are submitted together. They are not
the filesystem-only AgentPolicy integration described by the predecessor guide.

## Upstream review

The series was submitted for upstream review on 2026-10-27:

- [orka-agents/orka#952](https://github.com/orka-agents/orka/pull/952):
  optional container enforcement for native and managed ACP Tasks.
- [kaimahi-agents/kaimahi#781](https://github.com/kaimahi-agents/kaimahi/pull/781):
  enforcement requirement authoring and observations in native Run and Chat.

The [response to Sertac on the original RFC](https://github.com/orka-agents/orka/pull/831#issuecomment-6436965569)
summarizes how the implementation addresses his feedback and links both PRs.

Source branches and responsibilities:

| Repository | Review branch | Responsibility |
| --- | --- | --- |
| [vfalico/kaimahi-public](https://github.com/vfalico/kaimahi-public/tree/guardd-2) | `guardd-2` | Verified local candidate installation; native evaluation/digest Deploy; complete Run/Chat requirement forwarding and safe observations. |
| [vfalico/orka-public](https://github.com/vfalico/orka-public/tree/guardd-2) | `guardd-2` | Task admission, held native initialization, managed ACP preparation/launch, exact physical binding, mandatory-provider verification and retirement. |
| [vfalico/agentsuite-guardd-public](https://github.com/vfalico/agentsuite-guardd-public/tree/guardd-2) | `guardd-2` | Exact Kubernetes/containerd resolution, authenticated durable provider, combined BPF controls and optional node-provider installation. |
| This repository | `main` | Pinned source/commit/artifact identities, review order, build/use instructions and honest qualification limits. |

**Start with [the review map](docs/review.md), then [build and use](docs/build-and-use.md).**
[Architecture and trust](docs/architecture.md) explains the boundary.
[Qualification](docs/qualification.md) distinguishes actual results from
unresolved observations. [`release-manifest.json`](release-manifest.json)
contains the exact source commits and trees: branch names alone are not pins.
The [commit policy](CONTRIBUTING.md) requires contributor DCO sign-offs and
prohibits assistant-attribution/session trailers and repeated message scaffolding.
The historical DCO/message-only replacements preserve source and patch payloads;
both maps remain intact. Kaimahi's current review branch additionally integrates
fresh main. Its original qualified snapshot is retained separately in the
manifest and the `guardd-2-qualified-20261026` tag, not relabeled as the refresh.

## Review shape

There are **26 feature-series commits: Orka 12, Guardd 7, Kaimahi 7**.
Orka's first two commits are independent ordinary bug fixes; neither requires
Guardd. Later feature commits have explicit dependencies and are not claimed
to be independently deployable. Guardd's new `main` additionally retains two
baseline prerequisites, listed separately in the manifest rather than hidden
inside the seven-commit count.

The read-only upstream mains integrated before the original qualification were:
Orka `2026da6ad6e890070de4b28309d478319bc28cb7` and
Kaimahi `7959afdce64e262417ed214c5b1dd26af1456d1a`.
Upstream additions, including AgentHost functionality, were preserved. This is
qualification of these exact snapshots plus the series, not a promise about
whatever an upstream branch points to later.

Kaimahi's current review series is now based on
`3a0ab5695201e088acda79a4f4981f8e40da1cb2`, at tip
`019e0de701c1a3ab32149c53dfe08db830b2af94`. Six patches are unchanged; the
CLI patch preserves the updated upstream FILE command semantics and adds
behavioral refusal checks and its release note. Focused tests, vet and the
CLI build passed. This refresh is not a new live E2E qualification; the
artifact digests and demonstrations below remain tied to the manifest's
explicit historical qualified source trees.

## Actual pre-publication results

On the supported disposable Linux/amd64 Kubernetes/containerd lab profile:

| Journey | Result |
| --- | --- |
| Kaimahi create -> full native test -> local OCI push -> digest plan/Deploy -> protected Run | Evaluation 1/1 with cleanup; new protected Run answered exactly `4`. |
| Kaimahi protected Chat | Actual rendered terminal and read-only CLI result both showed `17`; normal exit. |
| Standalone Orka native Agent/Task | Answered exactly `4` through the authenticated result API. |
| Standalone Orka managed OpenCode ACP | Completed a useful, substantially correct two-file source review; strict excerpt/tool-verification compliance is **not** established. |

The two native execution journeys and ACP each had independent
**same-physical-container** filesystem and TCP/UDP allow/deny observations,
matching BPF state and exact source-derived image identities. Chat has its own
actual invocation/admission/visible-answer proof, not another kernel campaign.
All four new bindings were retired after use, all new Tasks were terminal,
and the bounded model/bridge processes were stopped.

**Important unresolved result:** native execution with the separate
Qwen3-Coder profile returned literal `4\n<tool_call>`, failing the exact-answer
contract despite successful admission and enforcement. The qualified native
profile is `qwen2.5:3b`; changing models did not establish the other failure's
root cause or fix it. See the full [limitations and retained failures](docs/qualification.md).

## Additional matched agent evidence

A later 15-case extension applied five scenarios to each of Kaimahi Run,
native Orka and managed ACP. Nine cases contain actual kernel-denial evidence;
none earns full strict acceptance. One case failed before tools, four ACP
cases hit outer tool permissions, and another ACP case refused the requested
probes. All outcomes and cleanup were retained without case reruns.
See the [complete matrix and limitations](docs/qualification.md#additional-five-scenario-matched-campaign);
these results do not relabel the earlier successful ACP demonstration.

## Scope

This is an experimental, reviewable source integration, not a general sandbox,
an all-model compatibility claim or a production release. No public images,
private raw evidence, credentials or lab configuration are distributed here.
Rebuilding does not guarantee identical binaries or image digests.

The previous
[AgentPolicy integration guide](https://github.com/vfalico/agentpolicy-guardd-integration-public)
and [IG/KMX implementation](https://github.com/vfalico/ig-kmx-guardd-public)
remain historical records. Their policy APIs, branches and qualification do
not describe this series. The existing
[`vfalico/agentsuite-guardd`](https://github.com/vfalico/agentsuite-guardd)
is preserved, not archived.

Documentation uses the Apache-2.0 license; each source project retains its own
license, notices and canonical module/import paths.
