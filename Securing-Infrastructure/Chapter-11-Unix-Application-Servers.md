# Chapter 11. Unix Application Servers

## Table of contents

- [Chapter 11. Unix Application Servers](#chapter-11-unix-application-servers)
  - [Table of contents](#table-of-contents)
  - [Keeping Up-to-Date](#keeping-up-to-date)
    - [Third-Party Software Updates](#third-party-software-updates)
    - [Core Operating System Updates](#core-operating-system-updates)


## Keeping Up-to-Date

Many vulnerabilities in an environment can often be remediated purely by keeping a system patched and up-to-date

### Third-Party Software Updates

- The various package management systems are so comprehensive in a modern distribution that for many environments it would be unusual to require anything further
- Sometimes applications need to be installed outside of the package management system

### Core Operating System Updates

The method of upgrading will vary from operating system to operating system, but the upgrade methods fall into two broad buckets:
- Binary update cannot make use of custom compiler options and make assumptions about dependencies, but they require less work in general and are fast to install
- Update from source takes more time and is more complex, however the operating system can include custom compiler optimizations and patches