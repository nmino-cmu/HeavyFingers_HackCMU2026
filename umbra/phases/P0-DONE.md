# P0-DONE

- Worker plan `vc2-6c-16gb`, `free -m` total 15982 on `64.176.200.124` / VPC `10.20.0.5`
- Orch still `207.246.126.149` / `10.20.0.3`; ufw 22, 8080, `10.20.0.0/24`
- Worker ufw: 22 + `10.20.0.0/24` only
- VPC ping orch → 10.20.0.5 0% loss
- `UMBRA_WORKER_URL=http://207.246.126.149:8080`
- Old 1 GB instance still locked; not used
