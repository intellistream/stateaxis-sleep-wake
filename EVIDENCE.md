# Evidence index

- Current activation contract: `evidence/ecpa-contract-20261011/RESULT.json`
  (`manager-contract-mock-worker-non-performance`).
- Frozen real-NPU cell: `evidence/ISSUE58_SLEEP_WAKE_CLOSURE_20260816.md`
  (`historical-real-npu-resource-release-positive-unqualified`).
- Complete frozen bundle: `evidence/issue58-sleep-wake-20260816-r1/`, with
  all six arms, request/lifecycle/HBM/NPU/cleanup records, and a repo-local
  SHA-256 manifest.

The historical cell proves scoped idle HBM release and exact wake recovery. It
does not prove inference acceleration. Current mock-worker checks do not replace
or amplify the hardware result.
