# P3 compile fail (paused 2026-09-12 07:12 ET)

`docker logs umbra-compile` last lines:

```
cleartext mismatch after 25000 steps
```

Container `umbra-compile` Exited (1). ChoreoP3 MLP (Linear 75→128→10 + card Linear 5→10) did not exact-fit fixtures in 25000 Adam steps.
