# Hosting My Portfolio on AWS EC2

As part of my AWS learning journey (IAM, EC2, S3, MFA, VPC), I also deployed my portfolio website on an **EC2 instance** running **Amazon Linux**, using **Apache (httpd)** as the web server, instead of using S3's static hosting feature. This was done specifically to understand server provisioning, security groups, and manual deployment — concepts that don't come up at all with S3 hosting.

> **Note on when to actually use this:** For a purely static site (HTML/CSS/JS, no backend), S3 static hosting is simpler, cheaper (near-zero cost), and requires no server maintenance. EC2 makes sense when you need a real server — custom backend logic, server-side processing, or just to learn how servers work. I did this primarily for the second reason: to understand EC2, not because it's the better choice for a static portfolio.

---

## 1. What is EC2?

Amazon EC2 (Elastic Compute Cloud) gives you a virtual server ("instance") in the cloud that you fully control — you choose the OS, install your own software, configure networking, and manage it like you would a physical machine. Unlike S3 hosting, EC2 requires you to set up and run an actual web server yourself.

---

## 2. Steps I Followed

### Step 1: Launch an EC2 Instance
1. Went to **EC2 → Launch Instance**.
2. Chose an Amazon Machine Image (AMI) — **Amazon Linux 2023**.
3. Selected an instance type — **t2.micro** (free-tier eligible), suitable for a low-traffic portfolio site.
4. Created a new **key pair** (`.pem` file) for SSH access, or selected an existing one.
   - Downloaded and saved the `.pem` file securely — this is the only way to SSH in later, and AWS won't let you re-download it.
5. Configured the **Security Group** (acts as a virtual firewall) to allow:
   - **SSH (port 22)** — restricted to my IP, for secure terminal access
   - **HTTP (port 80)** — open to all (`0.0.0.0/0`), so visitors can reach the site
   - **HTTPS (port 443)** — open to all, if planning to set up SSL later
6. Launched the instance.

📸 <img width="790" height="137" alt="Screenshot 2026-06-23 130747" src="https://github.com/user-attachments/assets/e21092aa-9bff-4723-881e-36b6dcd67ffe" />


### Step 2: Connect to the Instance

My key file was named `my-portfolio-key.pem`, saved in my Windows `Downloads` folder. A few early attempts failed before the connection worked — worth keeping in the doc since it's a common real-world snag:

