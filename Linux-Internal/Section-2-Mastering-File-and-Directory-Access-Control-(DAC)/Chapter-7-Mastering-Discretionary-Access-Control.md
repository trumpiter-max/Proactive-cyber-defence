# Chapter 7: Mastering Discretionary Access Control

`Discretionary Access Control (DAC)` means that each user can control who can get into their stuff

## Table of content

- [Chapter 7: Mastering Discretionary Access Control](#chapter-7-mastering-discretionary-access-control)
  - [Table of content](#table-of-content)
  - [Using chown to change ownership of files and directories](#using-chown-to-change-ownership-of-files-and-directories)
  - [Using chmod to set permissions on files and directories](#using-chmod-to-set-permissions-on-files-and-directories)
    - [Setting permissions with the symbolic method](#setting-permissions-with-the-symbolic-method)
    - [Setting permissions with the numerical method](#setting-permissions-with-the-numerical-method)
    - [Using SUID and SGID on regular files](#using-suid-and-sgid-on-regular-files)
  - [The security implications of the SUID and SGID permissions](#the-security-implications-of-the-suid-and-sgid-permissions)
    - [Finding spurious SUID or SGID files](#finding-spurious-suid-or-sgid-files)
    - [Hands-on lab – searching for SUID and SGID files](#hands-on-lab--searching-for-suid-and-sgid-files)
    - [Preventing SUID and SGID usage on a partition](#preventing-suid-and-sgid-usage-on-a-partition)
  - [Using extended file attributes to protect sensitive files](#using-extended-file-attributes-to-protect-sensitive-files)
    - [Setting the a attribute](#setting-the-a-attribute)
    - [Setting the i attribute](#setting-the-i-attribute)
    - [Hands-on lab – setting security-related extended file attributes](#hands-on-lab--setting-security-related-extended-file-attributes)
  - [Securing system configuration files](#securing-system-configuration-files)

## Using chown to change ownership of files and directories

 - Controlling access to files and directories with `chown`
 - Require sudo privileges to use
 - Example: `sudo chown maggie: perm_demo.txt`    

## Using chmod to set permissions on files and directories

 - Three basic permissions:
    - r: read (Number 4)
    - w: write (Number 2)
    - x: execute the binary, or authorize a user to cd directory (Number 1)
 - `ls -l` to view all permissions
 - `chmod` changes permissions:
    - The symbolic method
    - The numerical method 

### Setting permissions with the symbolic method

 - `+`: add new permission
 - `-`: remove permission
 - Example: `chmod u+x,g+x donnie_script.sh`

### Setting permissions with the numerical method

 - `chmod User/Group/Other filename`   
 - Number permission equal total of all parts, like `rw` = 4 + 2 = 6
 - `stat -c %a` to show permissions of file with a number

### Using SUID and SGID on regular files

 - SUID (Set User ID) whoever accesses the file will have the same privileges as the user of the file
 - SGID (Set Group ID) same as above but for group

## The security implications of the SUID and SGID permissions
 
The numerical value for SUID is 4000, and SGID is 2000

### Finding spurious SUID or SGID files

 - Find SUID & SGID files then save logs into the file: `sudo find / -type f \( -perm -4000 -o -perm -2000 \) > suid_sgid_files.txt`
 - See more details: `sudo find / -type f \( -perm -4000 -o -perm -2000 \) -ls > suid_sgid_files.txt`
 - Less type version (4000 + 2000 = 6000): `sudo find / -type f -perm /6000 -ls > suid_sgid_files.txt` 


### Hands-on lab – searching for SUID and SGID files

```sh
    #!/bin/bash
    sudo find / -type f -perm /6000 -ls > ~/suid_sgid_files.txt

    su - desired_user_account
    touch some_shell_script.sh
    chmod 4755 some_shell_script.sh
    ls -l some_shell_script.sh
    exit

    sudo find / -type f -perm /6000 -ls > ~/suid_sgid_files_2.txt

    # Compare 
    diff suid_sgid_files.txt suid_sgid_files_2.txt
```

### Preventing SUID and SGID usage on a partition

Set up a custom partition scheme instead, you could have the /home directory in its own partition, where could set the `nosuid` option

## Using extended file attributes to protect sensitive files

 - `lsattr` show which extended attributes already have set
 - The two attributes in this sections:
    - a: append text to the end of a file that has this attribute, prevent overwriting
    - i: file is immutable, and only someone with proper sudo privileges can set or delete

### Setting the a attribute

 - Example to add new: `sudo chattr +a filename.txt`
 - Example to remove: `sudo chattr -i filename.txt`

### Setting the i attribute

When a file has the i attribute set, the only thing to do is view its contents

### Hands-on lab – setting security-related extended file attributes

```sh
    #!/bin/bash

    # Create file
    echo "Hello World" > ~/perm_demo.txt
    lsattr ~/perm_demo.txt

    # Update file 
    sudo chattr +a ~/perm_demo.txt
    lsattr ~/perm_demo.txt

    # Try to overwrite and delete the file
    echo "I want to overwrite this file." > ~/perm_demo.txt
    sudo echo "I want to overwrite this file." > ~/perm_demo.txt
    rm ~/perm_demo.txt
    sudo rm ~/perm_demo.txt
 
    # Append something to the file
    echo "I want to append this line to the end of the file." >> ~/perm_demo.txt

    # Change attribute
    sudo chattr -a perm_demo.txt
    lsattr perm_demo.txt
    sudo chattr +i perm_demo.txt
    lsattr perm_demo.txt

    # Try to overwrite and delete the file
    echo "I want to overwrite this file." > ~/perm_demo.txt
    sudo echo "I want to overwrite this file." > ~/perm_demo.txt
    rm ~/perm_demo.txt
    sudo rm ~/perm_demo.txt

    mv perm_demo.txt some_file.txt
    sudo mv perm_demo.txt some_file.txt
    ln ~/perm_demo.txt ~/some_file.txt
    sudo ln ~/perm_demo.txt ~/some_file.txt

    ln -s ~/perm_demo.txt ~/some_file.txt
    
```

## Securing system configuration files

 - Change the settings with trusty friend, known as the find utility: `sudo find / -iname '*.conf' -exec chmod 600 {} \;`
 - Change the `resolv.conf` permission setting back to 644
- Set the /etc/locale.conf file back to the 644 permission setting


