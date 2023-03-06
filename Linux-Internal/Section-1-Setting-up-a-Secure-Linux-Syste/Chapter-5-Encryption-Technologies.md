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
  gpg -s not_secret_for_frank.txt
  ls -l # Verify

```

---

## Encrypting partitions with Linux Unified Key Setup (LUKS)

 - Block encryption: whole-disk or individual partitions encryption 
 - File-level encryption: encrypt individual directories 
 - Containerized Encryption: create encrypted, cross-platform containers

## Disk encryption during operating system installation

### Hands-on lab – adding an encrypted partition with LUKS

## Configuring the LUKS partition to mount automatically

### Hands-on lab – configuring the LUKS partition to mount automatically

## Encrypting directories with eCryptfs

## Home directory and disk encryption during Ubuntu installation
