# Chapter 2: Securing User Accounts

Make sure that users can always access their stuff and that they can perform the required tasks to do their jobs

---

## Table of content
 - [The dangers of logging in as the root user](#the-dangers-of-logging-in-as-the-root-user)
 - [The advantages of using sudo](#the-advantages-of-using-sudo)
 - [Setting up sudo privileges for full administrative users](#setting-up-sudo-privileges-for-full-administrative-users)
    - [Adding users to a predefined admin group](#adding-users-to-a-predefined-admin-group)
    - [Creating an entry in the sudo policy file](#creating-an-entry-in-the-sudo-policy-file)
    - [Hands-on lab for assigning limited sudo privileges](#hands-on-lab-for-assigning-limited-sudo-privileges)
 - [The sudo timer](#the-sudo-timer)
    - [View your sudo privileges](#view-your-sudo-privileges)
    - [Hands-on lab for disabling the sudo timer](#hands-on-lab-for-disabling-the-sudo-timer)
 - [Preventing users from having root shell access](#preventing-users-from-having-root-shell-access)
    - [Preventing users from using shell escapes](#preventing-users-from-using-shell-escapes) 
    - [Preventing users from using other dangerous programs](#preventing-users-from-using-other-dangerous-programs)
      - [Limiting the user's actions with commands](#limiting-the-users-actions-with-commands)
      - [Letting users run as other users](#letting-users-run-as-other-users)
    - [Preventing abuse via user's shell scripts](#preventing-abuse-via-users-shell-scripts)
    - [Detecting and deleting default user accounts](#detecting-and-deleting-default-user-account)
 - [Locking down users' home directories the Red Hat or CentOS way](#locking-down-users-home-directories-the-red-hat-or-centos-way)
 - [Locking down users' home directories the Debian/Ubuntu way](#locking-down-users-home-directories-the-debianubuntu-way)
    - [useradd on Debian/Ubuntu](#useradd-on-debianubuntu)
    - [adduser on Debian/Ubuntu](#adduser-on-debianubuntu)
    - [Hands-on lab for configuring adduser](#hands-on-lab-for-configuring-adduser)
 - [Enforcing strong password criteria](#enforcing-strong-password-criteria)

---

## The dangers of logging in as the root user

The root user can present a whole load of security problems, and can do the following:
 - Accidentally causes damage to the system
 - Someone else causes damage to the system

`sudo` utility allows users to perform administrative tasks without incurring the risk of having them always log on as the root user, and that would also allow users to have only the admin privileges they need to perform a certain job

---

## The advantages of using sudo

 - Assign certain users full administrative privileges
 - Allow users to perform administrative tasks
 - Make it harder for intruders to break into your systems
 - Improve your auditing capabilities
 - Create `sudo` policies to deploy across an entire enterprise network

---

## Setting up sudo privileges for full administrative users

## Adding users to a predefined admin group
 - In a business setting, allowing people to have password-less sudo privileges is a definite no-no
 - Some commands to config:
    - `groups` list user group file
    - `sudo visudo`, I'll open the sudo policy file then go to line `## Allows people in group <group-name>`
    - `usermod` add an existing user to the group with the -G option (Ex: `sudo usermod -a -G <group-name> <user-name>`)
    - `useradd` add a user account to the group as creating it (Ex: `sudo useradd -G <group-name> <user-name>`)
    - `sudo passwd -l root` disable the root account  

## Creating an entry in the sudo policy file

Config with with some command after using `sudo visudo` (in `/etc/sudoers` or simply `sudoer`):
 - `User_Alias ADMINS = <user-name-1>, <user-name-2>` set add own set of usernames, or add a line with own user alias
 - `ADMINS (or <user-name>) ALL=(ALL) ALL` give members of the user alias or special user full sudo power

## Setting up sudo for users with only certain delegated privileges

 - `User_Alias SOFTWAREADMINS = <user-name-1>, <user-name-2>` create other user aliases for other purposes
 - `Cmnd_Alias SOFTWARE = /bin/rpm, /usr/bin/up2date, /usr/bin/yum` is example command aliases
 - `SOFTWAREADMINS ALL=(ALL) SOFTWARE` assign the `SOFTWARE` command alias to the SOFTWAREADMINS user alias
 - `Host_Alias FILESERVERS = fs1, fs2` is host aliases example preceding the user alias

## Hands-on lab for assigning limited sudo privileges

---

## The sudo timer

 - By default, the sudo timer is set for five minutes (require password again for `sudo` command per 5 minutes)
 - Changing with `sudo visudo` then find and modify this line `Defaults        timestamp_timeout=XXXX` (replace `XXXX` to exactly minutes). Moreover, disable timeout `timestamp_timeout` to `!authenticate` 
 - Make this a global setting for all users, or set it for certain individual users
 - `sudo -k` reset the sudo timer

## View your sudo privileges

`sudo -l` see some of the environmental variables for user account and privileges

## Hands-on lab for disabling the sudo timer

---

## Preventing users from having root shell access

 - `<user-name> ALL=(ALL) /bin/bash, /bin/zsh` full access for the user so don't add lines like this to sudoers because it will trouble
 - Set up a user with limited sudo privileges

## Preventing users from using shell escapes

 - Certain programs, especially text editors and pagers, have a handy shell escape feature. This allows a user to run a shell command without having to exit the program first (Ex. `:!ls` to someone could run the `ls` command by running in Vi/Vim/emacs/less/view/more)
 - This use Vim's shell escape feature to perform other root-level commands, which includes being able to edit other configuration files
 - Fix this problem by having user use `sudoedit` (no shell escape feature) instead of vim

## Preventing users from using other dangerous programs

 - Give users unrestricted privileges to use dangerous programs (Ex. cat, cut, awk, sed, etc.)

## Limiting the user's actions with commands

 - sudo rule so that user can use the special command `<user-name> ALL=(ALL) <command-1>, <command-2>`
 - When writing sudo policies, should be aware of the differences between the different Linux and Unix distributions on network. Moreover, some system services have different names on different Linux distributions
 
## Letting users run as other users

 - Change that (ALL) to (root) in order to specify that user can only run these commands as the root user `user ALL=(root) <command-1>, <command-2>`
 - Change ALL=(database) to allow user run as the database user `user ALL=(database) <command-1>, <command-2>` or simply run with this command `sudo -u database <command>`

## Preventing abuse via user's shell scripts

 - If user allow in sudo rules to run own shell script (in home directory where user has full access control here) (`user ALL=(ALL) <shell-script-path>`), being the sneaky type, user can add the `sudo -i` ( log a person in to the root user's shell) line to the end of the script like this, excute it then user now logged in as the root user:
 ```sh
   #!/bin/bash
   echo "Hello World"
   sudo -i
 ```
 - Put shell script `/usr/local/sbin` directory and change the ownership to the root user so user can not change file, then `visudo` and change user rule to reflect the new location of the script

## Detecting and deleting default user account

 - `Internet of Things (IoT)` devices challenge normal operating system installation. In default setting, credentials are out there for all the world to see, and user is set up with full sudo privileges and isn't required to enter a sudo password (Ex. `raspex`)
 - Inside `/etc/sudoers` file of `raspex`: `raspex ALL=(ALL) NOPASSWD: ALL` allows the raspex user to do all sudo commands without having to enter a password
 - Some Linux distributions for IoT devices have this rule in a separate file in the /etc/sudoers.d directory which can be deleted by default user account, or change the root user password, and then lock the root user account

---

## Locking down users' home directories the Red Hat or CentOS way 

 - By default, the `useradd` utility on Red Hat-type systems creates user home directories with a permissions setting of 700 (user who owns the home directory
can access it)
 - In `/etc/login.defs` file of Red Hat-type, there is `UMASK` (set to such a restrictive value by default) line is what determines the permissions values on home directories
   ```
      CREATE_HOME yes
      UMASK 077 # removes all permissions from the group and others
   ```
 - Non-Red Hat distributions usually have a UMASK value of 022, which creates home directories with a permissions value of 755 allowing everybody to enter everybody else's home directories and access each others' files

---

## Locking down users' home directories the Debian/Ubuntu way

Debian/Ubuntu have two user creation utilities

## useradd on Debian/Ubuntu

 - `sudo useradd -m -d /home/user -s /bin/bash user` create a user account (-m creates the home directory, -d home directory path, -s specifies user's default shell)
 - Change the default permissions setting for home directories, open /etc/login.defs for editing `UMASK 022` to `UMASK 077` to lockdown like Red Hat-type

## adduser on Debian/Ubuntu

 - Is an interactive way to create user accounts and passwords with a
single command which is unique to the Debian family but default permission value is 755
 - useradd doesn't automatically encrypt a user's home directory as creating the account. Install the ecryptfs-utils package to solve problem
 - The first time login, using ecryptfs-unwrap-passphrase command to encrypt with passphrase

## Hands-on lab for configuring adduser

---

## Enforcing strong password criteria
