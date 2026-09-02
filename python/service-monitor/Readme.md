# Service Monitor

A Python script that automatically checks the running status of system services — instead of manually running `systemctl status <service>` one by one.

---

## The Problem It Solves

On a Linux server, services like `ssh` or `nginx` can stop unexpectedly.  
Normally you would check each one manually:

```bash
systemctl status ssh
systemctl status nginx
```

If you have 5–10 services, that becomes repetitive and error-prone.  
This script checks all of them in one run and tells you exactly what is running and what is not.

---

## How It Works

1. A list of services is defined inside the script (`SERVICES`)
2. For each service, it runs `systemctl is-active <service>` behind the scenes
3. It reads the response — either `active`, `inactive`, or `failed`
4. It prints a clear status line for each service
5. It exits with code `0` if everything is fine, or `1` if something is down

---

## Requirements

- Linux system with `systemd` (Ubuntu, Debian, CentOS, etc.)
- Python 3.x (check with `python3 --version`)
- The services you want to monitor must be installed on the system

---

## How to Run

**Step 1 — Clone or navigate to the repo**
```bash
cd DevOps_Learnings/bash-scripting/service-monitor/
```

**Step 2 — Give execute permission (first time only)**
```bash
chmod +x service_monitor.py
```

**Step 3 — Run the script**
```bash
python3 service_monitor.py
```

---

## Output and What It Means

### When all services are running:
