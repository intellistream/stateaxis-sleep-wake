# Issue #58 sleep/wake and online weight-release closure

> **Point-in-time report — not current repository status or a task
> assignment.** Current classification and defaults live in
> [`NATIVE_ENGINE_STATUS.md`](../../NATIVE_ENGINE_STATUS.md).

Issue #58 adds a default-off Rust supervisor around the replaceable native
worker. Sleep is allowed only when the runtime has unique ownership and the
worker reports no active state, request, continuation, host-tier state or APC
entry. It then terminates the complete C++ worker, releasing weights,
workspace and paged KV together instead of partially freeing allocator-owned
pointers. Wake starts the same command and accepts it only after the existing
state/execution digest handshake and an exact capacity-geometry comparison.

Requests while sleeping or faulted return HTTP 503. Concurrent handlers,
persistent state, unsupported final-export feedback modes, worker startup
failure and geometry drift fail closed. The public inference protocol is
unchanged; the internal lifecycle endpoints are available only when the
explicit `STATE_ENGINE_SLEEP_WAKE` authority is enabled. Workflow identity
binds that authority bit, and telemetry records requests, applications,
fallbacks, faults, durations and worker epoch.

## Verification

The offline suite passed 259/259 library tests. Dedicated regressions cover
default-off zero behavior, a concurrent request that completes exactly while
sleep falls back, persistent-state refusal, three repeated exact sleep/wake
cycles, and geometry drift that leaves the supervisor faulted.

Formal version `issue58-sleep-wake-20260816-r1` froze commit
`a2f8934892b3578d7a976c2489858e5612d5c8ec`, aggregate identity
`57f25d0778d70320e73090c8bf581829d38ee4338350d07cc51105eb2a58587d`,
the official local `.23` image ID
`sha256:f4c89c293e076453e9eef9edb5fb9669740dccbd3c48619a9f976d775fc29b81`,
the release Rust bundle, Qwen2.5-14B execution artifact, prompt and oracle.
Dynamic two-snapshot admission selected NPU3 with AICore zero and sufficient
free HBM. Control and candidate each ran three fresh server processes in the
preregistered counterbalanced order.

| metric | control | candidate |
|---|---:|---:|
| exact requests/lifecycles | 3/3 | 3/3 |
| authority applications per run | 0 | sleep 1, wake 1 |
| worker epoch | 1 unchanged | 1 → 2 |
| released HBM | sampling noise (-17 to -16 MiB) | 51,653 MiB in every run |
| sleep p50 / p95 / max | disabled | 3.878 / 4.517 / 4.588 s |
| wake p50 / p95 / max | disabled | 34.389 / 35.892 / 36.059 s |
| post-lifecycle request p50 / p95 | 295.371 / 298.982 ms | 363.709 / 364.851 ms |

The initial awake HBM sample and dormant sample directly establish release;
the post-wake exact request, epoch increment and unchanged worker geometry
establish restored execution ownership. All candidate wake durations pass the
600-second SLO. Cleanup removed only the experiment container; NPU3 returned
to AICore zero and baseline HBM.

The result is **positive for bounded idle resource release** and the feature is
retained as an opt-in production candidate. It remains default-off. This is
not an inference speedup claim and provides no comparison with vLLM or
vLLM-HUST. Raw per-arm requests, runtime identities, HBM snapshots, server
logs, status and cleanup evidence are under
`results/issue58-sleep-wake-20260816-r1/`.
