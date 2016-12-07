FROM alpine:3.4
MAINTAINER Manuel Andres Garcia Vazquez "<mvazquez@scabb-island.com.ar>"

ARG PYTHON_VERSION
ARG IPTABLES_VERSION
ARG SQUID_VERSION
ARG DUMB_INIT
ARG SQUID_PORT

ENV PYTHON_VERSION=${PYTHON_VERSION:-2.7.12-r0}
ENV IPTABLES_VERSION=${IPTABLES_VERSION:-1.6.0-r0}
ENV SQUID_VERSION=${SQUID_VERSION:-3.5.20-r0}
ENV SQUID_PORT=${SQUID_PORT:-3128}
ENV DUMB_INIT=${DUMB_INIT:-1.2.0}
ENV PYTHONUNBUFFERED=1

EXPOSE ${SQUID_PORT}

WORKDIR /tmp
ADD extras/squid.py /bin/
ADD extras/squid.conf /etc/squid/
ADD extras/squid.d /etc/squid/squid.d

# ------ https://github.com/Yelp/dumb-init ------
ADD https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT}/dumb-init_${DUMB_INIT}_amd64 /bin/dumb-init
# -----------------------------------------------

RUN echo -e "\
http://dl-4.alpinelinux.org/alpine/latest-stable/main\n\
@testing http://dl-4.alpinelinux.org/alpine/edge/testing" > /etc/apk/repositories &&\
    apk add --update \
      iptables=${IPTABLES_VERSION} \
      squid=${SQUID_VERSION} \
      python=${PYTHON_VERSION}

RUN rm -rf /var/cache/apk/* &&\
    mkdir -p /etc/squid/squid.d &&\
    chmod 777 /etc/squid/squid.d &&\
    chmod a+x /bin/dumb-init &&\
    chmod a+x /bin/squid.py

USER squid

ENTRYPOINT ["/bin/dumb-init"]
CMD ["/bin/squid.py"]
