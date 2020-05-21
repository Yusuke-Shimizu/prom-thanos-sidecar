FROM prom/prometheus as prom

FROM alpine:3.10.2 as alpine
RUN apk add gettext

COPY --from=prom /bin/prometheus /bin/prometheus

RUN mkdir -p /prometheus /etc/prometheus && \
chown -R nobody:nogroup etc/prometheus /prometheus

ADD prometheus.template.yml /etc/prometheus/prometheus.template.yml
ADD alert_rules.yml /etc/prometheus/alert.rules

ADD entrypoint.sh /etc/prometheus/entrypoint.sh
RUN chmod +x /etc/prometheus/entrypoint.sh
ENTRYPOINT ["/etc/prometheus/entrypoint.sh"]

USER nobody
EXPOSE 9090
VOLUME [ "/prometheus" ]
WORKDIR /prometheus

