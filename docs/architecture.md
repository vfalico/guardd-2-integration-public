# Architecture and trust

```text
Kaimahi native Run/Chat           standalone Orka Task / UI / API
             \                    /
              one complete immutable Task requirement
                              |
                         Orka controller
                 select exact physical incarnation
                 prepare/hold; do not dispatch yet
                              |
               authenticated mandatory-provider checks
                              |
               Guardd node-incarnation-specific provider
                 resolve actual CRI container and cgroup
                 install + independently read back controls
                              |
                   one combined BPF container boundary
                      filesystem + IPv4 TCP/UDP
                              |
               matching admission publication -> release
                              |
                   terminal -> fenced physical retirement
```

## What is existing, changed, or new?

Kaimahi remains the existing CLI and native AgentSuite lifecycle. Orka remains
the existing controller/API/UI, native worker and managed ACP supervisor.
`orka-acp-runtime` lives **inside Orka**: its executable starts at
`cmd/orka-acp-runtime/main.go` and uses `workers/acp/supervisor`. It is not a
separate dependency or another newly introduced agent.

The series modifies these existing paths to preserve whole requirements,
separate ACP preparation from launch, gate exact physical admission and retain
cleanup obligations. Kaimahi adds explicit candidate/enforcement options to
its normal workflow, rather than another Guardd-specific CLI.

Guardd's new lane is the provider-neutral Kubernetes/containerd adapter,
durable authenticated service, combined native policy enforcement and
optional installation. Its source repository also retains older signed/Unix
protocol implementations. Those compatibility lanes are not the new Orka
gRPC provider; do not mix their configuration or receipts.

The upstream **OpenCode 1.19.0 executable is unchanged**. Orka's
`workers/acp/images/opencode/Dockerfile` checksum-verifies its prebuilt native
npm artifact and installs it at `/opt/opencode/bin/opencode`. It compiles the
Orka supervisor from source and installs that separate executable at
`/usr/local/bin/orka-acp-runtime`, the image ENTRYPOINT. Downloaded upstream
source/license material is not a claim that the OpenCode binary is rebuilt
from source. The upstream agent runs as the supervisor's ACP child.

## Whole requirements, not inferred policy

The Task supplies format, exact base64 policy bytes, ordered capabilities and
`mode: enforce`. There is no inherited Agent policy, merge, endpoint discovery
grant, partial success or advisory/unprotected fallback. Orka treats the
provider policy as opaque. Every configured mandatory provider must confirm,
and their coverage must include every requested capability.

The combined Guardd v3 profile binds filesystem and network to the same exact
container/cgroup generation and one native object/lifecycle. Provider-neutral
does not mean every provider supports every format or runtime. Unsupported,
missing, uncertain and stale authority refuse dispatch.

## Privileged management and runtime boundaries

The controller registry, client certificates, Guardd keys, node state,
host PID/cgroup/bpffs and CRI access are trusted operator authority. They must
not enter a governed workload. Exact Node UIDs and per-incarnation authenticated
routes matter; a shared endpoint with a reusable identity is insufficient.

Use three distinct namespaces: privileged management, watched native Tasks,
and managed ACP runtimes. The native worker's existing Secret-reading role
makes management/Task colocation inappropriate. An installed enforcement
boundary refuses that colocation rather than silently weakening it.

The managed native entrypoint waits before initialization. ACP can prepare a
session without starting its agent, then launch only after matching admission.
The latter is a managed whole-runtime-container profile, including the
privileged supervisor, not a claim that a policy protects an arbitrary remote
ACP endpoint or separately allocated execution worker.

## Guarantees and exclusions

- The filesystem rule protects captured existing inode identities against the
  supported mutation operations. It does not establish read confinement,
  protection of future descendants, external symlink destinations or protection
  against arbitrary privileged host writers.
- The network policy is an explicit IPv4 TCP/UDP transport ceiling. Unlisted
  destinations and unsupported transports refuse; it is not URL/hostname or
  proxy-upstream authorization. DNS, model traffic, controller callbacks,
  health replies and loopback proxies need deliberate grants.
- ACP's explicit exact-IP/all-port health-reply and loopback rules are broader
  transport ceilings, not hidden exceptions. Reject the profile if they are
  unacceptable. Multipath TCP is not qualified; supervisor listeners explicitly
  use ordinary TCP.
- `/workspace` in the no-repository native example and `/home/worker` in ACP
  are different protected trees. The latter does not make an ACP checkout
  immutable; separate workspace protections must not be attributed to Guardd.
- Init containers, separate `code_exec` Jobs, external tools/MCP, other Pods,
  other architectures and untested kernels are not covered by these results.
- Privileged/root host and Kubernetes-management administrators remain trusted.
  Physical observer access is trusted observation, not tenant authority.

## Receipts, reuse and retirement

Task `status.enforcementAdmission` plus its generation-matched condition is a
**historical admission observation**. It is not a live provider check, a
general authorization token or permission to detach a restriction. Reuse
requires current proof for the same exact physical incarnation; policy
replacement is not a live map edit.

Bindings persist uncertain cleanup responsibility. Physical retirement uses
the guarded stopped/empty lifecycle, not an answer string or an arbitrary
client request. Installer disable/uninstall also retains authority and cleanup
obligations. Use the compatible chart's documented lifecycle; deleting its
state/trust or raw historical rollback is not a supported decommission.

Read the pinned component documentation before operating:

- Orka: `docs/development/container-enforcement.md`.
- Orka: `config/samples/enforcement/README.md`.
- Guardd: `docs/CONTAINER_POLICY.md`, `docs/SECURITY.md`, `docs/PROTOCOL.md`.
- Guardd: `charts/guardd/README.md`, `packaging/kubernetes/README.md`.
