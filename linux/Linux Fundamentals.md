# 🐧 Linux Fundamentals — Self-Study Notes

> **Goal:** DevOps-ready Linux skills from scratch  
> **Status:** In Progress  
> **Started:** June 2025

---

## ✅ Topics Completed

| # | Topic | Status |
|---|-------|--------|
| 1 | Navigation Commands | ✅ Done |
| 2 | File Operations | ✅ Done |
| 3 | File Searching & Text Processing | ✅ Done |
| 4 | Permissions (chmod, chown, chgrp) | ✅ Done |
| 5 | Process Management | ✅ Done |
| 6 | Disk & Memory Monitoring | ✅ Done |
| 7 | User Management | ✅ Done |
| 8 | Package Management (apt) | ⬜ Pending |
| 9 | Networking | ⬜ Pending |
| 10 | Services (systemctl, journalctl) | ⬜ Pending |
| 11 | Bash Scripting | ⬜ Pending |

---

## 📁 Topic 1 — Navigation Commands

```bash
pwd          # Print current directory
ls           # List files
ls -la       # List with hidden files and details
cd folder    # Change directory
cd ..        # Go one level up
cd ~         # Go to home directory
```

---

## 📁 Topic 2 — File Operations

```bash
touch file.txt            # Create empty file
mkdir folder              # Create directory
cp file.txt backup.txt    # Copy file
mv file.txt /tmp/         # Move file
rm file.txt               # Delete file
rm -rf folder/            # Delete folder recursively
cat file.txt              # View file content
nano file.txt             # Edit file
```

---

## 🔍 Topic 3 — File Searching & Text Processing

```bash
find / -name "file.txt"       # Find file by name
grep "error" app.log          # Search text in file
grep -r "error" /var/logs/    # Search recursively
grep -i "error" file.txt      # Case-insensitive search
wc -l file.txt                # Count lines
sort file.txt                 # Sort output
uniq file.txt                 # Remove duplicate lines
cut -d: -f1 /etc/passwd       # Extract field from file
pipe  |                       # Pass output to next command
```

---

## 🔐 Topic 4 — Permissions (chmod, chown, chgrp)

### Permission Structure
```
-rwxr-xr-- 1 ishika developers 500 Jun 4 app.sh
 ^^^        → Owner permissions  (rwx)
    ^^^     → Group permissions  (r-x)
       ^^^  → Others permissions (r--)
```

### chmod — Change Permissions
```bash
chmod 755 app.sh          # rwxr-xr-x
chmod 644 file.txt        # rw-r--r--
chmod +x script.sh        # Add execute permission
chmod -w file.txt         # Remove write permission
```

### chown — Change Owner
```bash
sudo chown ishika file.txt              # Change owner
sudo chown ishika:developers file.txt   # Change owner and group
sudo chown -R ishika:developers project/ # Recursive
```

### chgrp — Change Group
```bash
sudo chgrp developers file.txt    # Change group only
```

### Quick Reference
| Command | Changes |
|---------|---------|
| `chmod` | Permissions |
| `chown` | Owner |
| `chgrp` | Group |

---

## ⚙️ Topic 5 — Process Management

### What is a Process?
Every running program is a process. Each process has a unique **PID (Process ID)**.

```bash
ps              # Show processes in current terminal
ps aux          # Detailed list of all processes
top             # Live process monitor
htop            # Better live monitor (install: sudo apt install htop)
pgrep nginx     # Find PID by name
```

### Killing Processes
```bash
kill 1050        # Graceful stop (signal 15)
kill -9 1050     # Force stop (use when graceful fails)
killall chrome   # Kill all processes with that name
```

### Background Jobs
```bash
python app.py &   # Run in background
jobs              # Show background jobs
```

### Signals Reference
| Signal | Meaning |
|--------|---------|
| 15 | Graceful stop |
| 9 | Force kill |
| 1 | Reload config |
| 2 | Interrupt (Ctrl+C) |

---

## 💾 Topic 6 — Disk & Memory Monitoring

