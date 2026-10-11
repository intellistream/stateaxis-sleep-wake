"""Pinned contract for identity-verified StateAxis whole-worker sleep/wake."""

from dataclasses import dataclass

MOD_ID = "org.vllm-hust.stateaxis-sleep-wake"


@dataclass(frozen=True, slots=True)
class SleepWakeConfig:
    enabled: bool = True
    idle_only: bool = True
    require_zero_active_states: bool = True
    require_zero_inflight_requests: bool = True
    require_zero_continuations: bool = True
    require_zero_host_tier_states: bool = True
    require_zero_apc_entries: bool = True
    whole_worker_shutdown: bool = True
    exact_assembly_identity_on_wake: bool = True
    exact_capacity_geometry_on_wake: bool = True
    sleeping_requests_fail_unavailable: bool = True
    wake_failure_faults_service: bool = True
    fail_closed: bool = True

    def __post_init__(self) -> None:
        if not all(
            (
                self.enabled,
                self.idle_only,
                self.require_zero_active_states,
                self.require_zero_inflight_requests,
                self.require_zero_continuations,
                self.require_zero_host_tier_states,
                self.require_zero_apc_entries,
                self.whole_worker_shutdown,
                self.exact_assembly_identity_on_wake,
                self.exact_capacity_geometry_on_wake,
                self.sleeping_requests_fail_unavailable,
                self.wake_failure_faults_service,
                self.fail_closed,
            )
        ):
            raise ValueError(
                "sleep-wake 0.2.0 admits only the complete fail-closed contract"
            )


def sleep_wake() -> SleepWakeConfig:
    return SleepWakeConfig()


__all__ = ["MOD_ID", "SleepWakeConfig", "sleep_wake"]
