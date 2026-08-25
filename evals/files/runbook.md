## Recover the worker

1. Confirm `worker-03` is absent from the active queue.
2. Run `systemctl status atlas-worker@03`.
3. If the unit is inactive, run `systemctl start atlas-worker@03`.
4. Validate with `curl -fsS http://127.0.0.1:8083/health`.

Expected output: `{"status":"ok","worker":"03"}`

Do not restart the host. Escalate after two failed service starts.
