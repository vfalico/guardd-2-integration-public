# Build and use

Read [architecture and trust](architecture.md) before operating. These
commands are opt-in examples for an authorized disposable lab, not permission
to change production, download models, contact paid inference, publish images
or remove retained installation state.

## Current follow-up build and CLI

Use the [follow-up source selection](review.md#follow-up-source-selection) and
the explicit `--followup` verifier mode. Local verification uses Go 1.27.3
for Orka and Go 1.26.10 for Kaimahi; follow each exact component's manifests
and Dockerfiles for its other build inputs. This does not resolve or erase
the retained Go 1.27.2 compiler/runtime risk.

```sh
(cd kaimahi && GOTOOLCHAIN=go1.26.10 make build)
(cd orka && GOTOOLCHAIN=go1.27.3 make build)
```

Use the built binary's help and the
[exact Kaimahi source documentation](https://github.com/vfalico/kaimahi-public/blob/1286b13b9a89d380e420c795859270ce9a10e881/docs/kmx.md)
for current `cluster`/`package` routing and FILE/workspace semantics.
The original root-command examples below are historical, not instructions
for those newer CLI sources. Do not infer new flags from old recipes.

Materialize complete requirements against verified current workload/Pod,
Service and endpoint identities before freezing a new Task. Historical
controller/proxy IP grants are not portable defaults. Preserve profile-specific
permissions: the follow-up native grant did not gain an ACP proxy or TCP
wildcard. Never patch an admitted requirement to accommodate infrastructure
drift; fail visibly and prepare a separately identified future request.

## Original qualified-profile recipe

The numbered sections below retain the original sources, toolchains, command
routes and lab workflow. Select the original pins in the review map and use
the default verifier to follow that historical recipe. Do not mix it with
follow-up pins or treat it as new qualification.

## 1. Original source and prerequisites

Follow [the original clone/verification instructions](review.md#original-pinned-source-without-touching-upstream).
The original build used Go 1.27.2,
Python 3, Bun (the fresh build used 1.4.4), Helm 3, Kubernetes CLI and
kustomize 5.7.1 (also installed locally by Orka's manifest target).
Image building additionally needs Docker Buildx/BuildKit. Native compilation
needs BTF/bpftool, clang and the source's libbpf/runtime dependencies.
Follow each pinned component's dependency manifests rather than substituting
unverified executable downloads.

The clone/source-verifier instructions select the current review sources.
To reproduce the historical live-qualified Kaimahi source instead, use a
separate clone at `guardd-2-qualified-20261026` and compare its HEAD/tree to
`projects.kaimahi.qualifiedReviewSnapshot`. The manifest's observed artifact
hashes belong to the explicitly recorded qualified trees, not the newer
Kaimahi review tree. The refreshed Kaimahi-only checks/build used Go 1.26.10;
follow each component's pinned toolchain rather than inferring a tested
compiler from another component's build.

Build on an explicitly capped builder if the host is shared. Capping only
the Docker client does not cap BuildKit's daemon processes. Keep credentials
and runtime state outside source/build contexts.

From the parent of the pinned repositories:

```sh
(cd kaimahi && make build)
(cd orka && make build)
```

`kaimahi/bin/kmx` is the resulting CLI. Orka's standard build includes manifest/
code generation, formatting/vet, the actual UI production build and binaries.
Inspect `git diff --exit-code` afterward; do not dismiss generated-source drift.
These build commands are not E2E qualification.

## 2. Build only the required images, without pushing

From `orka`, use the actual source Dockerfiles. For example:

```sh
docker buildx build --platform linux/amd64 --provenance=false --sbom=false \
  -f Dockerfile -t localhost/guardd2/controller:local \
  --metadata-file controller.build.json \
  --output type=oci,dest=controller.oci.tar .
```

Repeat with a distinct tag, metadata and OCI output per component:

| Component | Dockerfile |
| --- | --- |
| Native AI worker | `workers/ai/Dockerfile` |
| General worker | `workers/general/Dockerfile` |
| Workspace publisher | `workers/publisher/Dockerfile` |
| Managed OpenCode ACP runtime | `workers/acp/images/opencode/Dockerfile` |

There is no need to build or enable Codex, Claude, Copilot, AgentKit or Foundry
to reproduce this profile. Do not run an all-images push target.

Build Guardd using its exact
[`packaging/kubernetes/README.md`](https://github.com/vfalico/agentsuite-guardd-public/blob/guardd-2/packaging/kubernetes/README.md):
provide a trusted `vmlinux.h`, a checksum-verified native `crictl`, an explicit
base manifest digest and a recorded source epoch through the named
`guardd_inputs` context. Build `packaging/kubernetes/Dockerfile` to a private
OCI archive. Do **not** add `--push`.

The source manifest pins the observed artifacts, not a claim that a clean
rebuild will have their digests. Dependency resolution, build metadata and
timestamps can differ; retain the newly resolved inputs and actual receipts.
Git archives can isolate tracked source from ignored local build files.

## 3. Compose the optional chart from real source charts

Package the actual standalone Guardd chart:

```sh
mkdir -p chart-inputs
helm package guardd/charts/guardd --destination chart-inputs
sha256sum chart-inputs/guardd-0.1.0.tgz
cp -R orka/cmd/build/helmify/static chart-inputs/static
```

Edit the copied `chart-inputs/static/values.yaml` **before generation** to
select your actual built images and the isolated namespaces listed below.
Set a distinct valid candidate version/appVersion in its `Chart.yaml`.
These private generator inputs are not changes to the pinned source.

From `orka`, generate the ordinary canonical CRDs with `make manifests`.
The generator reads a YAML stream; create one without flattening resources:

```sh
kustomize build config/crd > ../chart-inputs/generated-crds.yaml
go run ./cmd/build/helmify \
  --output-dir ../chart-inputs/orka \
  --static-dir ../chart-inputs/static \
  --enforcement-chart ../chart-inputs/guardd-0.1.0.tgz \
  --enforcement-chart-sha256 <actual-guardd-chart-sha256> \
  < ../chart-inputs/generated-crds.yaml
```

Verify the exact generated chart contains **your actual built immutable
references**, never an untested version tag. The
Kaimahi candidate derives native/ACP worker choices from the candidate chart;
Helm overrides alone do not redefine a candidate's tested image identity.
Do not hand-copy Guardd templates into Orka or edit source-owned generated
outputs to masquerade as a different candidate.

Important candidate defaults/installation values:

| Value | Required selection |
| --- | --- |
| `controller.image`, `workers.ai.image`, `workers.general.image`, `publisher.image` | Correct repository/digest and appropriate pull policy. |
| `controller.acpRuntime.opencodeImage` | Exact built OpenCode runtime image reference. |
| `enforcement.image` | Exact built Guardd provider image. |
| `controller.watchNamespace` | Precreated isolated Task namespace. |
| `controller.acpRuntime.namespace` | Third namespace, distinct from Tasks and management. |
| `enforcement.criSocketDirectory` | Actual selected runtime socket directory, not an assumed Docker path. |
| `enforcement.nodeSelector` | Only explicitly selected compatible lab nodes. |
| Proxy/model configuration | Existing approved local native Provider and ACP model route, without credentials in Tasks. |

Package the candidate with `helm package`, retain its SHA256 and keep all
platform/default image requirements explicit. Import the OCI archives into
the selected node's container runtime. For local K3s, Guardd's image README
documents adding the exact repository-digest reference and checking CRI
`repoDigests`; a tag-only import is insufficient. `imagePullPolicy: Never`
is appropriate only after those exact bytes are imported.

The candidate is operator-supplied, not publisher-attested. All changed
candidate bytes mean a new hash and new evaluation identity.

## 4. Install/enroll with the supported client

Kaimahi uses its existing `orka-system` management release; the verified
candidate's `controller.watchNamespace` selects the separate Task namespace.
Precreate that Task namespace and the distinct ACP namespace as described in
the source documentation. Provision actual bpffs/BPF-LSM/runtime prerequisites
using the node's normal management mechanism; do not silently alter boot
settings or substitute readiness for independent enforcement.

Use the current candidate CLI, an explicit context, a verified local chart,
and your approved local model route:

```sh
kmx orka install --context "$CONTEXT" \
  --chart "$CHART" --chart-sha256 "$CHART_SHA256" --enforcement \
  --provider "$PROVIDER" --model "$MODEL" --model-url "$MODEL_URL"
```

Inspect `kmx orka install --help` for the actual supported flags; do not assume
there is a Task-namespace install flag in this CLI. Configure the separate
ACP provider-proxy route and model before
the ACP journey; native Provider setup alone does not configure that route.
Do not add credentials to the guide, policy file or Task.

Enabling an addon is not the Task requirement. Omitting enrollment on an
existing installation preserves its explicit state; it does not silently
disable protection. Use compatible upgrades and the chart's retained
disable/uninstall/reinstall lifecycle, not raw historical rollback or ad hoc
deletion of keys/state. On upgrades, preserve all actual explicit values and
account for new chart defaults; blind reuse of old defaults is not a safe
fresh-version integration.

## 5. Kaimahi native lifecycle, then protected Run/Chat

The installed binary's help is authoritative. Do not use older `eval`/`lift`
examples: the tested current CLI uses `test` and digest `deploy`.

```sh
kmx create demo --workspace ./demo-workspace \
  --model "$MODEL" --instructions ./instructions.md
kmx test --workspace ./demo-workspace \
  --to-context "$CONTEXT" --to-namespace "$TASK_NAMESPACE" \
  --inference "provider:$PROVIDER" \
  --orka-chart "$CHART" --orka-chart-sha256 "$CHART_SHA256" \
  --out ./private-evaluation.json -o json
kmx push --workspace ./demo-workspace --evaluation ./private-evaluation.json \
  --to-layout ./suite-layout agentsuites/demo:v1
```

Read the exact manifest digest from the resulting OCI layout, then use it:

```sh
kmx deploy "agentsuites/demo@$SUITE_DIGEST" --from-layout ./suite-layout \
  --to-context "$CONTEXT" --to-namespace "$TASK_NAMESPACE" \
  --inference "provider:$PROVIDER" --evidence ./private-evaluation.json \
  --promote --orka-chart "$CHART" --orka-chart-sha256 "$CHART_SHA256" \
  --plan -o json
```

Review the GET-only plan, then repeat without `--plan` to apply. Inspect
actual evaluation results and cleanup; an unsigned passing receipt is
historical observation, not authentication or kernel proof.

Materialize the complete native requirement using
`orka/config/samples/enforcement/README.md`. Replace every symbolic address
and port with reviewed actual Service/backend/model/DNS/API destinations;
no component adds missing grants. The native and standalone-native journeys
must use the **same resulting requirement bytes**.

```sh
kmx run --context "$CONTEXT" --agent demo --namespace "$TASK_NAMESPACE" \
  --enforcement-file ./requirement.materialized.json \
  --prompt "What is 2+2? Answer with the single number." --wait 4m
kmx chat demo "Compute 8 + 9. Reply with only the integer." \
  --context "$CONTEXT" --namespace "$TASK_NAMESPACE" \
  --enforcement-file ./requirement.materialized.json
```

Confirm the actual deployed member name rather than assuming the example
name. Run keeps the answer on stdout and observations on stderr. In Chat,
inspect the visible answer and use `/exit` for normal exit. `kmx task result`
reads an existing result without another model invocation.

For noninteractive operation, use only an explicitly approved exact-context
confirmation (`KAIMAHI_CONFIRM="$CONTEXT"`); do not bypass context guards.

## 6. Standalone native and ACP

Use `orka/config/samples/enforcement/README.md` for the exact native Agent/Task
and ACP Agent/Task templates. Materialize the policy first; the intentionally
incomplete Task samples must fail closed if submitted directly.

For native, select the Ready native Provider and submit the same complete
requirement used by Kaimahi under a new Task name. For ACP, select the managed
OpenCode image and approved model route, pin the workspace repository/ref,
and author the separate complete ACP policy with its deliberate health/proxy/
loopback ceilings. The qualified factual-review profile and its limitations
are in [qualification](qualification.md).

Read results through the normal authenticated API with least-privilege
Task-read authority. Verify exact-generation admission separately from answer
correctness and independent physical controls. Do not treat success, a Ready
Pod, an image label, a historical receipt or a test in another cgroup as
current complete enforcement.

## 7. Focused checks and physical acceptance

Run tests deliberately; they can consume resources. The source projects retain
their own test suites. For a small starting point:

```sh
(cd guardd && PYTHONPATH=src python3 -m pytest)
(cd orka && go test ./workers/common -run \
  '^(TestEnforcedEntryPointCannotSilentlySkipMissingConfiguration|TestNativeWorkerWaitsForCurrentPodAdmission)$')
```

Use source-owned controller/enforcement/API/ACP/chart and Kaimahi tests for
their relevant changes. Inspect how many tests actually ran; an empty selector
is not coverage. Full suites can need additional dependencies/envtest assets
and are not claimed green by this publication.

Real acceptance additionally requires actual allowed/denied FS and TCP/UDP
operations in the exact physical container at the expected credentials, plus
live binding and BPF readback. See the [observation checklist and constraints](qualification.md).
Do not weaken the policy to make an observer or model work.
