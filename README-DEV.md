# Docker Registry MrProper

### Quick Start

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install --requirement requirements.txt
```

### Launch

```shell
# Mandatory
export DOCKER_REGISTRY_URL="https://my.docker.registry.local"
export DOCKER_USER="registry-user"
export DOCKER_PASSWORD="registry-password"

# Optional
export DOCKER_REGISTRY_CA_FILE=/path/to/CA.crt
export DOCKER_IMAGES_PREFIX=my/app  # will filter catalog for my/app** images

./docker_registry_mrproper.py | tee cleanup.log
```

### Build Image

```shell
docker build --tag zxteamorg/devel.docker-registry-mrproper .
```

### Re-new requirements.txt

```shell
python3 -m pip freeze > requirements.txt
```

### References

* https://docs.docker.com/registry/spec/api/

