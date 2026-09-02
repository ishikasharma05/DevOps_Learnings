# 🐧 Linux — Networking & Shell Scripting Commands

A hands-on reference for every networking and scripting command I've practiced.
Each section covers what the command does, why it matters in DevOps, and real examples I've run.

---

## 📡 Networking Commands

---

### `netstat` — Network Statistics

**What it does:**
Shows all active network connections, listening ports, and the programs using them.

**Why it matters in DevOps:**
When a service isn't reachable, the first thing you check is whether it's actually listening on the right port. `netstat` tells you that instantly.

**Install it first (not pre-installed on Ubuntu 24):**
```bash
sudo apt install net-tools
```

<img width="1452" height="375" alt="Screenshot 2026-06-09 151131" src="https://github.com/user-attachments/assets/456d64df-5fac-4400-8977-b75251ff640c" />

<img width="1827" height="61" alt="Screenshot 2026-06-09 151157" src="https://github.com/user-attachments/assets/9646fa74-87f5-4a26-840d-0d88a0f49279" />


**Flags used:**
| Flag | What it does |
|------|--------------|
| `-t` | Show TCP connections |
| `-u` | Show UDP connections |
| `-l` | Show only listening ports |
| `-n` | Show IP addresses instead of hostnames (faster) |
| `-p` | Show the PID and program name using the port |

**Commands I ran:**

```bash
# Without sudo — works but hides PID/program names
netstat -tulnp

<img width="1424" height="114" alt="Screenshot 2026-06-09 151248" src="https://github.com/user-attachments/assets/e53e3904-a262-4128-8771-24034fac0386" />


# With sudo — shows full output including which program owns each port
sudo netstat -tulnp
```

**Output I got (with sudo):**
```
Proto  Local Address     State    PID/Program name
tcp    0.0.0.0:80        LISTEN   1358/nginx: master
tcp    0.0.0.0:22        LISTEN   1/systemd
tcp    127.0.0.53:53     LISTEN   800/systemd-resolve
udp    127.0.0.1:323              1156/chronyd
```

**What this output means:**
- Port `80` → nginx is running and accepting HTTP traffic on all interfaces
- Port `22` → SSH is open (managed by systemd)
- Port `53` → DNS resolver is running locally (systemd-resolved)
- Port `323` → chronyd is handling time synchronisation (NTP)

**Key lesson:**
Running without `sudo` gives you `(No info could be read for "-p": geteuid()=1000 but you should be root.)` — you see the ports but not which program owns them. Always use `sudo` when you need the full picture.

---

### `dig` — DNS Lookup Tool

**What it does:**
Queries DNS servers and shows you exactly what records are returned — A records, MX records, TTL values, and which DNS server answered.

**Why it matters in DevOps:**
When a deployment fails because a domain isn't resolving, or you need to verify DNS propagation after a config change, `dig` is the tool. It gives you the raw DNS response — no guesswork.

**Commands I ran:**

```bash
# Quick answer only — just the IPs
dig google.com +short

<img width="590" height="195" alt="Screenshot 2026-06-09 151306" src="https://github.com/user-attachments/assets/9d313987-7f9d-4472-9ae7-5d44086e6856" />

# Full detailed output
dig google.com

# Query MX records (mail server records)
dig google.com MX
```

**Output breakdown — `dig google.com`:**
```
;; ANSWER SECTION:
google.com.    6    IN    A    192.178.193.113
google.com.    6    IN    A    192.178.193.102
```

<img width="977" height="347" alt="Screenshot 2026-06-09 151317" src="https://github.com/user-attachments/assets/f0ee35cf-2f98-47e8-bdd6-364b4a3d258a" />


| Field | What it means |
|-------|---------------|
| `google.com.` | The domain queried |
| `6` | TTL in seconds — how long this record is cached |
| `IN` | Internet class (always IN for standard queries) |
| `A` | Record type — A means IPv4 address |
| `192.178.x.x` | The actual IP address returned |

**Output breakdown — `dig google.com MX`:**
```
;; ANSWER SECTION:
google.com.    300    IN    MX    10 smtp.google.com.
```

