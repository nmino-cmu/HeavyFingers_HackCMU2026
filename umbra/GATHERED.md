# Umbra Vultr (2026-09-12)

No secrets. API key is in `umbra/.env` (gitignored) and `~/.umbra-vultr.env`.

| Role | Public IPv4 | VPC | Plan |
|---|---|---|---|
| umbra-orch | 207.246.126.149 | 10.20.0.3 | vc2-1c-1gb ewr |
| umbra-worker | 64.176.200.124 | 10.20.0.5 | **vc2-6c-16gb** ewr |

- VPC `ba995955-e979-4a6e-bc06-76a100949f34` `10.20.0.0/24` ewr
- Worker instance `7a87afed-f469-422a-a61d-8c6dfd55c247`
- Orch instance `2b27cd4c-24aa-475a-8a8f-97ca7c9f3cca`
- `UMBRA_WORKER_URL=http://207.246.126.149:8080`
- Old 1 GB worker `0e61feaf-…` was stuck locked after a failed in-place upgrade; left for later delete when unlocked
- Docker + `/opt/umbra` + ufw (22 + VPC) on the 16 GB box; `free -m` Mem total 15982
- VPC ping orch → 10.20.0.5 ok
- 2026-09-12 07:26: old worker `0e61feaf` `207.246.94.252` / `10.20.0.4` is 16 GB idle — farm-a (not live P2)
- farm-fast `d666350a` `45.32.5.249` / `10.20.0.6` vc2-8c-32gb (P5)
- farm-heavy `ebad155c` `104.156.226.53` / `10.20.0.7` vc2-8c-32gb (P6)
- Parallel P3–P8. Live P2 stays `10.20.0.5`. See `umbra/FARM.md`
