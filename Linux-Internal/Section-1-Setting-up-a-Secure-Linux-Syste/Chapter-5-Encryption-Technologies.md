# Chapter 5: Encryption Technologies

Encryption provides three things:
 - Confidentiality
 - Integrity
 - Availability

---

## Table of content

- [Chapter 5: Encryption Technologies](#chapter-5-encryption-technologies)
  - [Table of content](#table-of-content)
  - [GNU Privacy Guard (GPG)](#gnu-privacy-guard-gpg)
  - [Hands-on lab – creating your GPG keys](#hands-on-lab--creating-your-gpg-keys)
    - [Hands-on lab – creating your GPG keys](#hands-on-lab--creating-your-gpg-keys-1)
    - [Hands-on lab – symmetrically encrypting your files](#hands-on-lab--symmetrically-encrypting-your-files)
    - [Hands-on lab – encrypting files with public keys](#hands-on-lab--encrypting-files-with-public-keys)
    - [Hands-on lab – signing a file without encryption](#hands-on-lab--signing-a-file-without-encryption)
  - [Encrypting partitions with Linux Unified Key Setup (LUKS)](#encrypting-partitions-with-linux-unified-key-setup-luks)
  - [Disk encryption during operating system installation](#disk-encryption-during-operating-system-installation)
    - [Hands-on lab – adding an encrypted partition with LUKS](#hands-on-lab--adding-an-encrypted-partition-with-luks)
  - [Configuring the LUKS partition to mount automatically](#configuring-the-luks-partition-to-mount-automatically)
    - [Hands-on lab – configuring the LUKS partition to mount automatically](#hands-on-lab--configuring-the-luks-partition-to-mount-automatically)
  - [Encrypting directories with eCryptfs](#encrypting-directories-with-ecryptfs)
  - [Home directory and disk encryption during Ubuntu installation](#home-directory-and-disk-encryption-during-ubuntu-installation)
    - [Hands-on lab – encrypting a home directory for a new user account](#hands-on-lab--encrypting-a-home-directory-for-a-new-user-account)
  - [Creating a private directory within an existing home directory](#creating-a-private-directory-within-an-existing-home-directory)
    - [Hands-on lab – encrypting other directories with eCryptfs](#hands-on-lab--encrypting-other-directories-with-ecryptfs)
  - [Encrypting the swap partition with eCryptfs](#encrypting-the-swap-partition-with-ecryptfs)
  - [Using VeraCrypt for cross-platform sharing of encrypted containers](#using-veracrypt-for-cross-platform-sharing-of-encrypted-containers)
    - [Hands-on lab – getting and installing VeraCrypt](#hands-on-lab--getting-and-installing-veracrypt)
    - [Hands-on lab – creating and mounting a VeraCrypt volume in console mode](#hands-on-lab--creating-and-mounting-a-veracrypt-volume-in-console-mode)
  - [Using VeraCrypt in GUI mode](#using-veracrypt-in-gui-mode)
  - [OpenSSL and the public key infrastructure](#openssl-and-the-public-key-infrastructure)
  - [Commercial certificate authorities](#commercial-certificate-authorities)
  - [Creating keys, certificate signing requests, and certificates](#creating-keys-certificate-signing-requests-and-certificates)
    - [Creating a self-signed certificate with an RSA key](#creating-a-self-signed-certificate-with-an-rsa-key)
    - [Creating a self-signed certificate with an Elliptic Curve key](#creating-a-self-signed-certificate-with-an-elliptic-curve-key)
  - [Creating an RSA key and a Certificate Signing Request](#creating-an-rsa-key-and-a-certificate-signing-request)
    - [Creating an EC key and a CSR](#creating-an-ec-key-and-a-csr)
    - [Creating an on-premises CA](#creating-an-on-premises-ca)
    - [Hands-on lab – setting up a Dogtag CA](#hands-on-lab--setting-up-a-dogtag-ca)
  - [Adding a CA to an operating system](#adding-a-ca-to-an-operating-system)
    - [Hands-on lab – exporting and importing the Dogtag CA certificate](#hands-on-lab--exporting-and-importing-the-dogtag-ca-certificate)
  - [Importing the CA into Windows](#importing-the-ca-into-windows)
  - [OpenSSL and the Apache web server](#openssl-and-the-apache-web-server)
    - [Hardening Apache SSL/TLS on Ubuntu](#hardening-apache-ssltls-on-ubuntu)
    - [Hardening Apache SSL/TLS on RHEL 8/CentOS 8](#hardening-apache-ssltls-on-rhel-8centos-8)
    - [Hardening Apache SSL/TLS on RHEL 7/CentOS 7](#hardening-apache-ssltls-on-rhel-7centos-7)
  - [Setting up mutual authentication](#setting-up-mutual-authentication)

---

## GNU Privacy Guard (GPG)

Pros:
 - Strong, hard-to-crack 
 - Private/public key scheme
 - Able to encrypt email messages
 - GUI-type frontends available
  
Cons:
 - Hard to set up a web-of-trust model
 - Require recipients setup GPG to open end-to-end encryption of email
 - The plugin breaks after updating the standalone email client

## Hands-on lab – creating your GPG keys

### Hands-on lab – creating your GPG keys

```sh
  #!/bin/bash
  # Create user profile 
  cat > donnie << EOF
     %echo Generating a basic OpenPGP key
     Key-Type: RSA
     Key-Length: 3072
     Subkey-Type: ELG-E
     Subkey-Length: 1024
     Name-Real: Donald A. Tevault
     Name-Comment: No comment
     Name-Email: : donniet@something.net
     Expire-Date: 0
     Passphrase: donnie
     %pubring donnie.pub
     %secring donnie.sec
     %commit
     %echo done
EOF

  gpg --batch --gen-key doonie

  # Verify key
  gpg --list-keys

```

### Hands-on lab – symmetrically encrypting your files

```sh
  if ((`grep -c maggie /etc/passwd` > 0));
      then
          echo "Account: maggie exists";
      else
          echo -e "\n== Register account maggie ==\n"

          if ((`grep -c Ubuntu /etc/os-release` > 0));
            then
              sudo adduser maggie
          else if ((`grep -c CentOS /etc/os-release` > 0))
            then
              sudo useradd maggie
          fi;
          sudo passwd maggie
      fi; 

  # Create file in user home
  su - maggie
  echo "Shhh!!!! This file is super-secret." > ~/maggie/secret_squirrel_stuff.txt
  gpg -c secret_squirrel_stuff.txt # Encrypt

  # Verify
  ls -l
  sleep 1
  clear

  # Uncrypt
  shred -u -z secret_squirrel_stuff.txt
  less secret_squirrel_stuff.txt.gpg # Open file to see inside

  # Create a shared directory, and move the file there for others to access
  sudo mkdir /shared
  sudo chown donnie: /shared
  sudo chmod 755 /shared
  mv ~/secret_squirrel_stuff.txt.gpg /share

  # Check share folder
  cd /shared
  less secret_squirrel_stuff.txt.gpg

  # Decrypt file in order to let other people see it
  gpg -d secret_squirrel_stuff.txt.gp

```

### Hands-on lab – encrypting files with public keys

```sh
  #!/bin/bash
  if ((`grep -c frank /etc/passwd` > 0));
      then
          echo "Account: frank exists";
      else
          echo -e "\n== Register account frank ==\n"

          if ((`grep -c Ubuntu /etc/os-release` > 0));
            then
              sudo adduser frank
          else if ((`grep -c CentOS /etc/os-release` > 0))
            then
              sudo useradd frank
          fi;
          sudo passwd frank
      fi; 

  # Export frank key
  su - frank
  cd .gnupg
  gpg --export -a -o donnie_public-key.txt # user in first lab chapter 5

  # Import frank & donnie key
  gpg --import frank_public-key.txt
  gpg --import donnie_public-key.txt

  # Create a super-secret message for Frank with donnie
  su - donnie
  echo "Frank Siamese (I am a cat.) <frank@any.net>" > ~/secret_stuff_for_frank.txt
  gpg -s -e ~/secret_stuff_for_frank.txt

  # Verify
  ls -l

  # Add donnie public key to the trusted list
  cd .gnupg
  gpg --edit-key donnie # choose option 5

  # Login as frank to check
  su - frank
  gpg -d ~/secret_stuff_for_frank.txt.gpg

```

### Hands-on lab – signing a file without encryption

```sh
  #!/bin/bash
  # Create an unencrypted message for Frank and then sign it
  echo "Good signature from Donald A. Tevault" >> /share/not_secret_for_frank.txt
  gpg -s /share/not_secret_for_frank.txt
  ls -l # Verify

  # Login as frank to open file
  su - frank
  less /share/not_secret_for_frank.txt 

  # verify the signature and extract the document
  gpg --verify /share/not_secret_for_frank.txt.gpg

```

---

## Encrypting partitions with Linux Unified Key Setup (LUKS)

 - Block encryption: whole-disk or individual partitions encryption 
 - File-level encryption: encrypt individual directories 
 - Containerized Encryption: create encrypted, cross-platform containers

## Disk encryption during operating system installation

 - `/` filesystem and the `swap` partition will both be encrypted logical volumes
 - Reboot and type the passphrase
 - Using `sudo lvdisplay` to list all logical volumes

### Hands-on lab – adding an encrypted partition with LUKS

```sh
  #!/bin/bash

  # Install package
  if ((cat /etc/centos-release | grep -c "release 8")); then
    sudo dnf install gdisk;
  else if ((cat /etc/centos-release | grep -c "release 7")); then
    sudo yum install gdisk;
  fi;

  # Open and list available disk
  sudo gdisk /dev/sdb
  sudo gdisk -l /dev/sdb

  # Encrypt disk
  sudo cryptsetup -v -y luksFormat /dev/sdb1
  sudo cryptsetup luksDump /dev/sdb1
  sudo cryptsetup luksOpen /dev/sdb1 secrets

  # Verify
  pwd
  ls -l se*

  # Look at the information
  sudo dmsetup info secrets

  # Format the partition in the usual manner
  sudo mkfs.xfs /dev/mapper/secrets

  # Mount the encrypted partition
  sudo mkdir /secrets
  sudo mount /dev/mapper/secrets /secrets
  mount | grep 'secrets'

``` 

## Configuring the LUKS partition to mount automatically

 - Configure two different files:
   - /etc/crypttab
   - /etc/fstab
 - The UUID line is the `/boot` partition, which is the only part of the drive that isn't encrypted

### Hands-on lab – configuring the LUKS partition to mount automatically

```sh
  sudo cryptsetup luksUUID /dev/sdb1
```

## Encrypting directories with eCryptfs

## Home directory and disk encryption during Ubuntu installation

On the `Partition disks` screen, choose `Guided - use entire disk and set up encrypted LVM` then set a passphrase. Using `cat /etc/crypttab` to view changes

### Hands-on lab – encrypting a home directory for a new user account

```sh
  #!/bin/bash
  # Install ecryptfs-utils on Ubuntu
  PKG_OK=$(dpkg-query -W --showformat='${Status}\n' ecryptfs-utils | grep "install ok installed")
  echo Checking for ecryptfs-utils: $PKG_OK
  if [ "" = "$PKG_OK" ]; then
    echo "No ecryptfs-utils. Setting up ecryptfs-utils."
    sudo apt-get --yes install ecryptfs-utils;
  fi;

  if ((`grep -c goldie /etc/passwd` > 0));
    then
      echo "Account: goldie exists";
    else
      sudo adduser --encrypt-home goldie
  fi;

```

## Creating a private directory within an existing home directory

Keep the 755 permissions settings on their home directories so that other people can access their files and this private directory that nobody but them can access
 - Install the `ecryptfs-utils` package 
 - Create Charlie's account in the normal manner, without the encrypted home directory
 - Log in as Charlie and have him create his private directory
 - For the login passphrase, Charlie enters his normal password or passphrase for logging in to his user account

### Hands-on lab – encrypting other directories with eCryptfs

```sh
  sudo mkdir /secrets
  sudo mount -t ecryptfs /secrets /secrets

```
## Encrypting the swap partition with eCryptfs

Encrypt individual directories with eCryptfs instead of using LUKS whole disk encryption

## Using VeraCrypt for cross-platform sharing of encrypted containers

Allow the sharing of encrypted containers across different operating systems and VeraCrypt does offer more flexibility

### Hands-on lab – getting and installing VeraCrypt

```sh
```

### Hands-on lab – creating and mounting a VeraCrypt volume in console mode

```sh
  veracrypt -c
```
## Using VeraCrypt in GUI mode

## OpenSSL and the public key infrastructure

## Commercial certificate authorities

## Creating keys, certificate signing requests, and certificates

### Creating a self-signed certificate with an RSA key

### Creating a self-signed certificate with an Elliptic Curve key

## Creating an RSA key and a Certificate Signing Request

### Creating an EC key and a CSR

### Creating an on-premises CA

### Hands-on lab – setting up a Dogtag CA

## Adding a CA to an operating system

### Hands-on lab – exporting and importing the Dogtag CA certificate

## Importing the CA into Windows

## OpenSSL and the Apache web server

### Hardening Apache SSL/TLS on Ubuntu

### Hardening Apache SSL/TLS on RHEL 8/CentOS 8

### Hardening Apache SSL/TLS on RHEL 7/CentOS 7

## Setting up mutual authentication