- `MX` = Mail Exchange record — points to the mail server for this domain
- `10` = Priority (lower number = higher priority)
- `smtp.google.com.` = The actual mail server hostname

<img width="1007" height="574" alt="Screenshot 2026-06-09 151330" src="https://github.com/user-attachments/assets/4aea00a9-a5f0-43cd-a0a1-d734a49fba4c" />


**DNS server that answered:**
```
;; SERVER: 127.0.0.53#53(127.0.0.53)
```
This is `systemd-resolved` — Ubuntu's local DNS resolver running on the loopback interface.

**Useful `dig` flags:**
```bash
dig google.com +short          # IPs only, no extra output
dig google.com MX              # Mail server records
dig google.com NS              # Name server records
dig google.com @8.8.8.8        # Query Google's DNS directly instead of local resolver
dig -x 192.178.193.100         # Reverse lookup — IP to hostname
```

---

### `curl` — Transfer Data from URLs

**What it does:**
Sends HTTP (and other protocol) requests from the command line and shows the response. Think of it as a browser, but for the terminal.

**Why it matters in DevOps:**
- Test if a web server is actually responding
- Hit API endpoints to check health or test payloads
- Download files in scripts without a browser
- Debug headers, redirects, response codes
- It's in almost every deployment script and CI/CD pipeline

**Install it (if not present):**
```bash
sudo apt install curl
```

**Basic usage:**
```bash
# Fetch the response body of a URL
curl http://localhost

# Fetch a public URL
curl https://example.com
```

**Essential flags:**
| Flag | What it does |
|------|--------------|
| `-I` | Fetch headers only (no body) |
| `-v` | Verbose — shows full request + response headers |
| `-o filename` | Save output to a file |
| `-L` | Follow redirects automatically |
| `-s` | Silent mode — suppress progress output |
| `-w "%{http_code}"` | Print only the HTTP status code |
| `-X POST` | Change request method |
| `-H "Header: value"` | Add a custom header |
| `-d "data"` | Send data in the request body |

**Commands to practice:**

```bash
# Check if nginx is responding on localhost
curl http://localhost

# See only the HTTP headers (check status code, server type, content-type)
curl -I http://localhost

# Verbose output — full request and response including TLS handshake
curl -v https://example.com

# Follow redirects (e.g. http → https redirect)
curl -L http://example.com

# Just print the HTTP status code — useful in scripts
curl -s -o /dev/null -w "%{http_code}" http://localhost

# Download a file and save it
curl -o myfile.html https://example.com

# Test a JSON API endpoint
curl -s https://api.github.com/users/ishikasharma05

# Send a POST request with JSON data
curl -X POST -H "Content-Type: application/json" \
  -d '{"name": "test"}' \
  http://localhost/api/endpoint
```

**Real DevOps use case — health check in a script:**
```bash
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)

if [ "$STATUS" -eq 200 ]; then
    echo "Service is up. Status: $STATUS"
else
    echo "Service is DOWN. Status: $STATUS"
fi
```

**Difference between `curl` and `wget`:**
| | `curl` | `wget` |
|--|--------|--------|
| Primary use | API calls, testing, scripting | Downloading files |
| Supports multiple protocols | Yes (HTTP, FTP, SMTP, etc.) | Mostly HTTP/FTP |
| Output by default | Prints to terminal | Saves to file |
| In DevOps | Health checks, API testing | Downloading binaries, packages |

---

## 🐚 Shell Scripting

---

### Variables in Shell Scripts

**What they are:**
Named storage for values you want to reuse across your script — environment names, port numbers, paths, etc.

**Script I wrote — `variabletry.sh`:**
```bash
#!/bin/bash

ENV="Production"
PORT=8080

echo "Deploying to $ENV on port $PORT"
echo "script worked successfully"
```

**Run it:**
```bash
chmod u+x variabletry.sh
./variabletry.sh
```

**Output:**
```
Deploying to Production on port 8080
script worked successfully
```

**Rules for variables:**
```bash
NAME="Ishika"        # No spaces around = sign
echo $NAME           # Access with $ prefix
echo "${NAME}_log"   # Use {} to avoid ambiguity with adjacent text
readonly PI=3.14     # Constant — cannot be changed after this line
unset NAME           # Delete a variable
```

