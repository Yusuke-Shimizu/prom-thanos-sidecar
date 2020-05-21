FROM thanosio/thanos:v0.10.1 as thanos

FROM alpine:3.10.2 as alpine
RUN apk add gettext

# Copy exe file from thanos to alpine container
COPY --from=thanos /bin/thanos /bin/thanos

# Copy files from local to container
ADD bucket_config_original.yaml /etc/thanos/bucket_config_original.yaml
ADD entrypoint.sh /etc/thanos/entrypoint.sh

RUN chmod +x /bin/thanos /etc/thanos/entrypoint.sh

ENTRYPOINT "/etc/thanos/entrypoint.sh"