### df — Disk Filesystem
Check disk usage of all mounted filesystems.
```bash
df -h        # Human readable (G/M instead of raw bytes)
```

Example output:
```
Filesystem      Size  Used Avail Use%
/dev/sda1        50G   25G   22G  54%
```

| Field | Meaning |
|-------|---------|
| Size | Total disk size |
| Used | Used storage |
| Avail | Free storage |
| Use% | Percentage used |

### du — Disk Usage
Find which files/folders are consuming storage.
```bash
du -sh Downloads    # Size of a specific folder
du -sh *            # Size of every item in current directory
du -sh ~            # Size of your home directory
```

### free — RAM Usage
```bash
free -h             # RAM usage (human readable)
```

Example output:
```
Mem:  8Gi  4Gi  2Gi
```

| Field | Meaning |
|-------|---------|
| Total | Total RAM |
| Used | Currently used |
| Free | Available RAM |

### Other Monitoring Commands
```bash
uptime              # How long server has been running + load average
uname -a            # OS and kernel version
hostname            # Machine name (useful when managing multiple servers)
```

### Real Scenario — Disk Full
```bash
df -h        # Step 1: Find which partition is at 95%+
du -sh *     # Step 2: Find which folder is the culprit
# Example: 20G Logs → delete or archive old logs
```

---

## 👤 Topic 7 — User Management

### Why It Exists
Linux is a multi-user OS. Not everyone should have access to everything.
```
Ishika → Developer
Rahul  → DevOps Engineer
Amit   → Tester
```
Users + Groups + Permissions = controlled access.

### Checking Current User
```bash
whoami           # Who am I?
id               # Full details: UID, GID, all groups
groups           # All groups current user belongs to
groups rahul     # Groups of a specific user
```

Example `id` output:
```
uid=1000(ishika) gid=1000(ishika) groups=1000(ishika),27(sudo)
```

### Creating Users
```bash
sudo adduser rahul       # Interactive — asks for password, name, etc. (recommended)
sudo useradd rahul       # Basic — no prompts
sudo passwd rahul        # Set or change a user's password
```

### Modifying Users
```bash
sudo usermod -aG docker ishika       # Add ishika to docker group
sudo usermod -aG developers rahul    # Add rahul to developers group
# -a = append, -G = group (never drop -a or it removes other groups)
```

**Real DevOps use:** After adding user to `docker` group, they can run `docker ps` without `sudo` (re-login required).

### Deleting Users
```bash
sudo userdel rahul          # Delete user account only
sudo userdel -r rahul       # Delete user + home directory
```

### Managing Groups
```bash
sudo groupadd developers         # Create a new group
getent group developers          # Verify group exists
```

### Real Team Example
```bash
sudo groupadd projectteam
sudo usermod -aG projectteam ishika
sudo usermod -aG projectteam rahul
sudo usermod -aG projectteam amit
# Now all project files under group=projectteam are shared
```

### Important System Files
```bash
cat /etc/passwd    # All users on the system
cat /etc/group     # All groups on the system
# Know these exist — don't edit them manually
```

### Quick Reference
| Command | Purpose |
|---------|---------|
| `whoami` | Current user |
| `id` | UID, GID, groups |
| `groups` | User's groups |
| `adduser` | Create user (interactive) |
| `useradd` | Create user (basic) |
| `passwd` | Set password |
| `usermod -aG` | Add user to group |
| `groupadd` | Create group |
| `userdel` | Delete user |
| `userdel -r` | Delete user + home |

---

## 🌐 Topic 8 — Networking (ss)

### ss — Socket Statistics (modern replacement for netstat)

```bash
ss -tuln        # Show all listening TCP/UDP ports (no DNS resolution)
ss -tulnp       # Same + show process name and PID
ss -t           # Show only TCP connections
ss -u           # Show only UDP connections
ss -l           # Show only listening sockets
ss -s           # Summary of socket statistics
ss -p           # Show process using each socket
```

