# Chapter 6: SSH Hardening

## Table of content

- [Chapter 6: SSH Hardening](#chapter-6-ssh-hardening)
  - [Table of content](#table-of-content)
  - [Ensuring that SSH protocol 1 is disabled](#ensuring-that-ssh-protocol-1-is-disabled)
  - [Creating and managing keys for passwordless logins](#creating-and-managing-keys-for-passwordless-logins)
  - [Creating a user's SSH key set](#creating-a-users-ssh-key-set)
  - [Transferring the public key to the remote server](#transferring-the-public-key-to-the-remote-server)
    - [Hands-on lab – creating and transferring SSH keys](#hands-on-lab--creating-and-transferring-ssh-keys)
  - [Disabling root user login](#disabling-root-user-login)
  - [Disabling username/password logins](#disabling-usernamepassword-logins)
    - [Hands-on lab – disabling root login and password authentication](#hands-on-lab--disabling-root-login-and-password-authentication)
  - [Configuring Secure Shell with strong encryption algorithms](#configuring-secure-shell-with-strong-encryption-algorithms)
  - [Understanding SSH encryption algorithms](#understanding-ssh-encryption-algorithms)
  - [Scanning for enabled SSH algorithms](#scanning-for-enabled-ssh-algorithms)
    - [Hands-on lab – installing and using ssh\_scan](#hands-on-lab--installing-and-using-ssh_scan)
  - [Disabling weak SSH encryption algorithms](#disabling-weak-ssh-encryption-algorithms)
    - [Hands-on lab – disabling weak SSH encryption algorithms – Ubuntu 18.04](#hands-on-lab--disabling-weak-ssh-encryption-algorithms--ubuntu-1804)
    - [Hands-on lab – disabling weak SSH encryption algorithms – CentOS 7](#hands-on-lab--disabling-weak-ssh-encryption-algorithms--centos-7)
  - [Setting system-wide encryption policies on RHEL 8/CentOS 8](#setting-system-wide-encryption-policies-on-rhel-8centos-8)
    - [Hands-on lab – setting encryption policies on CentOS 8](#hands-on-lab--setting-encryption-policies-on-centos-8)
  - [Configuring more detailed logging](#configuring-more-detailed-logging)
    - [Hands-on lab – configuring more verbose SSH logging](#hands-on-lab--configuring-more-verbose-ssh-logging)
  - [Configuring access control with whitelists and TCP Wrappers](#configuring-access-control-with-whitelists-and-tcp-wrappers)
    - [Configuring whitelists within sshd\_config](#configuring-whitelists-within-sshd_config)
    - [Hands-on lab – configuring whitelists within sshd\_config](#hands-on-lab--configuring-whitelists-within-sshd_config)
  - [Configuring whitelists with TCP Wrappers](#configuring-whitelists-with-tcp-wrappers)
  - [Configuring automatic logouts and security banners](#configuring-automatic-logouts-and-security-banners)
    - [Configuring automatic logout for both local and remote users](#configuring-automatic-logout-for-both-local-and-remote-users)
    - [Configuring automatic logout in sshd\_config](#configuring-automatic-logout-in-sshd_config)
    - [Creating a pre-login security banner](#creating-a-pre-login-security-banner)
  - [Configuring other miscellaneous security settings](#configuring-other-miscellaneous-security-settings)
    - [Disabling X11 forwarding](#disabling-x11-forwarding)
    - [Disabling SSH tunneling](#disabling-ssh-tunneling)
    - [Changing the default SSH port](#changing-the-default-ssh-port)
    - [Managing SSH keys](#managing-ssh-keys)
  - [Setting different configurations for different users and groups](#setting-different-configurations-for-different-users-and-groups)
    - [Creating different configurations for different hosts](#creating-different-configurations-for-different-hosts)
    - [Setting up a chroot environment for SFTP users](#setting-up-a-chroot-environment-for-sftp-users)
  - [Creating a group and configuring the sshd\_config file](#creating-a-group-and-configuring-the-sshd_config-file)
    - [Hands-on lab – setting up a chroot directory for the sftpusers group](#hands-on-lab--setting-up-a-chroot-directory-for-the-sftpusers-group)
  - [Sharing a directory with SSHFS](#sharing-a-directory-with-sshfs)
    - [Hands-on lab – sharing a directory with SSHFS](#hands-on-lab--sharing-a-directory-with-sshfs)
  - [Remotely connecting from Windows desktops](#remotely-connecting-from-windows-desktops)

---

## Ensuring that SSH protocol 1 is disabled

Version 1 is severely flawed, the config in /etc/ssh/sshd_config file

## Creating and managing keys for passwordless logins

Prevent these types of attacks:
 - Enabling SSH logins through an exchange of public keys
 - Disabling the root user login through SSH

## Creating a user's SSH key set

 - `National Institute of Standards and Technology (NIST)` uses either an RSA key of at least
3,072 bits or an `Elliptic Curve Digital Signature Algorithm (ECDSA)` key of at least 384 bits
 - Create a 3072 RSA key pair: `ssh-keygen -t rsa -b 3072` then this key will be stored in `.ssh` directory
 - There's some fear that they may be subject to `padding attacks`

## Transferring the public key to the remote server

 - Add the private key to my session keyring. This requires two commands invoke ssh-agent, and add the private key to the keyring
 - Every time the user login this server, requiring to enter the passphrase for the private key

### Hands-on lab – creating and transferring SSH keys

 - From client machine
```sh
  #!/bin/bash
  # Create a pair of 384-bit elliptic curve keys
  ssh-keygen -t ecdsa -b 384
  ls -l ./ssh
  # Add private key to session keyring
  exec /usr/bin/ssh-agent $SHELL 
  ssh-add
```
 - Using `ssh-copy-id` to transfer the public key to the server
 - From server machine
```sh
  #!/bin/bash
  ls -l .ssh
  cat .ssh/authorized_keys
```
 - Log out from the server and close the Terminal window on the client. Open another Terminal window and log in to the server again, then server requires a passphrase
 - Log back out of the server, and add your private key back to the session keyring of the client
```sh
  exec /usr/bin/ssh-agent $SHELL
  ssh-add
```

## Disabling root user login

 - There were three reasons:
   - The internet-facing servers involved were set up to use username/password
authentication for SSH
   - The root user was allowed to log in through SSH
   - User passwords, including the root user's password, were incredibly weak

 - Edit /etc/ssh/sshd_config file on CentOS `#PermitRootLogin yes` to `PermitRootLogin no` or `PermitRootLogin prohibit-password` on Ubunut. Then use command `sudo systemctl restart sshd` to take effect

## Disabling username/password logins

### Hands-on lab – disabling root login and password authentication

## Configuring Secure Shell with strong encryption algorithms

`Commercial National Security Algorithm Suite (CNSA Suite)`, involves using stronger algorithms and longer keys than what using previously

## Understanding SSH encryption algorithms

 - Ciphers: These are the symmetric algorithms that encrypt the data that the client and server exchange with each other
 - HostKeyAlgorithms: This is the list of host key types that the server can use
 - KexAlgorithms: These are the algorithms that the server can use to perform the symmetric key exchange
 - MAC: Message Authentication Codes are hashing algorithms that cryptographically sign the encrypted data in transit. This ensures data integrity and will let you know if someone has tampered with your data

## Scanning for enabled SSH algorithms

- Using `SSHCheck` site [here](https://sshcheck.com/)
- Local scanning tools like ssh_scan

### Hands-on lab – installing and using ssh_scan

```sh
  if ((grep -c ubuntu /etc/os-release));
  then
    sudo apt update & sudo apt install ruby gem;
  else if ((grep -c centos /etc/os-release))
  then
    if ((grep -c VERSION="7 /etc/os-release));
    then
      sudo yum install ruby gem;
    else
      sudo dnf install ruby gem;
    fi;
  fi;

  sudo gem install ssh_scan
  sudo ln -s /usr/local/bin/ssh_scan /usr/bin/ssh_scan
  sudo ssh_scan -h

```

## Disabling weak SSH encryption algorithms

### Hands-on lab – disabling weak SSH encryption algorithms – Ubuntu 18.04

```sh
  #!/bin/bash

  sudo ssh_scan -t <ip-server> -o ~/ssh_scan-7.json

  sed "s/#RekeyLimit default none/
  #RekeyLimit default none

  Ciphers -aes128-ctr,aes192-ctr,aes128-gcm@openssh.com
  KexAlgorithms ecdh-sha2-nistp384
  MACs -hmac-sha1-etm@openssh.com,hmac-sha1,umac-64-
  etm@openssh.com,umac-64@openssh.com,umac-128-
  etm@openssh.com,umac-128@openssh.com,hmac-sha2-256-
  etm@openssh.com,hmac-sha2-256/g" /etc/ssh/sshd_config

  sudo systemctl restart ssh
  sudo systemctl status ssh

  sudo ssh_scan -t <ip-server> -o ~/ssh_scan-7-modified.json

  # Compare 
  diff -y ~/ssh_scan_results-7.json ~/ssh_scan_results-7-modified.json

```

### Hands-on lab – disabling weak SSH encryption algorithms – CentOS 7

```sh
  #!/bin/bash

  sudo ssh_scan -t <ip-server> -o ~/ssh_scan-53.json

  sed "s/#RekeyLimit default none/#RekeyLimit default none

  Ciphers aes256-gcm@openssh.com,aes256-ctr,chacha20-poly1305@openssh.com

  KexAlgorithms ecdh-sha2-nistp384
  MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-256/g" /etc/ssh/sshd_config

  sudo systemctl restart sshd
  sudo systemctl status sshd

  sudo ssh_scan -t <ip-server> -o ~/ssh_scan-53-modified.json

  # Compare
  diff -y ssh_scan_results-53.json ssh_scan_results-53-modified.json
```

## Setting system-wide encryption policies on RHEL 8/CentOS 8

 - Look in the /etc/crypto-policies/back-ends/ directory 
 - DEFAULT configuration shows that quite a few older algorithms are still enabled

### Hands-on lab – setting encryption policies on CentOS 8

```sh
  #!/bin/bash

  sudo update-crypto-policies --show

  sudo ssh_scan -t <ip-server> -o ssh_scan-161.json

  sudo update-crypto-policies --set FUTURE
  sudo shutdown -r now

  sudo ssh_scan -t <ip-server> -o ssh_scan_results-161-FUTURE.json
  ls -l /etc/crypto-policies/back-ends/
  sudo fips-mode-setup --check
  sudo fips-mode-setup --enable
  sudo shutdown -r now
  sudo fips-mode-setup --check
  sudo ssh_scan -t <ip-server> -o ssh_scan_results-161-FIPS.json
  ls -l /etc/crypto-policies/back-ends/

```
## Configuring more detailed logging

The entry is made in the /var/log/auth.log file on Debian/Ubuntu and /var/log/secure file on Red Hat/CentOS systems  

### Hands-on lab – configuring more verbose SSH logging

```sh
  #!/bin/bash

  # Change log level to DEBUG3
  if ((grep -c ubuntu /etc/os-release));
  then
    sudo less /var/log/auth.log
    sed "s/#LogLevel INFO/LogLevel DEBUG3/" /etc/ssh/sshd_config
    sudo systemctl restart ssh
    sudo less /var/log/auth.log
  else if ((grep -c centos /etc/os-release))
  then
    sudo less /var/log/secure
    sed "s/#LogLevel INFO/LogLevel DEBUG3/" /etc/ssh/sshd_config
    sudo systemctl restart sshd
    sudo less /var/log/secure
  fi;

  # Change log level to VERBOSE - log the fingerprint of any key used to log in
  if ((grep -c ubuntu /etc/os-release));
  then
    sudo less /var/log/auth.log
    sed "s/#LogLevel INFO/LogLevel VERBOSE/" /etc/ssh/sshd_config
    sudo systemctl restart ssh
    sudo less /var/log/auth.log
  else if ((grep -c centos /etc/os-release))
  then
    sudo less /var/log/secure
    sed "s/#LogLevel INFO/LogLevel VERBOSE/" /etc/ssh/sshd_config
    sudo systemctl restart sshd
    sudo less /var/log/secure
  fi;

```

## Configuring access control with whitelists and TCP Wrappers

 - Whitelists within the sshd_config file
 - TCP Wrappers, via the /etc/hosts.allow and /etc/hosts.deny files

### Configuring whitelists within sshd_config

Four access control directives:
 - DenyUsers
 - AllowUsers
 - DenyGroups
 - AllowGroups

### Hands-on lab – configuring whitelists within sshd_config

```sh
  users=(frank charlie maggie);

  for user in "${users[@]}";
  do
      if ((`grep -c $user /etc/passwd` > 0));
      then
          echo "Account: $user exists";
      else
          if ((grep -c ubuntu /etc/os-release));
            then
              sudo adduser $user
            else if ((grep -c centos /etc/os-release))
            then
              sudo useradd $user
          fi;
          sudo passwd $user
      fi;
  done

  # Set permission
  sudo groupadd webadmins
  sudo usermod -a -G webadmins frank
  sudo echo "AllowUsers donnie" >> /etc/ssh/sshd_config

  if ((grep -c ubuntu /etc/os-release));
    then
      sudo systemctl restart ssh
      sudo systemctl status ssh
  else if ((grep -c centos /etc/os-release));
    then
      sudo systemctl restart sshd
      sudo systemctl status sshd
  fi;
  
  sudo echo "AllowGroups webadmins" >> /etc/ssh/sshd_config

```

## Configuring whitelists with TCP Wrappers

Whitelists and blacklists are configured in the /etc/hosts.allow file and the /etc/hosts.deny

## Configuring automatic logouts and security banners

### Configuring automatic logout for both local and remote users

Create the autologout.sh file in /etc/profile.d/ directory 
```sh
  TMOUT=100
  readonly TMOUT
  export TMOUT
```

Allow the file to run `sudo chmod +x autologout.sh` then machine forces the user logs in again after 100 seconds

### Configuring automatic logout in sshd_config

Change the value of /etc/ssh/sshd_config to set timeout in 100 seconds 
```
  ClientAliveInterval 100
  ClientAliveCountMax 0
```

### Creating a pre-login security banner

 - Create the /etc/ssh/sshd-banner file with the message
 - Edit /etc/ssh/sshd_config file to `Banner /etc/ssh/sshd-banner`

## Configuring other miscellaneous security settings

### Disabling X11 forwarding

Edit sshd_config file to `X11Forwarding no`

### Disabling SSH tunneling

Edit sshd_config file to
```
  AllowTcpForwarding no
  AllowStreamLocalForwarding no
  GatewayPorts no
  PermitTunnel no

```

### Changing the default SSH port

Uncomment the `#Port 22` line in sshd_config, and change the port number

### Managing SSH keys

 - Disable username/password authentication on the server
 - The handle to keep track of keys is to move everyone's authorized_keys file to one central location
 - Find more [here](https://www.ssh.com/iam/ssh-key-management)

## Setting different configurations for different users and groups

 - Match User or Match Group directive to set up 
custom configurations for certain users or groups
 - Set up a custom configuration for a group, just replace Match User with Match Group, and supply a group name instead of a user name

### Creating different configurations for different hosts

 - Created either a DNS record or an /etc/hosts file entry for servers
 - Create custom configurations for other hosts, just add a stanza for each one to ~/.ssh/config file

### Setting up a chroot environment for SFTP users

- A great tool for performing secure file transfers
- Able to log in through either SSH or SFTP and can navigate through the server's entire filesystem

## Creating a group and configuring the sshd_config file

```sh
  #!/bin/bash

  sudo groupadd sftpusers
  sudo useradd -G sftpusers max
  sudo useradd -m -d /home/max -s /bin/bash -G sftpusers max

  sudo sed "s/Subsystem sftp \usr\lib\openssh\sftp-server / Subsystem sftp internal-sftp/" /etc/ssh/sshd_config

  echo -e "Match Group sftpusers
  ChrootDirectory /home
  AllowTCPForwarding no
  AllowAgentForwarding no
  X11Forwarding no
  ForceCommand internal-sftp" >> /etc/sshd_config

```

### Hands-on lab – setting up a chroot directory for the sftpusers group

```sh
  #!/bin/bash

  # Create group and account max
  sudo groupadd sftpusers

  if ((grep -c ubuntu /etc/os-release));
    then
      sudo useradd -m -d /home/max -s /bin/bash -G sftpusers max
      sudo chmod 700 /home/*;
  else if ((grep -c centos /etc/os-release));
    then
      sudo useradd -G sftpusers max;
  fi;

  sudo sed "s/Subsystem sftp \usr\lib\openssh\sftp-server / Subsystem sftp internal-sftp/" /etc/ssh/sshd_config

  echo -e "Match Group sftpusers
  ChrootDirectory /home
  AllowTCPForwarding no
  AllowAgentForwarding no
  X11Forwarding no
  ForceCommand internal-sftp" >> /etc/sshd_config

  if ((grep -c ubuntu /etc/os-release));
    then
      sudo systemctl ssh restart;
  else if ((grep -c centos /etc/os-release));
    then
      sudo systemctl sshd restart;
  fi;

```

## Sharing a directory with SSHFS

 - Its network traffic is encrypted by default, unlike with NFS or Samba
 - It is especially handy for accessing a directory on a cloud-based `Virtual Private Server (VPS)`

### Hands-on lab – sharing a directory with SSHFS

```sh
  #!/bin/bash

  # Create a mount-point directory and install sshfs
  mkdir remote

  if ((grep -c ubuntu /etc/os-release));
    then
      PKG_OK=$(dpkg-query -W --showformat='${Status}\n' sshfs|grep "install ok installed")
      echo Checking for sshfs: $PKG_OK
      if [ "" = "$PKG_OK" ]; then
        echo "No sshfs. Setting up sshfs."
        sudo apt-get --yes install sshfs;
      fi;
  else if ((grep -c centos /etc/os-release));
    then
      PKG_OK=$(yum list installed | grep fuse-sshfs | grep "install ok installed")
      echo Checking for fuse-sshfs: $PKG_OK
      if [ "" = "$PKG_OK" ]; then
        echo "No fuse-sshfs. Setting up fuse-sshfs."
        sudo yum install --yes fuse-sshfs;
      fi;
  fi;

```

## Remotely connecting from Windows desktops

Using a Terminal program, rather than a full-blown Bash Shell such as `Cygwin` or `PuTTY`
