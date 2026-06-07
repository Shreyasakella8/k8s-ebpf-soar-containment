# Cloud-Native SOAR: eBPF-Driven Runtime Detection & Automated Containment

An enterprise-grade, closed-loop automated incident response architecture inside a Kubernetes cluster. This project leverages kernel-level eBPF instrumentation to detect real-time container breaches and execute sub-second automated mitigation.

## Architecture Overview
1. **Telemetry & Detection:** Falco deploys a modern eBPF probe into the worker node kernel to intercept system calls (`syscall`) bypassing standard user-space restrictions.
2. **Orchestration / SOAR Engine:** A multi-container Python Flask microservice receives structured JSON alert webhooks via internal cluster routing.
3. **Automated Containment:** Upon verifying a high-risk runtime exploit (e.g., a terminal shell execution), the Python engine interacts with the Kubernetes CoreV1Api to instantly evict the compromised workload with zero-second grace periods.

## Verification & Proof of Concept
During a simulated terminal hijack exploit inside a target pod, the eBPF sensor registered the violation and triggered the SOAR webhook. The automation engine successfully evicted the compromised workload within **291 milliseconds**, returning an exit code `137` (SIGKILL) to the intruder.
