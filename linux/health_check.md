Project Explanation

This Linux System Health Monitor script is used to check the overall health of a server. It monitors important system resources such as CPU usage, RAM usage, disk usage, and the status of critical services like Nginx and SSH. The goal is to quickly identify potential problems before they affect applications or users.

Why Check CPU Usage?

The CPU performs all processing tasks on a system. If CPU usage becomes too high, applications may slow down or become unresponsive. Monitoring CPU usage helps identify heavy workloads and performance issues.

Why Check RAM Usage?

RAM stores data that applications need while running. High memory usage can lead to slow performance, crashes, or excessive use of swap memory. Monitoring RAM helps ensure applications have enough resources to operate efficiently.

Why Check Disk Usage?

Disk space is required for storing files, logs, databases, and application data. If a disk becomes full, applications may fail to write data, causing service disruptions. Monitoring disk usage helps prevent storage-related issues.

Why Check Nginx and SSH Services?
Nginx is commonly used as a web server or reverse proxy. If it stops running, websites and APIs may become inaccessible.
SSH allows remote access to the server. If SSH is down, administrators may be unable to manage or troubleshoot the system remotely.
Importance for DevOps

Monitoring system resources is a fundamental DevOps responsibility. Before deploying applications or troubleshooting issues, engineers must know the health status of their servers. This script automates basic health checks, helping detect problems early and maintain system reliability. It also demonstrates key DevOps skills such as Linux administration, monitoring, automation, and Bash scripting.

#!/bin/bash

# ======================================
# Linux System Health Monitor
# ======================================

# Color Codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Thresholds
CPU_THRESHOLD=80
RAM_THRESHOLD=80
DISK_THRESHOLD=80

echo "======================================"
echo "      SYSTEM HEALTH REPORT"
echo "======================================"
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo

# --------------------------------------
# CPU Usage Check
# --------------------------------------
if command -v top >/dev/null 2>&1; then
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}')
    CPU_USAGE=${CPU_USAGE%.*}

    if [ "$CPU_USAGE" -gt "$CPU_THRESHOLD" ]; then
        echo -e "${RED}[WARNING] CPU Usage: ${CPU_USAGE}%${NC}"
    else
        echo -e "${GREEN}[OK] CPU Usage: ${CPU_USAGE}%${NC}"
    fi
else
    echo -e "${YELLOW}[INFO] top command not found${NC}"
fi

# --------------------------------------
# RAM Usage Check
# --------------------------------------
if command -v free >/dev/null 2>&1; then
    RAM_USAGE=$(free | awk '/Mem:/ {printf("%.0f"), $3/$2 * 100}')

    if [ "$RAM_USAGE" -gt "$RAM_THRESHOLD" ]; then
        echo -e "${RED}[WARNING] RAM Usage: ${RAM_USAGE}%${NC}"
    else
        echo -e "${GREEN}[OK] RAM Usage: ${RAM_USAGE}%${NC}"
    fi
else
    echo -e "${YELLOW}[INFO] free command not found${NC}"
fi

# --------------------------------------
# Disk Usage Check
# --------------------------------------
echo
echo "Disk Usage:"

if command -v df >/dev/null 2>&1; then
    df -hP | awk 'NR>1 {print $5, $6}' | while read usage mountpoint
    do
        percent=${usage%\%}

        if [ "$percent" -gt "$DISK_THRESHOLD" ]; then
            echo -e "${RED}[WARNING] $mountpoint : $usage used${NC}"
        else
            echo -e "${GREEN}[OK] $mountpoint : $usage used${NC}"
        fi
    done
else
    echo -e "${YELLOW}[INFO] df command not found${NC}"
fi

# --------------------------------------
# Service Check Function
# --------------------------------------
check_service() {
    SERVICE=$1

    if ! command -v systemctl >/dev/null 2>&1; then
        echo -e "${YELLOW}[INFO] systemctl not available${NC}"
        return
    fi

    if systemctl list-unit-files | grep -q "^${SERVICE}"; then
        if systemctl is-active --quiet "$SERVICE"; then
            echo -e "${GREEN}[OK] Service '$SERVICE' is running${NC}"
        else
            echo -e "${RED}[WARNING] Service '$SERVICE' is NOT running${NC}"
        fi
    else
        echo -e "${YELLOW}[INFO] Service '$SERVICE' not installed${NC}"
    fi
}

# --------------------------------------
# Service Checks
# --------------------------------------
echo
echo "Service Status:"

check_service nginx
check_service ssh

echo
echo "======================================"
echo "      HEALTH CHECK COMPLETED"
echo "======================================"


<img width="436" height="394" alt="image" src="https://github.com/user-attachments/assets/34525ba8-0e8a-453e-823c-e83a1edc32f0" />

