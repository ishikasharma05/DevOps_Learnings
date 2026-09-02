# Blue-Green Deployment on AWS EC2

A hands-on demonstration of the blue-green deployment strategy using two EC2 instances behind an Application Load Balancer (ALB), with zero-downtime traffic cutover between application versions.

## Overview

This project simulates a real-world blue-green deployment:

- **Blue instance** runs "Version 1" of the app
- **Green instance** runs "Version 2" of the app
- An **Application Load Balancer** sits in front of both, routing live traffic through target groups
- Switching the ALB listener's target group instantly cuts traffic from blue to green (or back) with **no downtime and no DNS changes**

## Architecture

```
                         ┌─────────────┐
                         │   Client    │
                         └──────┬──────┘
                                │
                         ┌──────▼──────┐
                         │     ALB     │
                         │ (Listener)  │
                         └──┬───────┬──┘
                            │       │
                    ┌───────▼──┐ ┌──▼───────┐
                    │ blue-tg  │ │ green-tg │
                    └───────┬──┘ └──┬───────┘
                            │       │
                    ┌───────▼──┐ ┌──▼───────┐
                    │  blue    │ │  green   │
                    │ instance │ │ instance │
                    │  (v1)    │ │  (v2)    │
                    └──────────┘ └──────────┘
```

## Prerequisites

- AWS account with EC2 and ELB permissions
- A key pair for SSH access
- Basic familiarity with the AWS EC2 console and SSH

## Tech Stack

- **AWS EC2** — Ubuntu Server 22.04 LTS, t2.micro
- **AWS Application Load Balancer (ALB)**
- **AWS Target Groups**
- **Apache2** — lightweight web server to serve each version

---

## Steps

### Part 1: Launch the Blue EC2 Instance

1. EC2 Console → **Launch Instance**
2. Name: `blue-instance`
3. AMI: **Ubuntu Server 22.04 LTS** (free tier eligible)
4. Instance type: `t2.micro`
5. Key pair: create or reuse one (e.g. `bluegreen-key.pem`)
6. Network settings:
   - Auto-assign public IP: **Enable**
   - Security group `bluegreen-sg`:
     - SSH (22) — Source: My IP
     - HTTP (80) — Source: Anywhere (0.0.0.0/0)
7. Launch and wait for "Running" + 2/2 status checks
8. Copy the public IPv4 address

### Set Up the App on Blue (Version 1)

```bash
chmod 400 bluegreen-key.pem
ssh -i bluegreen-key.pem ubuntu@<blue-public-ip>

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y apache2
sudo systemctl start apache2
sudo systemctl enable apache2
sudo systemctl status apache2
```

Edit `/var/www/html/index.html`:

```bash
sudo nano /var/www/html/index.html
```

```html
<html>
<head><title>Blue-Green Demo</title></head>
<body style="background-color:#cce5ff; text-align:center; padding-top:100px;">
  <h1>Version 1 - BLUE</h1>
  <p>Serving from blue-instance</p>
</body>
</html>
```

Test at `http://<blue-public-ip>` — confirm the blue page loads. Exit SSH.

### Part 2: Launch the Green EC2 Instance

Repeat the launch steps above, naming it `green-instance`, reusing the same key pair and security group.

```bash
ssh -i bluegreen-key.pem ubuntu@<green-public-ip>

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y apache2
sudo systemctl start apache2
sudo systemctl enable apache2
sudo systemctl status apache2
```

Edit `/var/www/html/index.html`:

```html
<html>
<head><title>Blue-Green Demo</title></head>
<body style="background-color:#d4edda; text-align:center; padding-top:100px;">
  <h1>Version 2 - GREEN</h1>
  <p>Serving from green-instance</p>
</body>
</html>
```

Test at `http://<green-public-ip>` — confirm the green page loads. Exit SSH.

### Part 3: Create Target Groups

1. EC2 Console → **Target Groups** → **Create target group**
2. **blue-tg**: Target type = Instances, Protocol = HTTP, Port = 80, Health check path = `/`, register `blue-instance`
3. **green-tg**: same settings, register `green-instance`

### Part 4: Create the Application Load Balancer

1. **Load Balancers** → **Create load balancer** → Application Load Balancer
2. Name: `bluegreen-alb`
3. Scheme: Internet-facing
4. Mappings: at least 2 Availability Zones
5. Security group: `bluegreen-sg`
6. Listener: HTTP:80 → default action forwards to `blue-tg`
7. Create, wait for "Active" state, copy the ALB DNS name

### Part 5: Test Baseline and Perform the Cutover

1. Open the ALB DNS name in a browser — should show **Version 1 - BLUE**
2. Go to **Load Balancers** → `bluegreen-alb` → **Listeners** → HTTP:80 → **Edit rules**
3. Change the default forward action from `blue-tg` to `green-tg` → Save
4. Hard refresh the ALB DNS URL — should now show **Version 2 - GREEN**, instantly, with no downtime

<img width="959" height="343" alt="image" src="https://github.com/user-attachments/assets/e7016175-7db3-4bab-89e5-f278babbd163" />


5. To confirm rollback works, switch the listener back to `blue-tg` and refresh — blue should return immediately

   <img width="567" height="218" alt="image" src="https://github.com/user-attachments/assets/42b1e2b0-84bb-4c66-97bd-0472574224c8" />

### Part 6: Cleanup

To avoid ongoing charges (the ALB is **not** free-tier free — ~$0.0225/hr):

1. Delete the Load Balancer
2. Delete both target groups (`blue-tg`, `green-tg`)
3. Terminate both EC2 instances
4. Remove the security group if not reused elsewhere

---

## Key Takeaway

Blue-green deployment allows instant, zero-downtime version switches and instant rollback — because the cutover happens at the load balancer's routing layer, not by redeploying or restarting anything. This makes it a safer alternative to in-place deployments where a bad release can cause extended downtime while you scramble to fix or redeploy.

## Notes

- Ubuntu AMIs use the `ubuntu` SSH user (not `ec2-user` like Amazon Linux)
- `ufw` (Ubuntu's firewall) is inactive by default on AWS AMIs — port access is controlled entirely by the EC2 security group
