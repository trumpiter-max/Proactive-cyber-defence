# Chapter 8: Access Control Lists and Shared Directory Management

`Access Control List (ACL)` allows only a certain person to access a file, or allows multiple people to access a file with different permissions for each person

## Table of content

- [Chapter 8: Access Control Lists and Shared Directory Management](#chapter-8-access-control-lists-and-shared-directory-management)
  - [Table of content](#table-of-content)
  - [Creating an ACL for either a user or a group](#creating-an-acl-for-either-a-user-or-a-group)
    - [Creating an inherited ACL for a directory](#creating-an-inherited-acl-for-a-directory)
    - [Removing a specific permission by using an ACL mask](#removing-a-specific-permission-by-using-an-acl-mask)
    - [Using the tar --acls option to prevent the loss of ACLs during a backup](#using-the-tar---acls-option-to-prevent-the-loss-of-acls-during-a-backup)
  - [Creating a user group and adding members to it](#creating-a-user-group-and-adding-members-to-it)
    - [Adding members as we create their user accounts](#adding-members-as-we-create-their-user-accounts)
    - [Using usermod to add an existing user to a group](#using-usermod-to-add-an-existing-user-to-a-group)
    - [Adding users to a group by editing the /etc/group file](#adding-users-to-a-group-by-editing-the-etcgroup-file)
    - [Creating a shared directory](#creating-a-shared-directory)
    - [Setting the SGID bit and the sticky bit on the shared directory](#setting-the-sgid-bit-and-the-sticky-bit-on-the-shared-directory)
  - [Using ACLs to access files in the shared directory](#using-acls-to-access-files-in-the-shared-directory)
    - [Setting the permissions and creating the ACL](#setting-the-permissions-and-creating-the-acl)
    - [Hands-on lab – creating a shared group directory](#hands-on-lab--creating-a-shared-group-directory)


## Creating an ACL for either a user or a group

 - Use `getfacl` to view an ACL for a file or directory
 - Allow a user or a group to have any
combination of read, write, or execute privileges

### Creating an inherited ACL for a directory

 - Create the new_perm_dir directory, and set the inherited ACL on it
 - Create donnie_script.sh and run to make new_file.txt with the correct permissions settings
```sh
    #!/bin/bash
    cd new_perm_dir
    touch new_file.txt
    chmod 600 new_file.txt
    exit
```

### Removing a specific permission by using an ACL mask

Remove an ACL from a file or directory with the -x option

### Using the tar --acls option to prevent the loss of ACLs during a backup

Using tar to create a backup of either a file or a last two files

## Creating a user group and adding members to it

Three different ways:
 - Add members as we create their user accounts.
 - Using `usermod` to add members that already have user accounts.
 - Edit the /etc/group file

### Adding members as we create their user accounts

 - Using the -G option of useradd
 - CentOS: `sudo useradd -G marketing cleopatra`
 - Debian/Ubuntu: `sudo useradd -m -d /home/cleopatra -s /bin/bash -G marketing cleopatra`

### Using usermod to add an existing user to a group

```sh
  #!/bin/bash
  sudo usermod -a -G marketing maggie
  groups maggie
```

### Adding users to a group by editing the /etc/group file

Adding this line `marketing:x:1005:cleopatra,maggie,vicky,charlie` to /etc/group file

### Creating a shared directory

```sh
  #!/bin/bash

  cd /
  sudo mkdir marketing
  ls -ld marketing
  sudo chown nobody:marketing marketing
  sudo chmod 770 marketing
  ls -ld marketing

  # Verify with other user
  su - vicky
  cd /marketing
  touch vicky_file.txt
  ls -l

```

### Setting the SGID bit and the sticky bit on the shared directory

```sh
  #!/bin/bash
  sudo chmod 2770 marketing
  ls -ld marketing

  su - vicky
  cd /marketing
  touch vicky_file_2.txt
  ls -l

  su - charlie
  cd /marketing
  touch charlie_file.txt
  ls -l

  rm vicky*
  ls -l
```

## Using ACLs to access files in the shared directory

Restricting access to a file to only specific group members

### Setting the permissions and creating the ACL

```sh
  #!/bin/bash

  # Vicky sets the normal permissions
  echo "This file is only for my good friend, Cleopatra." > vicky_file.txt
  chmod 600 vicky_file.txt
  setfacl -m u:cleopatra:r vicky_file.txt
  ls -l

  # Check if Cleopatra actually can read
  su - cleopatra
  cd /marketing
  ls -l
  cat vicky_file.txt
  echo "You are my friend too, Vicky." >> vicky_file.txt

  # Check if Charlie can do anything
  su - charlie
  cd /marketing
  cat vicky_file.txt

```

### Hands-on lab – creating a shared group directory

```sh
    #!/bin/bash

    sudo groupadd sales

    if ((grep -c ubuntu /etc/os-release)); then
        sudo useradd -m -d /home/mimi -s /bin/bash -G sales mimi
        sudo useradd -m -d /home/mrgray -s /bin/bash -G sales mrgray
        sudo useradd -m -d /home/mommy -s /bin/bash -G sales mommy

    else if if ((grep -c centos /etc/os-release)); then
        sudo useradd -G sales mimi
        sudo useradd -G sales mrgray
        sudo useradd -G sales mommy

    sudo passwd mimi
    sudo passwd mrgray
    sudo passwd mommy;

    sudo mkdir /sales
    sudo chown nobody:sales /sales
    sudo chmod 3770 /sales
    ls -ld /sales

    su - mimi
    cd /sales
    echo "This file belongs to Mimi." > mimi_file.txt
    ls -l
    chmod 600 mimi_file.txt
    setfacl -m u:mrgray:r mimi_file.txt
    getfacl mimi_file.txt
    ls -l

    su - mrgray
    cd /sales
    cat mimi_file.txt
    echo "I want to add something to this file." >> mimi_file.txt
    echo "Mr. Gray will now create his own file." > mr_gray_file.txt ls -l

    su - mommy
    cat mimi_file.txt
    cat mr_gray_file.txt
    rm -f mimi_file.txt
    rm -f mr_gray_file.txt
    exit
```



