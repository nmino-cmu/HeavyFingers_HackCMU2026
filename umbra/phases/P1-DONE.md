# P1-DONE

- `python3 umbra/test_vpc.py` CHECKS_RUN=10
- orch systemd `umbra-orch` on 0.0.0.0:8080, machine-id match
- stub systemd `umbra-stub` on 10.20.0.5:8081 only
- Mac cannot open worker public :8081
- nonce echoed; stub echoes 200kB blob; no 0.9137 in body
- EVAL_HOST=vultr (echo stub, not FHE yet)
