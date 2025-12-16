FROM minio/minio:latest

ENV MINIO_ROOT_USER=minioadmin
ENV MINIO_ROOT_PASSWORD=minioadmin123

VOLUME /data

EXPOSE 9000 9001

# Copy and set up the initialization script
COPY minio.sh /usr/local/bin/minio.sh
RUN chmod +x /usr/local/bin/minio.sh

ENTRYPOINT ["/usr/local/bin/minio.sh"]