# Umbra farm (2026-09-12 07:50 ET)

Human: parallel P3–P8. Do not compile on live `:8086`.

| Role | Public | VPC | Plan | Assigned |
|---|---|---|---|---|
| umbra-orch | 207.246.126.149 | 10.20.0.3 | 1 GB | public `:8080` `/eval` `/eval3` `/print` `/audio` `/face` `/bid` |
| LIVE P2 | 64.176.200.124 | **10.20.0.5** | 16 GB | TinyS5 `umbra-choreo` `:8086`. P3 sidecar `:8087`. **Do not docker rm** |
| farm-a | 207.246.94.252 | **10.20.0.4** | 16 GB | OpenFHE try (`umbra-p3`). Idle compile |
| farm-fast | **45.32.5.249** | **10.20.0.6** | 32 GB / 8 CPU | **P5 DONE** print `:8082` **P7** face `:8084` **P8** bid `:8085` |
| farm-heavy | **104.156.226.53** | **10.20.0.7** | 32 GB / 8 CPU | **P6** audio `:8083` |

`UMBRA_WORKER_URL=http://207.246.126.149:8080`
SSH: `root@` + `~/.ssh/id_ed25519`. Env: `~/.umbra-vultr.env` (do not print, do not commit).
VPC `ba995955-e979-4a6e-bc06-76a100949f34`.
No `sk` / `client.zip` on any VM. No `docker build` without `</dev/null`. No `docker commit`.
P3 sidecar restart: `/root/start-p3-sidecar.sh` on the live worker (docker exec only).
