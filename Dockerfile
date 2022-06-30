ARG IMAGE=python:3.10-alpine3.15


FROM ${IMAGE} AS builder
WORKDIR /stage/usr/local/docker-registry-mrproper
COPY requirements.txt .
COPY LICENSE .
COPY README.md .
COPY NOTICE .
COPY delete_image_matcher.py .
COPY docker_registry_mrproper.py .
COPY docker-entrypoint.sh /stage/usr/local/bin/


FROM ${IMAGE}
COPY --from=builder /stage /
RUN \
  cd /usr/local/docker-registry-mrproper && \
  python3 -m venv .venv && \
  source .venv/bin/activate && \
  pip install --upgrade pip && \
  pip install --requirement requirements.txt

# Mandatory
ENV DOCKER_REGISTRY_URL=
ENV DOCKER_USER=
ENV DOCKER_PASSWORD=
# Optional
ENV DOCKER_REGISTRY_CA_FILE=
ENV DOCKER_IMAGES_PREFIX=

CMD [ "/usr/local/bin/docker-entrypoint.sh" ]
