# Chapter 12: Logging and Log Security


- System log can tell 
  - how well your system is performing
  - how to troubleshoot problems
  - what the users—both authorized and unauthorized—are doing on the system.


## Linux system log files

- In the `/var/log` directory
  - On Red Hat-type system:
    - Main log file is the message files
    - Authentication-related events is the `secure` file
  - On Debian-type system:
    - Main log file is the `syslog` file
    - Authentication log is the `auth.log` file
  - `/var/log/kern.log`: On Debian system, it contains messages about what's going on with the Linux kernel.
  - `/var/log/wtmp` and `/var/run/utmp` : Record information about users who are logged in to te system. `wtmp` hold historical data from `utmp`
  - `/var/log/btmp`: Information about failed login attemps
  - `/var/log/lastlog`: Last time users logged in to the system
  - `/var/log/audit/audit.log`: Information from the audited daemon.

- The system log and the authentication log: 
  - Have the same basic structure and are all plaintext files.   
  - Ways to obtain specific information from the log files:
    - utility: `grep`, `less`
    - Writing scripts in languages: `bash`, `Python`, `awk`
- The utmp, wtmp, btmp, and lastlog files:
  - Binary files
  - Tools to extract information from them:
    - `w` and `who` : pull information about who's logged in and what they're doing from the `/var/run/utmp` file.
    - `last` command pulls information from the `/var/log/wtmp` file.
    - `lastlog` command: pulls information from `/var/log/lastlog` file => show record of all users on the machine and when they logged in last

## rsylog

- rsyslog logging rules
  - Define where to record messages for each particular system service:
    - On RedHat/CentOS systems, rules are stored in the `/etc/rsyslog.conf`
    - On Debian/Ubuntu systems, the rules are in separate files in the `/etc/rsyslog.d/` directory. The main file that we care is `deault.conf` file (contains the main logging rules)


## journald

- Use the systemd ecosystem
## Logwatch

## Setting up a remote log server
