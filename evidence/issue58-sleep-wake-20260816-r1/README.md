# Issue 58 sleep/wake: frozen real-NPU result

This is the complete formal Qwen2.5-14B real-NPU 3+3 bundle. It includes all
arm runs, exact requests, lifecycle counters, worker identities and geometry,
HBM snapshots, NPU admission, server logs, and cleanup records. `SHA256SUMS`
covers every imported file except itself.

Every ON run released 51,653 MiB while dormant and woke to the exact same
execution geometry with worker epoch 1 -> 2. Wake p95 was 35.892 seconds and
post-wake requests were exact. This is positive resource/lifecycle evidence,
not inference acceleration evidence.
