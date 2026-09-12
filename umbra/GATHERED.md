# Umbra Vultr smoke (2026-09-12)

No secrets in this file. API key lives in `umbra/.env` (gitignored) and `~/.umbra-vultr.env`.

| Role | Public IPv4 | VPC | Plan | Notes |
|---|---|---|---|---|
| umbra-orch | 207.246.126.149 | 10.20.0.3 | vc2-1c-1gb ewr | public :8080 |
| umbra-worker | 207.246.94.252 | 10.20.0.4 | vc2-1c-1gb ewr | SSH only; FHE on VPC :8081 |

- VPC `umbra-vpc` `10.20.0.0/24` id `ba995955-e979-4a6e-bc06-76a100949f34` region ewr
- `UMBRA_WORKER_URL=http://207.246.126.149:8080`
- Orch machine-id `ffa79e01ec0c428793ec83f6353dc016`
- Worker machine-id `4a7203905c954d08b526760b99c9b441`
- Docker + `/opt/umbra` on both
- Smoke proved: SSH both, `docker run hello-world` both, VPC ping both ways, orch public HTTP, FHE HTTP only on `10.20.0.4:8081`, Mac cannot hit worker :8080/:8081

These are **1 GB smoke boxes**, not the 16 GB FHE worker. Resize/rebuild `umbra-worker` to `vc2-6c-16gb` before Concrete compile. Keep orch at 1 GB.
