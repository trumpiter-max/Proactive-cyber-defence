# Chapter 5: Encryption Technologies

Encryption provides three things:
 - Confidentiality
 - Integrity
 - Availability

## Table of content

 - [Chapter 5](Chapter-5-Encryption-Technologies.md)
   - [Table of content](#table-of-content)

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
    gpg --gen-key
```

### Hands-on lab – symmetrically encrypting your files

### Hands-on lab – encrypting files with public keys