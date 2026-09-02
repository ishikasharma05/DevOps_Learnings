# Git & SSH — Commands I've Learned

This file documents the Git and SSH commands I practiced as part of my DevOps learning.  
All commands were run on Ubuntu (Linux). Screenshots are attached below each section.

---

## SSH Setup & Service Management

These commands are used to start and verify the SSH service on Linux before connecting to a remote machine.

```bash
sudo systemctl status ssh     # Check if SSH service is running
sudo systemctl start ssh      # Start the SSH service if it's stopped
```

```bash
ssh ishika2@localhost          # Connect to local machine via SSH using another user
```

> Screenshot ↓

<img width="573" height="55" alt="Screenshot 2026-05-30 121121" src="https://github.com/user-attachments/assets/01ec84fe-e1d2-4aea-ab79-8d9a4e7cbec8" />


---

## SSH Key Generation

SSH keys are used to authenticate with GitHub without typing a password every time.

```bash
cd ~/.ssh/                     # Navigate to the SSH directory
ssh-keygen -o                  # Generate a new SSH key pair (-o uses a stronger format)
```

> Screenshot ↓

<img width="1191" height="685" alt="Screenshot 2026-05-30 121104" src="https://github.com/user-attachments/assets/47cc48b3-8712-40e1-a130-327b2ff15510" />


---

## Git Configuration

Before using Git, you need to set up your identity and verify settings.

```bash
git config --list              # View all current Git configuration settings
```

> Screenshot ↓

<img width="1586" height="404" alt="Screenshot 2026-05-30 122746" src="https://github.com/user-attachments/assets/18f31cd8-d5c7-4a5a-a1d8-6b5203c5287f" />


---

## Starting with a Repository

```bash
git clone <repo-url>           # Download a remote repository to your local machine
git status                     # Check which files are changed or untracked
```

> Screenshot ↓

<img width="916" height="643" alt="Screenshot 2026-06-02 183619" src="https://github.com/user-attachments/assets/51491e5c-ceb1-45f5-b44c-ac56ad7ed939" />


---

## Staging, Committing & Pushing

This is the core Git workflow — track changes, save them, send them to GitHub.

```bash
git add .                      # Stage all changed files for commit
git add <filename>             # Stage a specific file

git commit -m "your message"   # Save staged changes with a descriptive message

git push                       # Upload commits to the remote repository (GitHub)
git pull                       # Download and merge latest changes from remote
```

> Screenshot ↓

<img width="1473" height="394" alt="Screenshot 2026-06-02 183702" src="https://github.com/user-attachments/assets/0ad27dc3-4db7-4682-89c8-ed1e578710ac" />


---

## Branching & Switching

Branches let you work on features or experiments without touching the main codebase.

```bash
git branch                     # List all local branches
git branch <branch-name>       # Create a new branch

git checkout <branch-name>     # Switch to an existing branch
git checkout -b <branch-name>  # Create AND switch to a new branch in one step
```

> Screenshot ↓

<img width="1037" height="743" alt="Screenshot 2026-06-02 182450" src="https://github.com/user-attachments/assets/f3c5594a-f563-4297-8b9e-625b5290ab9d" />


---

## Ignoring Files

Some files should never be pushed to GitHub — like `.env` files, `node_modules`, etc.

```bash
# Create a .gitignore file and list what to ignore
touch .gitignore
```

Example `.gitignore` content:

```
node_modules/
.env
*.log
__pycache__/
```

> Screenshot ↓

<img width="1023" height="856" alt="Screenshot 2026-06-02 183640" src="https://github.com/user-attachments/assets/d78e3f86-9988-48fa-a5a7-22c160d3853f" />


---

## Viewing Commit History

```bash
git log                        # View full commit history with author, date, and message
git log --oneline              # Compact view — one line per commit
```

> Screenshot ↓

<img width="740" height="355" alt="image" src="https://github.com/user-attachments/assets/df1ba376-fc21-4bcc-af85-cd716aa6d963" />


---

## Summary Table

| Command | What It Does |
|---|---|
| `sudo systemctl status ssh` | Check if SSH is running |
| `sudo systemctl start ssh` | Start SSH service |
| `ssh user@host` | Connect to a machine via SSH |
| `ssh-keygen -o` | Generate SSH key pair |
| `git config --list` | View Git settings |
| `git clone <url>` | Clone a remote repo |
| `git status` | See changed/staged files |
| `git add` | Stage files for commit |
| `git commit -m` | Save changes with a message |
| `git push` | Push commits to GitHub |
| `git pull` | Pull latest changes |
| `git branch` | List or create branches |
| `git checkout` | Switch or create branches |
| `.gitignore` | Tell Git which files to ignore |
| `git log` | View commit history |

---

*Part of my DevOps learning journey — practicing Linux, Git, and SSH fundamentals.*
