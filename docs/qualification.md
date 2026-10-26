# Qualification and retained limitations

## Exact source and artifacts

`release-manifest.json` records the tested baseline, ordered commits, final
tree, CLI/chart hashes and all six locally built image manifest/config digests.
The five Orka images and Guardd provider were built from the actual fresh
integrated sources, imported privately and checked against live container
identities. They are **not published images** or an image download catalog.

The supported observed profile was Linux/amd64, cgroup v2, containerd/K3s,
bpffs, BPF LSM and the documented management privileges. A selected kernel BTF
header and independently checksum-verified `crictl` were build inputs.
This does not qualify another kernel, architecture, runtime or deployment.

Before deployment, independent installed-file comparison rejected a stale
Guardd image even though its candidate source Git tree matched an earlier
tree. A fresh image was built instead. All 27 installed provider Python files
and 36 recorded provider/native inputs were then compared with the actual
candidate source. A source hash alone was not treated as binary identity.

The lab upgrade preserved all 211 pre-existing protected UID/spec
fingerprints. The current upstream AgentHost CRDs/schema additions were
retained, not deleted to make older manifests fit.

## Fresh actual journeys

| Journey | Semantic result | Enforcement/operational observation |
| --- | --- | --- |
| New Kaimahi native suite | Create, full evaluation 1/1 and candidate cleanup; actual evaluated local OCI push; digest-only plan and Deploy; protected Run exactly `4`. | Exact new Task/Job/Pod/container, current-generation admission, real native UID1000 filesystem/TCP/UDP controls and BPF state. |
| Standalone Orka native | New Agent/Task, authenticated result exactly `4`, single attempt. | Same complete native policy, fresh physical incarnation and independent same-container controls. |
| Kaimahi Chat | Real PTY/VT displayed `17`; actual read-only CLI result matched; one new Task and exit 0. | Same complete requirement and exact-generation historical admission. No separate Chat-specific kernel probe is claimed. |
| Standalone Orka ACP | One new managed OpenCode Task completed a useful, substantially correct two-file review of startup/build/entrypoint/binary provenance. | Exact runtime image/Pod/container/cgroup, independently live binding, root-UID same-container controls, BPF state and ordinary TCP listeners. |

Filesystem measurements included successful `/tmp` write/read/unlink and
EACCES on a protected tree independently shown to be writable without the BPF
rule. Network measurements included actual permitted and denied TCP, and
connected plus unconnected UDP/DNS. Namespace/cgroup and actual observer
credentials were checked: host connectivity or a test in a lookalike Pod did
not count.

These are bounded measurements, not an exhaustive kernel escape assessment.
ACP's fresh physical probe used runtime-root UID0. It does not separately
measure every coding-child UID or requalify checkout immutability.

All new Tasks were terminal. The three native bindings retired normally.
The one new idle ACP pool was deleted with an exact UID precondition and its
binding independently reached `RETIRED`; its Task history was preserved.
The campaign's coding backend container was stopped/removed and the separate
bounded native bridge was stopped. Earlier protected task/installation history
was not deleted.

## Model-bound results

**Native qualified profile:** cached Ollama `qwen2.5:3b`,
model digest
`357c53fb659c5076de1d65ccb0b397446227b71a42be9d1603d46168015c9e4b`,
3.1B Q4_K_M, CPU serving. This is an explicit new model-bound authoring,
evaluation, package/digest deployment and protected invocation, not an
unrecorded endpoint substitution.

**ACP qualified factual-review profile:** official
`Qwen/Qwen3-Coder-30B-A3B-Instruct`, revision
`b2cff646eb4bb1d68355c01b18ae02e7cf42d120`, BF16, native template,
vLLM 0.10.2, `qwen3_coder` tool parser, automatic tool choice and no reasoning
parser, native context 32768/output budget 4096. The official metadata and
all 16 weight shards were independently hashed. A route alias was not treated
as evidence of the underlying model.

## Unresolved and failed observations: keep them failed

1. **Native Qwen3-Coder exact-answer failure remains unresolved.** An earlier
   fresh protected native Run returned literal `4\n<tool_call>`. Admission,
   physical controls and Task `Succeeded` did not make that an exact `4`.
   No markers were stripped, no identical inference was retried for luck,
   and no backend-only cause was established. The separately qualified
   general native model neither fixes nor exonerates this compatibility seam.
2. **ACP useful factual review is not perfect prompt compliance.** The fresh
   answer identifies the correct startup, build/copy/ENTRYPOINT paths and
   prebuilt upstream binary distinction. Its displayed build block is not an
   exact excerpt: it drops `sharing=locked` and changes the continued ending.
   It labels build output `/out/orka-acp-runtime` imprecisely before supplying
   the correct final installation copy. It omits the full requested native
   artifact-flow excerpt, and redacted tool events do not prove the separate
   grep verification. Earlier strict excerpt/grep experiments also remain
   failed. Do not advertise full compliance or universal model quality.
3. A broad fresh Orka test selection encountered five unrelated Git fixture
   failures with `safe.bareRepository=explicit`. The safety setting and
   unrelated tests were not changed. No full-suite-green claim is made.
4. An initially selected worker test regex matched zero tests. That output
   was rejected as coverage; the two actual named native admission tests
   were then run and passed.
5. An initial noninteractive evaluation omitted exact-context confirmation
   and safely refused before execution. The correctly confirmed new
   invocation is the executed result, not a claim that the refusal ran tests.

## Builds and tests actually reused

The standard Orka controller/UI build passed after restoring a missing Bun
dependency privately, without source workarounds or global installation.
Focused controller/enforcement/API/ACP/Helm checks and the two actual native
admission tests passed. Kaimahi focused tests/build passed. The six actual
candidate images built and were exercised as described above.

Earlier exact-series application/prefix checks and original successful tests
remain historical evidence, not another execution on fresh main. Identical
successful heavy tests are not rerun merely for repackaging.

## Evidence availability and reproduction

This public repository intentionally publishes **sanitized outcome summaries
and exact code/artifact identities**, not private raw transcripts, process
state, endpoint configuration, credentials, kubeconfigs or the private evidence
archive. It is not a publicly replayable raw-evidence bundle or signed
attestation. Published summaries state their observation scope explicitly.

Use [build and use](build-and-use.md) and the source-owned examples to repeat
the workflows in a separately authorized compatible lab. For physical
qualification, independently establish Task -> Job/RuntimePool -> Pod -> CRI
container -> live PID/cgroup, observe authenticated provider readback and the
pinned BPF maps, and run actual positive/negative probes at the workload's
credentials in that exact cgroup. Retain immutable inputs and failed results.

A `kubectl exec` can fail during CRI bootstrap after foreign Unix brokers are
blocked. Do not add an exemption to make a probe run. The accepted procedure
uses a privileged observer that enters the independently verified container
namespaces/cgroup and drops credentials, or starts a probe before activation.
No such observer is automatically installed or authorized by this guide.
