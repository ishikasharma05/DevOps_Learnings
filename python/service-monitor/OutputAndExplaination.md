<img width="360" height="43" alt="image" src="https://github.com/user-attachments/assets/64bf7ca7-ef8a-44f8-8bc1-d642290499fd" />


**Output breakdown:**

| Prefix    | Meaning                                              |
|-----------|------------------------------------------------------|
| `[OK]`    | Service is active and running normally               |
| `[FAIL]`  | Service is not running — needs attention             |
| `[ERROR]` | Script could not check the service (permissions, typo in name, etc.) |

The `status:` part in `[FAIL]` lines tells you *why* it failed:
- `inactive` — service was stopped cleanly (manually or on boot)
- `failed` — service crashed or exited with an error
- `activating` — service is still starting up

---

## Exit Codes

The script returns an exit code when it finishes.  
This matters when you run it inside automation, cron jobs, or CI pipelines.

```bash
python3 service_monitor.py
echo $?   # prints the exit code
```

| Exit Code | Meaning                          |
|-----------|----------------------------------|
| `0`       | All services are active          |
| `1`       | One or more services are down    |

---

## How to Monitor Different Services

Open `service_monitor.py` and edit this line:

```python
SERVICES = ["ssh", "nginx"]
```

Replace or add any service name you want:

```python
SERVICES = ["ssh", "nginx", "docker", "ufw", "cron"]
```

Service names must match exactly what `systemctl` uses on your system.  
To verify a service name:

```bash
systemctl list-units --type=service
```

---

## Concepts This Script Covers

| Concept | What It Does Here |
|---|---|
| `subprocess.run()` | Runs a shell command from inside Python |
| `systemctl is-active` | Asks the OS if a service is running |
| Exit codes (`sys.exit`) | Signals success or failure to the outside world |
| Functions | `check_service()` isolates the logic cleanly |
| Error handling | Catches unexpected failures without crashing |
| `if __name__ == "__main__"` | Ensures script only runs when called directly, not when imported |
