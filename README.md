# Docker Squid Proxy

This is an Squid-Proxy that act like an 'transparent-proxy' to accelerate the docker-image reconstruction.

This solution are based on [squid-in-a-can](https://github.com/jpetazzo/squid-in-a-can) project, developed by &copy;[Jérôme Petazzoni](https://github.com/jpetazzo).

---

* [Docker Image](#docker-image)
* [Requirements](#requirements)
* [Limitations](#limitations)
* [How-to](#how-to)
* [To-Do](#to-do)

---
### Docker Image

[![](https://images.microbadger.com/badges/version/mgvazquez/squid-proxy.svg)](https://microbadger.com/images/mgvazquez/squid-proxy "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/mgvazquez/squid-proxy.svg)](https://microbadger.com/images/mgvazquez/squid-proxy "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/commit/mgvazquez/squid-proxy.svg)](https://microbadger.com/images/mgvazquez/squid-proxy "Get your own commit badge on microbadger.com") [![](https://images.microbadger.com/badges/license/mgvazquez/squid-proxy.svg)](https://microbadger.com/images/mgvazquez/squid-proxy "Get your own license badge on microbadger.com")

---

### Requirements
* `docker-engine` >= 1.12
* `docker-compose` >= 1.8.1
* `docker run` need `--privileged` and `--network host` flag.

---

### Limitations
* Can't handle [HTTPS](http://wiki.squid-cache.org/Features/HTTPS) for now.

---

### How-to

#### Manually (with `docker run`)

You can manually run these commands:

```bash
docker run -d --privileged --network host mgvazquez/squid-proxy
```

#### Run via docker-compose

There is a `docker-compose.yml` file to enable launching via [docker compose](https://docs.docker.com/compose/).
To use this you will need a
local checkout of this repo and have `docker` and `compose` installed.

> Run the following command in the same directory as the `docker-compose.yml` file:

```bash
 docker-compose up
```

You can customize the `docker-compose.yml`:

```yaml
version: '2'

volumes:
  squid_cache:

services:
  squid-proxy:
    image: mgvazquez/squid-proxy
    hostname: squid-proxy
    container_name: squid-proxy
    network_mode: host
    privileged: true
    volumes:
      - squid_cache:/var/cache/squid
      - /etc/localtime:/etc/localtime
    environment:
      - SQUID_LISTEN_PORT=3128
      - SQUID_MAX_CACHE_SIZE=5000
      - SQUID_MAX_CACHE_OBJECT=1024
```

#### Tuning

The docker image can be tuned using environment variables.

###### SQUID_LISTEN_PORT
Squid listening port. Use the `-e SQUID_LISTEN_PORT=1024` to set the listening port.

###### SQUID_MAX_CACHE_OBJECT
Squid has a maximum object cache size. Often when caching debian packages vs standard web content it is valuable to increase this size. Use the `-e SQUID_MAX_CACHE_OBJECT=1024` to set the max object size (in MB).

###### SQUID_MAX_CACHE_SIZE
The squid disk cache size can be tuned. Use `-e SQUID_MAX_CACHE_SIZE=5000` to set the disk cache size (in MB).

---

### To-Do
* To handle [HTTPS](http://wiki.squid-cache.org/Features/HTTPS) requests with custom trusted certificates.

---

<p align="center"><img src="http://www.catb.org/hacker-emblem/glider.png" alt="hacker emblem"></p>
