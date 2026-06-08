# Automated Kubernetes Runtime Detection & Containment (eBPF + SOAR)

A production-grade, closed-loop incident response pipeline built inside a Kubernetes cluster. This project demonstrates how to orchestrate real-time threat detection via eBPF kernel hooks and seamlessly link it to an automated containment engine to minimize attacker dwell time.

---

## 🏗️ Architecture Overview

The system architecture consists of three core engineering layers:
1. **Vulnerable Vector (Production Namespace):** A frontend Python Flask application mimicking a network diagnostic tool exposed to a simulated Remote Command Injection vulnerability.
2. **Detection Layer (Monitoring Namespace):** CNCF Falco tracking kernel-level system calls via eBPF probes. It actively flags anomalous behaviors such as unauthorized container terminal breakouts (`bin/bash` spawns).
3. **SOAR Engine (Monitoring Namespace):** A custom Python automation responder that consumes Falco's structured JSON alert webhooks, dynamically looks up the target asset, and orchestrates an instantaneous eviction policy using the Kubernetes API client.

```text
[ Attacker Injection ] 
         │
         ▼
 ┌───────────────┐
 │  Web App Pod  │ ──( Spawns /bin/bash System Call )
 └───────────────┘                   │
                                     ▼
                        ┌────────────────────────┐
                        │ Falco Agent Engine     │ (eBPF Kernel Probe)
                        └────────────────────────┘
                                     │
                        ( Ships JSON HTTP Alert Webhook )
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │ Custom SOAR Responder  │ (Telemetry Parsing Engine)
                        └────────────────────────┘
                                     │
                         ( Issues Eviction Request )
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │ Kubernetes API Server  │ ──( Evicts Compromised Pod )
                        └────────────────────────┘




https://github.com/user-attachments/assets/256d26dd-f402-4e74-bc1b-35837f0a68dd





