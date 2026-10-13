# stateaxis-sleep-wake

Extension ID: `org.vllm-hust.stateaxis-sleep-wake`

Experimental, default-off whole-worker lifecycle MOD. Under explicit ECPA
authority, StateAxis sleeps only after proving there are no active states,
requests, continuations, host-tier states, or APC entries. Wake must reproduce
the exact assembly identity and worker capacity geometry or the service faults
closed. Direct CLI activation is unsupported.

## Evidence boundary

Historical Qwen2.5-14B real-NPU evidence is positive for **idle resource
release**: every candidate run released 51,653 MiB. Wake p95 was 35.892 seconds
and post-wake requests remained exact. This is not an inference speedup or broad
performance qualification; the MOD remains opt-in and experimental.
The complete formal bundle is vendored under
`evidence/issue58-sleep-wake-20260816-r1/`.

Current ECPA evidence covers digest binding, lifecycle counters, repeated exact
mock-worker sleep/wake, failure recovery, geometry drift rejection and Manager
launch composition. See `EVIDENCE.md`.

```bash
python -m pip install -e '.[test]'
pytest -q
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json \
  vllm-hust-ext extension check org.vllm-hust.stateaxis-sleep-wake
```

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.
