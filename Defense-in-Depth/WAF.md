# Web application firewall

A security solution on the web application level which - from a technical point of view - does not depend on the application itself

## Table of contents

- [Web application firewall](#web-application-firewall)
  - [Table of contents](#table-of-contents)
  - [Introduction](#introduction)
    - [Functionality](#functionality)
    - [Key Features](#key-features)
  - [ModSecurity](#modsecurity)
  - [Overall](#overall)
    - [Features](#features)
    - [Mechanism](#mechanism)
      - [Phase 1: Request Headers](#phase-1-request-headers)
      - [Phase 2: Request Body](#phase-2-request-body)
      - [Phase 3: Response Headers](#phase-3-response-headers)
      - [Phase 4: Response Body](#phase-4-response-body)
  - [Hand-on labs](#hand-on-labs)
    - [Setup victim](#setup-victim)
    - [Setup rules](#setup-rules)
    - [Result](#result)
      - [Sql injection](#sql-injection)

## Introduction

### Functionality

WAFs analyze HTTP and HTTPS traffic between clients and web applications, examining requests and responses to identify and block potentially harmful activities

### Key Features

- `Application Layer Protection` focuses on the application layer of the OSI model, providing granular inspection of web traffic to detect and mitigate vulnerabilities and attacks
- `Attack Detection and Prevention` employes various techniques, such as signature-based detection, anomaly detection, and behavioral analysis, to identify and block common attacks like SQL injection, cross-site scripting (XSS), and more
- `Security Policies and Rule Sets` allows administrators to define customized security policies and rule sets to enforce specific security requirements and mitigate known threats
- `Logging and Reporting` generates detailed logs and reports, offering insights into detected attacks, blocked traffic, and potential vulnerabilities for analysis and auditing purposes

## ModSecurity

An open-source Web Application Firewall module that can be deployed on popular web servers like IIS, Apache and Nginx

![](https://sysally.com/wp-content/uploads/2019/01/Modsecurity.png)

## Overall

### Features

- `Rules-Based Security` utilizes a rule-based engine to define and enforce security policies. It comes with a wide range of preconfigured rules and allows for custom rule creation
- `Extensibility` supports custom rule sets and allows developers to create and implement their own security rules tailored to their specific web applications
-  `Integration` can be integrated with other security tools and services, such as intrusion detection systems (IDS) and security information and event management (SIEM) systems, for enhanced threat detection and incident response capabilities
- `Flexibility` offers fine-grained control over security configurations, enabling administrators to adjust rule thresholds, whitelist trusted sources, and customize response actions

### Mechanism

![](https://1.bp.blogspot.com/-WbBhBMSXvCY/WAOzRxAbtGI/AAAAAAAAGF4/BepC0Hv8lwQLXgwoLDA4wjYjPorTWLsFQCLcB/s1600/2.jpg)

ModSecurity handles requests and responses during each phase:

#### Phase 1: Request Headers

- Examining the incoming request headers, such as the HTTP method, URL, and other metadata
- Performing rule-based analysis and evaluates predefined rules or custom rule sets to detect potential security issues
- Rules can include checks for SQL injection, cross-site scripting (XSS), file inclusion vulnerabilities, and more

#### Phase 2: Request Body

If the request contains a body, ModSecurity inspects the request payload. It analyzes the data and applies rules to detect and prevent malicious content or suspicious patterns.This phase is particularly useful for detecting attacks like command injection or data exfiltration

#### Phase 3: Response Headers

ModSecurity analyzes the headers in the server's response to the client. It can detect issues like missing security headers, suspicious server software versions, or other security-related information leakage

#### Phase 4: Response Body

If the response contains a body, ModSecurity inspects it. It looks for potential security vulnerabilities or suspicious patterns, such as malicious JavaScript code, phishing attempts, or unauthorized content disclosure. Content modification or blocking can be applied based on predefined rules or custom configurations. During each phase, ModSecurity evaluates rules based on regular expressions, string matching, or other techniques to identify potential threats. When a rule matches, ModSecurity can take various actions, including blocking the request/response, modifying the content, or logging the event for further analysis

## Hand-on labs

### Setup victim

[DVWA](https://github.com/digininja/DVWA) is used as victim, and setup with Ubuntu 20.04 LTS

```sh
    # Create web folder and download DVWA
    sudo mkdir /var/www/html 
    cd mkdir/var/www/html 
    sudo apt install git -y
    git clone https://github.com/digininja/DVWA.git
    mv DVWA dvwa 

    sudo chmod -R 777 dvwa
    cd dvwa/config
    sudo cp config.inc.php.dist config.inc.php
    sudo nano config.inc.php # modify config of dvwa

    # Install dependent
    sudo apt install lsb-release apt-transport-https ca-certificates default-mysql-server php php-gd -y

    # Then change config of php
    cd /etc/php/7.4/apache2 # change 7.4 to specific version
    sudo nano php.ini
    # Change allow_url_fopen = On, allow_url_include = On, and uncomment extension=pdo_mysql, extension=mysql
    sudo systemctl start apache2

    # Config mysql server
    sudo systemctl start mysql
    systemctl status mysql
    sudo mysql -u root -p
    create user 'name_of_user_db_of_above_config'@'127.0.0.1' identified by "name_of_password_db_of_above_config";
    grant all privileges on dvwa.* to 'name_of_user_db_of_above_config'@'127.0.0.1'
```

### Setup rules

Install ModSecurity with command

```sh   
    # Install dependent
    sudo apt install libapache2-mod-security2 -y
    sudo a2enmod headers
    systemctl restart apache2

    # Config 
    sudo cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
    sudo nano /etc/modsecurity/modsecurity.conf
    # Chang SecRuleEngine On, default is DetectionOnly
    sudo systemctl restart apache2

    # Install core rule set of OWASP
    sudo git clone https://github.com/coreruleset/coreruleset /usr/share/modsecurity-crs
    sudo mv /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf
    # Rename rule
    sudo mv /usr/share/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example /usr/share/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf

    # Enable 
    sudo nano /etc/apache2/mods-available/security2.conf
    # Then make this file include 3 lines
    # SecDataDir /var/cache/modsecurity
    # Include /usr/share/modsecurity-crs/crs-setup.conf
    # Include /usr/share/modsecurity-crs/rules/*.conf

    # Config apache and add line # SecRuleEngine On
    sudo nano /etc/apache2/sites-enabled/000-default.conf
```

However, another simple method is using docker from [here](/Defense-in-Depth/Material/modsecurity-docker/)

### Result

#### Sql injection

![](https://i.ibb.co/cQ4y5Mv/Screenshot-2023-05-12-105709.png)