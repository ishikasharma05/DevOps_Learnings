# Linux Basic Commands

These are the first commands I learned. Practiced all of them 
on terminal myself.

---

## whoami
Tells you which user you're logged in as.

```bash
whoami
# output: ishika
```
Useful when you're working on servers where multiple users exist
and you need to confirm who you are.

---

## man
Opens the manual for any command.

```bash
man ls
```
This is the most important command to know honestly.
Whenever you don't know what a command does or what options it has —
just type man before it. Press q to exit.

---

## clear
Clears the terminal screen. That's it.

```bash
clear
```
Doesn't delete your history. Just cleans up the mess on screen.

---

## pwd
Shows where you currently are in the system.

```bash
pwd
# output: /home/ishika
```
I use this constantly when I get lost navigating folders.

---

## ls and ls -l
ls lists what's inside your current folder.
ls -l shows the same thing but with extra details like 
permissions, owner, size, and date.

```bash
ls
ls -l
ls -a      # shows hidden files too
ls -lh     # shows file sizes in readable format like KB, MB
```

---

## cd
Move between folders.

```bash
cd projects        # go into projects folder
cd ..              # go back one level
cd ~               # go to home directory
cd -               # go back to where you just were
```

---

## mkdir
Creates a new folder.

```bash
mkdir devops-notes
mkdir -p projects/aws/ec2    # creates the full path at once
```
The -p flag is handy when you want to create nested folders 
in one go without creating each one separately.

---

## touch
Creates a new empty file instantly.

```bash
touch notes.txt
touch script.sh
```

---

## rm and rmdir
rm deletes files. rmdir deletes empty folders.

```bash
rm notes.txt           # delete a file
rm -r foldername/      # delete a folder and everything inside it
rmdir empty-folder     # only works if folder is empty
```

⚠️ rm has no undo. There's no recycle bin in Linux.
Once it's gone, it's gone. Be careful especially with rm -r.

---

## mv
Moves files or renames them. Same command does both.

```bash
mv notes.txt documents/          # move to another folder
mv oldname.txt newname.txt       # rename
```

---

## cp
Copies files or folders.

```bash
cp notes.txt notes-backup.txt       # copy a file
cp -r projects/ projects-backup/    # copy entire folder
```
Need -r when copying folders. Without it the command won't work.

---

## date
Shows current date and time.

```bash
date
# output: Mon Jun 2 10:30:00 IST 2026
```
Mostly useful inside scripts when you want to timestamp something
like a log file or a backup.

---

## cat
Prints the content of a file directly in terminal.

```bash
cat notes.txt
```
Good for small files. If the file is huge it'll flood your screen —
use less for large files instead.

---

## echo
Prints text to terminal or writes text into a file.

```bash
echo "Hello"                      # prints to terminal
echo "my notes" > notes.txt       # writes to file, overwrites existing content
echo "more notes" >> notes.txt    # adds to file without deleting what's there
```
The difference between > and >> matters a lot.
> overwrites everything. >> just adds to the end.

---

## nano
A simple text editor inside the terminal.

```bash
nano notes.txt
```

Shortcuts inside nano:
- Ctrl + O to save
- Ctrl + X to exit
- Ctrl + K to cut a line
- Ctrl + U to paste it back

You'll use this a lot when editing config files on a server
where you don't have a proper code editor.

---

## wc
Counts lines, words, and characters in a file.

```bash
wc notes.txt
# output: 5 20 100 notes.txt
# means: 5 lines, 20 words, 100 characters

wc -l notes.txt    # just count lines
```
I use wc -l on log files to see how many entries are in there.

---

## find
Searches for files anywhere in the system.

```bash
find . -name "notes.txt"          # find by exact name
find . -name "*.sh"               # find all shell scripts
find . -type d                    # find only folders
```
The dot means search from current location.
Replace it with / to search the entire system.

---

## du
Shows how much disk space a file or folder is taking up.

```bash
du -h notes.txt       # size of one file
du -sh projects/      # total size of a folder
du -sh *              # size of everything here
```
-h makes it readable. Without it you get raw bytes which is hard to read.

---

## df
Shows how much space is left on the disk overall.

```bash
df -h
```
This gives you a full picture of every partition —
total size, used space, free space, and percentage used.

If the Use% column hits 85% or above on a server, 
that needs to be fixed immediately.
Disk full = server down in most cases.

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| whoami | shows current user |
| pwd | shows current location |
| ls | lists files |
| cd | moves between folders |
| mkdir | creates folder |
| touch | creates empty file |
| rm | deletes file |
| rmdir | deletes empty folder |
| mv | moves or renames |
| cp | copies |
| cat | shows file content |
| echo | prints text or writes to file |
| nano | terminal text editor |
| wc | counts lines words characters |
| find | searches for files |
| du | space used by files |
| df | space left on disk |
| date | current date and time |
| clear | clears the screen |
| man | opens command manual |

---

✅ All 20 commands practiced on terminal personally.

Part of my DevOps learning journey →
[DevOps_Learnings](https://github.com/ishikasharma05/DevOps_Learnings)
