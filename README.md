# host-scanner

Automated host scanner

## Examples

```sh
./host-scanner.py -o /tmp/ -t 10.211.55.4 -v
INFO:host-scanner:Starting TCP service enumeration on 10.211.55.4
DEBUG:host-scanner:Creating folder /tmp//10.211.55.4/nmap
DEBUG:host-scanner:nmap -Pn -sV -O -T4 -p- -oA /tmp//10.211.55.4/nmap/10.211.55.4
INFO:host-scanner:Starting UDP service enumeration on 10.211.55.4 [top 200 ports]
DEBUG:host-scanner:nmap -n -Pn -sC -sU --top-ports 200 -T4 -oA /tmp//10.211.55.4/nmap/10.211.55.4-UDP
DEBUG:host-scanner:Service found    22/tcp ssh
DEBUG:host-scanner:Service found  8123/tcp http-proxy
INFO:host-scanner:Analyzing found services
DEBUG:host-scanner:Creating folder /tmp//10.211.55.4/22-ssh
INFO:host-scanner:Starting ssh on 10.211.55.4 for service ssh
DEBUG:ssh:Grabbing SSH banner
```

## Available plugins
* dirsearch
* nikto
* DNS AXFR
* nmap NSE scripts
* SAM dump
* SMTP VRFY
* SSH banner grab
* testssl.sh

## Dependencies
* paramiko (https://github.com/paramiko/paramiko)
* python-libnmap (https://github.com/savon-noir/python-libnmap)