### Flag Reference
| Flag | Meaning |
|------|---------|
| `-t` | TCP sockets |
| `-u` | UDP sockets |
| `-l` | Listening only |
| `-n` | No DNS resolution (faster) |
| `-p` | Show process/PID |

### Common Usage
```bash
# Check if a specific port is in use
ss -tuln | grep :80
ss -tuln | grep :3000

# Check which process is using port 8080
ss -tulnp | grep :8080

# View all established connections
ss -t state established
```

### Real DevOps Scenario
```bash
# Is Nginx actually listening on port 80?
ss -tuln | grep :80

# Which app is holding port 3000? (common Node.js conflict)
ss -tulnp | grep :3000
```

---

## ⬜ Upcoming Topics

### Package Management (apt)
```bash
# Coming soon
sudo apt update
sudo apt install nginx
sudo apt remove nginx
sudo apt upgrade
```

### Services (systemctl)
```bash
# Coming soon
sudo systemctl start nginx
sudo systemctl status nginx
sudo systemctl enable nginx
journalctl -u nginx
```

### Bash Scripting
```bash
# Coming soon
#!/bin/bash
variables, loops, conditionals, functions
```

---

## 🧠 DevOps Context — Why These Commands Matter

| Command | Real-World Use Case |
|---------|-------------------|
| `ps aux / top` | Server is slow → find the heavy process |
| `df -h` | Deployment fails → disk is full |
| `free -h` | App crashes → check if RAM is exhausted |
| `chown -R` | App can't write logs → fix ownership |
| `usermod -aG docker` | Developer can't run Docker without sudo |
| `ss -tulnp` | Port conflict → find which app is blocking |
| `kill -9` | Zombie process won't stop → force terminate |

---


<img width="1654" height="85" alt="Screenshot 2026-06-04 113454" src="https://github.com/user-attachments/assets/40f7f48e-7537-4574-8a78-ba60337d6a29" 
 

 <img width="1511" height="114" alt="Screenshot 2026-06-04 113513" src="https://github.com/user-attachments/assets/66e52467-7537-4cbe-8f9e-19801ef2f479" />


 <img width="652" height="120" alt="Screenshot 2026-06-04 114849" src="https://github.com/user-attachments/assets/8f10793e-fb11-4970-a289-4bcc5f5c05ad" />


 <img width="1905" height="255" alt="Screenshot 2026-06-04 122220" src="https://github.com/user-attachments/assets/dd566419-e664-4b53-8769-56d185874880" />


<img width="1548" height="405" alt="Screenshot 2026-06-04 122257" src="https://github.com/user-attachments/assets/58fbfbb8-3475-4448-8e44-427f23db81af" />
 

<img width="1878" height="522" alt="Screenshot 2026-06-04 122409" src="https://github.com/user-attachments/assets/f4475b59-dab3-4c30-baee-6640fa4e9939" />


 <img width="1182" height="314" alt="Screenshot 2026-06-04 191449" src="https://github.com/user-attachments/assets/f989926d-1d35-4eee-869a-b32ec9ba090f" />



 <img width="646" height="147" alt="Screenshot 2026-06-04 191500" src="https://github.com/user-attachments/assets/a6363641-b4ae-4115-a2c9-996059131c95" />


<img width="1148" height="123" alt="Screenshot 2026-06-04 191516" src="https://github.com/user-attachments/assets/0a49346c-8f08-4b4b-86ec-86b5584e017f" />



<img width="902" height="59" alt="Screenshot 2026-06-04 191556" src="https://github.com/user-attachments/assets/094b6b9c-cfa1-45d0-8ce7-24bebc965815" />


<img width="684" height="63" alt="Screenshot 2026-06-04 192231" src="https://github.com/user-attachments/assets/a4e0e1dd-b22b-4983-a434-7408a3974d33" />


<img width="936" height="617" alt="Screenshot 2026-06-04 200607" src="https://github.com/user-attachments/assets/f5689e42-6376-4d57-9232-c3bb0385e8ee" />


 />


*Notes maintained by Ishika | B.Sc. IT, SK College Navi Mumbai*