```bash
ssh -i my-portfolio-key.pem ec2-user@35.154.165.61
```
→ Failed: `Identity file my-portfolio-key.pem not accessible` (run from a folder that didn't contain the key).

```bash
ssh -i "%USERPROFILE%\Downloads\portfolio-key.pem" ec2-user@35.154.165.61
```
→ Failed: wrong filename — the key was `my-portfolio-key.pem`, not `portfolio-key.pem`.

```bash
ssh -i "path-to-key.pem" ubuntu@35.154.165.61
```
→ Failed: placeholder filename used by mistake, plus wrong username (`ubuntu` is for Ubuntu AMIs, not Amazon Linux).

**What finally worked** — running the command from inside the `Downloads` folder where the key actually lived, with the correct filename and username:
```bash
cd %USERPROFILE%\Downloads
ssh -i my-portfolio-key.pem ec2-user@35.154.165.61
```
This connected successfully and accepted the host's fingerprint on first connect (normal — SSH always asks this the first time you connect to a new server).

📸 <img width="555" height="157" alt="image" src="https://github.com/user-attachments/assets/6726e051-0a9b-4773-b3fc-744d4d749d36" />


**Lesson learned:** SSH key errors are almost always about the *path* — either you're not in the folder containing the `.pem` file, or you typed the wrong filename. The error message always tells you exactly which file it couldn't find.

### Step 3: Update the Server

First tried the Ubuntu-style command out of habit — it failed immediately, which is expected on this OS:
```bash
sudo apt update
```
```
sudo: apt: command not found
```

Switched to the correct command for Amazon Linux:
```bash
sudo dnf update -y
```
Output:
```
Amazon Linux 2023 Kernel Livepatch repository    434 kB/s | 55 kB  00:00
Dependencies resolved.
Nothing to do.
Complete!
```
("Nothing to do" just means the instance was already fully up to date — this is normal on a freshly launched AMI.)

**What `dnf` is:** `dnf` (Dandified YUM) is the package manager used on Amazon Linux and other RHEL-based Linux distributions — it's the equivalent of `apt` on Ubuntu/Debian. Both do the same job (install, update, remove software), they just belong to different Linux "families." Amazon Linux uses `dnf`, which is exactly why `apt` failed above — the command doesn't exist on this OS at all.

**What this specific command does:**
- Checks for the latest available updates to installed packages.
- Installs security patches and bug fixes.
- `sudo` runs the command as administrator (root), required for system-level changes.
- `-y` automatically answers "yes" to any confirmation prompts, so the command doesn't pause waiting for input.

Think of it like updating all the apps on your phone before installing something new — you want the system current before adding a web server on top of it.

### Step 4: Install Apache Web Server
```bash
sudo dnf install httpd -y
```
This pulled in 13 packages (Apache itself plus dependencies like `apr`, `httpd-tools`, `mod_http2`) and completed with:
```
Installed:
  httpd-2.4.68-1.amzn2023.0.1.x86_64  ...
Complete!
```

📸 <img width="781" height="136" alt="image" src="https://github.com/user-attachments/assets/db349517-a4da-416d-9cee-04551e7fb0c6" />


**What this does:**
- Installs Apache, referred to by its package/service name `httpd` (HTTP Daemon).
- Apache is the software that actually serves your website's files to visitors' browsers.

Without a web server installed, the EC2 instance is just a machine with files sitting on it — nothing is listening for web requests:
```
Browser → EC2  ❌  (nothing responds)
```
With Apache installed and running:
```
Browser → Apache → Website  ✅
```

### Step 5: Start Apache
```bash
sudo systemctl start httpd
```
This starts the Apache service immediately. Installing software and starting it are two separate steps — think of it as: **installed = app downloaded, started = app opened.** Until this command runs, Apache exists on the server but isn't actively doing anything yet.

### Step 6: Enable Apache on Boot
```bash
sudo systemctl enable httpd
```
This tells the OS to automatically start Apache every time the instance boots up — including after a stop/restart.
- **Without this:** if the EC2 instance restarts for any reason, the website goes down until Apache is started manually again.
- **With this:** the website comes back automatically the moment the instance is running again.

### Step 7: Check Apache Status
```bash
sudo systemctl status httpd
```
Output confirmed it was running:
```
● httpd.service - The Apache HTTP Server
   Active: active (running) since Tue 2026-06-23 07:00:18 UTC
   Main PID: 26486 (httpd)
   ...
   httpd[26486]: Server configured, listening on: port 80
```

📸 <img width="721" height="155" alt="image" src="https://github.com/user-attachments/assets/809cfb41-bbcb-4f15-96e7-55ba114461c7" />


`active (running)` confirms Apache started successfully and is currently serving requests on port 80. Press `q` to exit the status screen and return to the terminal.

### Step 8: Test the Website

**Mistake to flag:** my first instinct was to type the URL directly into the SSH terminal:
```bash
http://35.154.165.61
```
This fails because the terminal is a Linux shell, not a browser — it tried to interpret `http://35.154.165.61` as a filename to run:
```
-bash: http://35.154.165.61: No such file or directory
```
Same result trying `httpd://35.154.165.61` — neither is a valid shell command.

**The correct way to test:** open a **web browser** (Chrome/Edge) on your own computer — not the SSH terminal — and type the URL into the address bar:
```
http://35.154.165.61
```

**If the page doesn't load in the browser:** this almost always means the Security Group is blocking traffic, not that Apache failed. Fix:
1. Go to **AWS → EC2 → Security Groups** (for the instance).
2. Add an inbound rule:

   | Type | Port | Source |
   |------|------|--------|
   | HTTP | 80 | Anywhere (`0.0.0.0/0`) |
3. Save, then refresh the browser.

### Step 9: Deploy the Portfolio Files *(in progress)*

Navigated to Apache's web root to prepare for file deployment:
```bash
cd /var/www/html
```
The SSH session disconnected right after this (`client_loop: send disconnect: Connection reset`) — just a dropped connection, not an error caused by the command. `cd` doesn't fail like that; this was a network blip / session timeout.

Remaining steps to complete deployment (reconnect via SSH, then run):
```bash
sudo rm -rf /var/www/html/*
```
Removes the default Apache placeholder page.

```bash
scp -i my-portfolio-key.pem -r ./portfolio/* ec2-user@35.154.165.61:/var/www/html/
```
Transfers portfolio files from the local machine to the server. *(Run this from the local machine, not inside the SSH session — `scp` connects from your computer to the server.)*

```bash
sudo chown -R apache:apache /var/www/html
```
Sets correct ownership so Apache can read and serve the files.


### Step 10: Verify the Live Site *(pending)*
Once files are uploaded, reload `http://35.154.165.61` in the browser — the portfolio should load, served directly by Apache.

📸 <img width="940" height="483" alt="image" src="https://github.com/user-attachments/assets/6d6a76d6-d4ec-4eb3-bbe7-cc7318e20fc8" />


---

## 3. Role of the Security Group

The **Security Group** in EC2 plays the same conceptual role that the bucket policy played in S3 hosting — it's the access control layer. But instead of controlling access to files, it controls access to the **server itself** at the network level:

- **SSH (22)** restricted to my IP only — prevents random internet traffic from attempting to log into the server, while still letting me manage it.
- **HTTP (80)** open to everyone — required for any visitor's browser to load the site.
- **HTTPS (443)** open to everyone — reserved for when SSL/TLS is configured.

Without the right inbound rules here, either nobody could reach the site (port 80 blocked) or the server would be exposed to unnecessary risk (SSH open to the world).

---

## 4. Live URL

**Current live state:** `http://35.154.165.61` — serving Apache's default test/welcome page (portfolio files not yet uploaded).

**Once Step 9 is complete**, this same URL will serve the actual portfolio instead.

*(Found on the EC2 instance's dashboard under "Public IPv4 address." Note: this IP will change if the instance is stopped and restarted, unless an Elastic IP is attached — see below.)*

---

## 5. What I'd Do Next to Make It Production Grade

Running a raw HTTP site on a bare public IP is fine for learning, but several gaps remain before this would be production-ready:

- **Attach an Elastic IP** — without one, the public IP changes every time the instance restarts, breaking any DNS pointed at it.
- **Set up a custom domain (Route 53 or external registrar)** — point a real domain at the Elastic IP instead of sharing a raw IP address.
- **Enable HTTPS** — install a free SSL certificate via **Let's Encrypt (Certbot)** and configure Apache to serve over port 443.
- **Restrict SSH further** — consider replacing direct SSH key access with **AWS Systems Manager Session Manager**, removing the need to expose port 22 at all.
- **Set up automatic patching** — keep the OS and Apache updated to avoid known vulnerabilities.
- **Add monitoring/alerts** — use **CloudWatch** to track CPU, memory, and uptime, and get notified if the instance goes down.
- **Set up a deployment pipeline** - instead of manual `scp` uploads, automate deployment with GitHub Actions or a simple webhook + `git pull` on push.
- **Consider an Auto Scaling Group + Load Balancer** — only relevant at real traffic scale, but worth knowing about for resilience (a single EC2 instance is a single point of failure).
- **Re-evaluate the hosting choice itself** — for a static portfolio specifically, this is the point where it's worth asking whether maintaining a server is worth it versus just using S3 + CloudFront, which removes almost all of the above concerns by design.

---

## Stack / Learning Context

This project was built while learning core AWS services: **IAM, EC2, S3, MFA, and VPC.** It served as a hands-on contrast to S3 static hosting — showing what's involved in running and securing an actual server versus using a fully managed storage-based hosting feature.
