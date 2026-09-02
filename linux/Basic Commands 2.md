# 🐧 Linux Commands Reference Guide

A beginner-friendly reference for essential Linux file search, text processing, and pipeline commands.

---

## Table of Contents

1. [find](#1-find)
2. [locate](#2-locate)
3. [grep](#3-grep)
4. [less](#4-less)
5. [head](#5-head)
6. [tail](#6-tail)
7. [sort](#7-sort)
8. [uniq](#8-uniq)
9. [wc](#9-wc)
10. [pipe ( | )](#10-pipe--)

---

## 1. `find`

**Purpose:** Search for files and directories **in real-time** by traversing the directory tree.

**Syntax:**
```bash
find [path] [options] [expression]
```

**Common Examples:**
```bash
# Find a file by name in the current directory and subdirectories
find . -name "filename.txt"

# Find all .log files under /var
find /var -name "*.log"

# Find files modified in the last 7 days
find . -mtime -7

# Find and delete all .tmp files
find . -name "*.tmp" -delete

# Find directories only
find /home -type d -name "projects"

# Find files larger than 100MB
find / -size +100M
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `-name` | Search by filename (case-sensitive) |
| `-iname` | Search by filename (case-insensitive) |
| `-type f` | Match files only |
| `-type d` | Match directories only |
| `-mtime -N` | Modified within last N days |
| `-size +NM` | Files larger than N megabytes |
| `-delete` | Delete matched files |
| `-exec` | Execute a command on each result |

> **Note:** `find` searches the live filesystem — it's slower but always up-to-date.

<img width="953" height="317" alt="Screenshot 2026-06-03 184131" src="https://github.com/user-attachments/assets/eac40244-d070-466a-9dce-e3a98aae0aaa" />

---

## 2. `locate`

**Purpose:** Quickly find files by name using a **pre-built database** (much faster than `find`).

**Syntax:**
```bash
locate [options] filename
```

**Common Examples:**
```bash
# Locate a file by name
locate filename.txt

# Case-insensitive search
locate -i README.md

# Limit results to 10
locate -n 10 config.conf

# Update the database (run as root or with sudo)
sudo updatedb
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `-i` | Case-insensitive search |
| `-n N` | Limit output to N results |
| `-c` | Count matching entries only |
| `--regex` | Use regular expressions |

> **Note:** `locate` reads from `/var/lib/mlocate/mlocate.db`. Run `sudo updatedb` after adding new files so they appear in results.

<img width="866" height="401" alt="Screenshot 2026-06-03 184836" src="https://github.com/user-attachments/assets/8d51ff22-ce43-4f93-9e63-7cdb0981cc2f" />

<img width="575" height="107" alt="Screenshot 2026-06-03 184901" src="https://github.com/user-attachments/assets/b7fbddb6-e1e7-40d9-8278-1ea0678e4d30" />

---

## 3. `grep`

**Purpose:** Search for a **pattern (text/regex)** within files or command output.

**Syntax:**
```bash
grep [options] "pattern" [file...]
```

**Common Examples:**
```bash
# Search for the word "error" in a file
grep "error" logfile.txt

# Case-insensitive search
grep -i "warning" logfile.txt

# Show line numbers of matches
grep -n "TODO" script.py

# Search recursively in all files under a directory
grep -r "password" /etc/

# Invert match — show lines that do NOT contain the pattern
grep -v "DEBUG" app.log

# Count the number of matching lines
grep -c "ERROR" server.log

# Show only the matched part (not the full line)
grep -o "http[s]*://[^ ]*" file.txt

# Use extended regular expressions
grep -E "error|fail|critical" logfile.txt
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `-i` | Ignore case |
| `-n` | Show line numbers |
| `-r` | Recursive search |
| `-v` | Invert match |
| `-c` | Count matches |
| `-l` | List filenames with matches |
| `-o` | Print only matched text |
| `-E` | Use extended regex |
| `-w` | Match whole words only |

> **Tip:** `grep` is most powerful when combined with pipe (`|`) to filter output from other commands.

<img width="849" height="65" alt="Screenshot 2026-06-03 190252" src="https://github.com/user-attachments/assets/67944a84-27d1-4466-a2ed-8b2256f48f78" />

<img width="925" height="53" alt="Screenshot 2026-06-03 191331" src="https://github.com/user-attachments/assets/0468c8d5-ea05-4e01-a085-432d7a342658" />

<img width="915" height="112" alt="Screenshot 2026-06-03 191342" src="https://github.com/user-attachments/assets/13bbf570-c1c0-4063-937e-e00d965c509e" />

<img width="931" height="58" alt="Screenshot 2026-06-03 191355" src="https://github.com/user-attachments/assets/c7571ca0-5adf-4a9f-9d8e-ddf53dbe7dd1" />


---

## 4. `less`

**Purpose:** View file contents **one page at a time** (scrollable, read-only viewer).

**Syntax:**
```bash
less [options] filename
```

**Common Examples:**
```bash
# Open a file in less
less /var/log/syslog

# Open with line numbers
less -N filename.txt

# Search within less (after opening)
# Press / then type your search term, press Enter
# Press n to go to next match, N for previous
```

**Navigation Shortcuts (inside `less`):**

| Key | Action |
|-----|--------|
| `Space` / `f` | Scroll forward one page |
| `b` | Scroll backward one page |
| `↑` / `↓` | Scroll one line |
| `g` | Go to beginning of file |
| `G` | Go to end of file |
| `/pattern` | Search forward |
| `?pattern` | Search backward |
| `n` | Next search match |
| `N` | Previous search match |
| `q` | Quit |

> **Tip:** Unlike `cat`, `less` doesn't load the entire file into memory — great for large files like logs.

<img width="779" height="34" alt="Screenshot 2026-06-03 192407" src="https://github.com/user-attachments/assets/5d42662f-e9d2-4e88-a5ca-4bab155c4ae7" />

---

## 5. `head`

**Purpose:** Display the **first N lines** of a file (default: 10 lines).

**Syntax:**
```bash
head [options] filename
```

**Common Examples:**
```bash
# Show first 10 lines (default)
head filename.txt

# Show first 20 lines
head -n 20 filename.txt

# Show first 5 lines of multiple files
head -n 5 file1.txt file2.txt

# Show first 100 bytes of a file
head -c 100 filename.txt
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `-n N` | Show first N lines |
| `-c N` | Show first N bytes |

> **Use case:** Quickly preview the structure/header of a large CSV or log file.

<img width="1727" height="785" alt="Screenshot 2026-06-03 192430" src="https://github.com/user-attachments/assets/44b16674-0ff8-4334-9e5f-1c7ae0d043f3" />

---

## 6. `tail`

**Purpose:** Display the **last N lines** of a file (default: 10 lines). Also used to monitor live log files.

**Syntax:**
```bash
tail [options] filename
```

**Common Examples:**
```bash
# Show last 10 lines (default)
tail filename.txt

# Show last 25 lines
tail -n 25 filename.txt

# Follow a file in real-time (live monitoring)
tail -f /var/log/syslog

# Follow with N lines shown initially
tail -f -n 50 app.log
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `-n N` | Show last N lines |
| `-c N` | Show last N bytes |
| `-f` | Follow — stream new lines as file grows |
| `-F` | Like `-f`, but handles log rotation |

> **Use case:** `tail -f` is the go-to command for watching server logs in real-time.

<img width="1697" height="653" alt="Screenshot 2026-06-03 192522" src="https://github.com/user-attachments/assets/a565e321-f522-441c-9089-48661a4bd7e3" />

---

## 7. `sort`

**Purpose:** Sort lines of text **alphabetically or numerically**.

**Syntax:**
```bash
sort [options] [file]
```

**Common Examples:**
```bash
# Sort lines alphabetically
sort names.txt

# Sort in reverse order
sort -r names.txt

# Sort numerically
sort -n numbers.txt

# Sort by the 2nd column (space-separated)
sort -k2 data.txt

# Sort and remove duplicates
sort -u names.txt

# Sort a CSV by 3rd column numerically
sort -t',' -k3 -n data.csv
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `-r` | Reverse order |
| `-n` | Numeric sort |
| `-u` | Remove duplicate lines |
| `-k N` | Sort by column N |
| `-t 'X'` | Use X as field delimiter |
| `-f` | Ignore case |
| `-h` | Human-readable numbers (e.g., 1K, 2M) |


<img width="837" height="174" alt="Screenshot 2026-06-03 193040" src="https://github.com/user-attachments/assets/4bfd2ed6-2563-487e-b871-6898c8ad2c03" />

---

## 8. `uniq`

**Purpose:** Remove or report **consecutive duplicate lines** in a file.

**Syntax:**
```bash
uniq [options] [input] [output]
```

**Common Examples:**
```bash
# Remove consecutive duplicate lines
uniq file.txt

# Count occurrences of each line
uniq -c file.txt

# Show only duplicate lines
uniq -d file.txt

# Show only unique (non-duplicate) lines
uniq -u file.txt

# Case-insensitive duplicate removal
uniq -i file.txt
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `-c` | Prefix lines with count of occurrences |
| `-d` | Only print duplicate lines |
| `-u` | Only print unique lines |
| `-i` | Ignore case differences |

> **Important:** `uniq` only detects **consecutive** duplicates. Always `sort` first if your duplicates may be non-adjacent:
> ```bash
> sort file.txt | uniq
> ```

---

## 9. `wc`

**Purpose:** Count **lines, words, and characters/bytes** in a file.

**Syntax:**
```bash
wc [options] [file...]
```

**Common Examples:**
```bash
# Count lines, words, and bytes
wc filename.txt

# Count lines only
wc -l filename.txt

# Count words only
wc -w filename.txt

# Count characters only
wc -c filename.txt

# Count lines in multiple files + total
wc -l file1.txt file2.txt
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `-l` | Count lines |
| `-w` | Count words |
| `-c` | Count bytes |
| `-m` | Count characters (handles multi-byte) |

**Sample Output:**
```
  42  318  2048 filename.txt
  ^    ^    ^
lines words bytes
```

> **Tip:** Use `wc -l` at the end of a pipeline to count how many results a command returned.

<img width="785" height="115" alt="Screenshot 2026-06-03 192746" src="https://github.com/user-attachments/assets/376be665-016e-46fa-b9d7-f581f0e24e45" />

---

## 10. Pipe ( `|` )

**Purpose:** Connect commands — sends the **output of one command as the input to another**.

**Syntax:**
```bash
command1 | command2 | command3 ...
```

**How It Works:**

```
[command1] --output--> [command2] --output--> [command3] --output--> Terminal
```

**Common Examples:**
```bash
# List files and search for .txt files
ls -l | grep ".txt"

# Show running processes and search for a specific one
ps aux | grep "nginx"

# Count the number of files in a directory
ls | wc -l

# Sort and remove duplicates from a file
cat names.txt | sort | uniq

# Find errors in a log, sort them, and count unique ones
grep "ERROR" app.log | sort | uniq -c | sort -rn

# Show the top 5 most frequent errors
grep "ERROR" app.log | sort | uniq -c | sort -rn | head -5

# View long command output page by page
cat /var/log/syslog | less

# Count how many lines contain "warning"
grep -i "warning" logfile.txt | wc -l
```

**Power Pipeline Example:**
```bash
# Find all .py files, search for "import", sort results, remove duplicates
find . -name "*.py" | xargs grep "import" | sort | uniq
```

> **Key concept:** The pipe `|` is what makes Linux commands truly powerful — small, focused commands chained together to solve complex problems.

<img width="1045" height="56" alt="Screenshot 2026-06-03 193743" src="https://github.com/user-attachments/assets/ad6f460f-65a4-48e9-a487-ee7e1ed414bc" />

---

## Quick Reference Cheat Sheet

| Command | Primary Use | Key Flag |
|---------|-------------|----------|
| `find` | Search files (live) | `-name`, `-type`, `-mtime` |
| `locate` | Search files (fast, DB) | `-i`, `updatedb` |
| `grep` | Search text patterns | `-r`, `-i`, `-n`, `-v` |
| `less` | Page through file | `/` to search, `q` to quit |
| `head` | First N lines | `-n` |
| `tail` | Last N lines / live follow | `-n`, `-f` |
| `sort` | Sort lines | `-n`, `-r`, `-u`, `-k` |
| `uniq` | Remove duplicates | `-c`, `-d`, `-u` |
| `wc` | Count lines/words/bytes | `-l`, `-w`, `-c` |
| `\|` | Chain commands | — |

---

## Combining Commands — Real-World Examples

```bash
# 1. Find the 10 largest files in current directory
find . -type f | xargs du -sh | sort -rh | head -10

# 2. Count unique IP addresses in an access log
grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" access.log | sort | uniq -c | sort -rn

# 3. Search all Python files for a function and show line numbers
find . -name "*.py" -exec grep -n "def my_function" {} +

# 4. Monitor a log file and highlight errors
tail -f app.log | grep --color "ERROR"

# 5. Get the total word count across all .txt files
find . -name "*.txt" | xargs wc -w | tail -1
```

---

*Last updated: June 2026 | Linux Commands Reference*
