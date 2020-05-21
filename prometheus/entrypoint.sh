#!/bin/sh

envsubst < /etc/prometheus/prometheus.template.yml > /etc/prometheus/prometheus.yml && \
/bin/prometheus \
    --config.file=/etc/prometheus/prometheus.yml \
    --storage.tsdb.path=/prometheus \
    --web.console.libraries=/usr/share/prometheus/console_libraries \
    --web.console.templates=/usr/share/prometheus/consoles \
    --storage.tsdb.retention=200h \
    --storage.tsdb.max-block-duration=2h \
    --storage.tsdb.min-block-duration=2h