**Special built-in variables:**
| Variable | What it holds |
|----------|---------------|
| `$0` | Name of the script itself |
| `$1`, `$2` | First, second argument passed to script |
| `$#` | Number of arguments passed |
| `$?` | Exit code of the last command (0 = success) |
| `$$` | PID of the current script |
| `$@` | All arguments passed |

---

### Conditional Statements (`if/elif/else`)

**What they do:**
Make decisions in your script based on conditions — service running or not, file exists or not, exit code success or failure.

**Script I wrote — `condition.sh`:**
```bash
#!/bin/bash

SERVICE="nginx"

if systemctl is-active --quiet $SERVICE; then
    echo "$SERVICE is running perfectly."
else
    echo "$SERVICE is NOT running."
fi
```

**Output:**
```
nginx is running perfectly.
```

**Syntax rules (the mistake I made and fixed):**
```bash
# WRONG — missing fi, causes "unexpected end of file" error
if [ condition ]; then
    echo "something"

# CORRECT — every if must close with fi
if [ condition ]; then
    echo "something"
fi
```

**Common conditions:**
```bash
# String comparisons
if [ "$VAR" = "value" ]; then      # string equals
if [ "$VAR" != "value" ]; then     # string not equals
if [ -z "$VAR" ]; then             # string is empty
if [ -n "$VAR" ]; then             # string is not empty

# Number comparisons
if [ $NUM -eq 10 ]; then           # equal
if [ $NUM -ne 10 ]; then           # not equal
if [ $NUM -gt 5 ]; then            # greater than
if [ $NUM -lt 5 ]; then            # less than

# File checks
if [ -f "/path/to/file" ]; then    # file exists
if [ -d "/path/to/dir" ]; then     # directory exists
if [ -x "/path/to/file" ]; then    # file is executable

# Command success check
if systemctl is-active --quiet nginx; then   # exits 0 if service is active
```

**Full if/elif/else example:**
```bash
#!/bin/bash

PORT=$1   # take port number as argument

if [ -z "$PORT" ]; then
    echo "Usage: $0 <port>"
    exit 1
elif [ "$PORT" -eq 80 ]; then
    echo "Port 80 — HTTP traffic"
elif [ "$PORT" -eq 22 ]; then
    echo "Port 22 — SSH"
else
    echo "Port $PORT — checking..."
    sudo netstat -tulnp | grep ":$PORT"
fi
```

<img width="1291" height="516" alt="Screenshot 2026-06-09 151345" src="https://github.com/user-attachments/assets/c2a71314-4037-4ec5-ba2c-f0082c316449" />


---

## 🔑 Key Concepts Learned

| Concept | What I understood |
|---------|-------------------|
| `sudo` vs normal user | Some commands need root. Without sudo, netstat hides PIDs. |
| TTL in DNS | How long a DNS record is cached. Short TTL = changes propagate faster. |
| Ports | Each service listens on a specific port. 80=HTTP, 22=SSH, 53=DNS. |
| Exit codes | Every command returns 0 (success) or non-zero (failure). Scripts use this for decisions. |
| `chmod u+x` | Makes a script executable for the owner before you can run it with `./` |
| Syntax errors | Shell scripts fail at the first syntax error. Always check with `bash -n script.sh` before running. |

---

## ✅ Commands Quick Reference

```bash
# Networking
sudo netstat -tulnp              # All listening ports with program names
dig domain.com                   # Full DNS lookup
dig domain.com +short            # Just the IPs
dig domain.com MX                # Mail server records
dig domain.com @8.8.8.8          # Query specific DNS server
curl http://localhost             # Test if web server responds
curl -I http://localhost          # Headers only
curl -s -o /dev/null -w "%{http_code}" http://localhost   # Just the status code
curl -v https://example.com      # Verbose with headers

# Shell scripting
chmod u+x script.sh              # Make script executable
./script.sh                      # Run script
bash -n script.sh                # Check for syntax errors without running
bash -x script.sh                # Debug mode — prints each command as it runs
```

---

*Part of my DevOps learning journey — [DevOps_Learnings](https://github.com/ishikasharma05/DevOps_Learnings)*
