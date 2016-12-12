# Docker Squid Proxy

This is an Squid-Proxy that act like an 'transparent-proxy' to accelerate the docker-image recontrstuction.

This solution are based on [squid-in-a-can](https://github.com/jpetazzo/squid-in-a-can) project, developed by &copy;[Jason Wilder](https://github.com/jpetazzo).

---

* [Requirements](#requirements)
* [Limitations](#limitations)
* [How-to](#how-to)
* [Example](#example)
* [To-Do](#to-do)

---

### Requirements
* `docker-engine` >= 1.12
* `docker-compose` >= 1.8.1
* `docker-compose` must run as `root` user, to be able to map `161`(udp) port.
* Map `docker.sock`, to be able to access the `docker-engine` API.

---

### Limitations
* SNMP Community harcoded to 'public' for now

---

### How-to

Lo primero que debemos hacer es configurar el composer para que la imagen 'snmp-proxy':

* Tenga mapeado el puerdo 161 (udp)
* Tenga montado el socket del docker-engine.

```yaml
services:
  snmp-proxy:
    image: mgvazquez/snmp-proxy
    hostname: snmp-proxy01
    container_name: snmp-proxy
    ports:
      - "161:161/udp"
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro
```

Luego lo que debemos hacer es configurar cada container al que querramos consultar via SNMP:

* Que levante el SNMP Daemon
* Que exponga el puerdo 161 (udp)
* Que disponibles las OIDs a consultar
* Setear las variables de entorno con las OIDs que expondrá.

```yaml
[...]
snmp-host1:
  image: elcolio/net-snmp
  hostname: snmp-host01
  command: snmpd -Lo -f -V -c /etc/snmp/snmpd.conf
  container_name: snmp-host1
  ports:
    - 161/udp
  environment:
    - SNMPOID_1=.1.3.6.1.2.1.1.5.0
    - SNMPOID_2=.1.3.6.1.2.1.1.6.0
    - SNMPOID_<n>=.x.x.x

[...]
```

---

### Example

```bash
$ sudo docker-compose up
[sudo] password for <user>:
Starting snmp-proxy
Starting snmp-host3
Starting snmp-host1
Starting snmp-host2
Attaching to snmp-proxy, snmp-host3, snmp-host2, snmp-host1
snmp-proxy    | 2016-11-15 19:34:02,628 CRIT Supervisor running as root (no user in config file)
snmp-proxy    | 2016-11-15 19:34:02,629 INFO Included extra file "/etc/supervisord.d/docker-gen.conf" during parsing
snmp-proxy    | 2016-11-15 19:34:02,629 INFO Included extra file "/etc/supervisord.d/snmpd.conf" during parsing
snmp-proxy    | 2016-11-15 19:34:02,635 INFO RPC interface 'supervisor' initialized
snmp-proxy    | 2016-11-15 19:34:02,635 CRIT Server 'unix_http_server' running without any HTTP authentication checking
snmp-proxy    | 2016-11-15 19:34:02,635 INFO supervisord started with pid 1
snmp-host3    | error finding row index in _ifXTable_container_row_restore
snmp-host3    | NET-SNMP version 5.7.2
snmp-host2    | error finding row index in _ifXTable_container_row_restore
snmp-host2    | NET-SNMP version 5.7.2
snmp-host1    | error finding row index in _ifXTable_container_row_restore
snmp-host1    | NET-SNMP version 5.7.2
snmp-proxy    | 2016-11-15 19:34:03,637 INFO spawned: 'snmpd' with pid 17
snmp-proxy    | 2016-11-15 19:34:03,639 INFO spawned: 'docker-gen' with pid 18
snmp-proxy    | 2016-11-15 19:34:03,772 INFO waiting for snmpd to stop
snmp-proxy    | 2016-11-15 19:34:03,776 INFO stopped: snmpd (exit status 0)
snmp-proxy    | 2016-11-15 19:34:03,779 INFO spawned: 'snmpd' with pid 27
snmp-proxy    | 2016-11-15 19:34:04,809 INFO success: snmpd entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
snmp-proxy    | 2016-11-15 19:34:04,809 INFO success: docker-gen entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
[...]
```
---

### To-Do
* Set up SNMP Communities per host (SNMP Contexts)
