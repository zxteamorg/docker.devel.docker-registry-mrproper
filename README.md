[![Build Status](https://github.com/zxteamorg/docker.devel.docker-registry-mrproper/actions/workflows/build.yml/badge.svg)](https://github.com/zxteamorg/docker.devel.docker-registry-mrproper/actions/workflows/build.yml)
[![Docker Image Version](https://img.shields.io/docker/v/zxteamorg/devel.docker-registry-mrproper?sort=date&label=Version)](https://hub.docker.com/r/zxteamorg/devel.docker-registry-mrproper/tags)
[![Docker Image Size](https://img.shields.io/docker/image-size/zxteamorg/devel.docker-registry-mrproper?label=Image%20Size)](https://hub.docker.com/r/zxteamorg/devel.docker-registry-mrproper/tags)
[![Docker Pulls](https://img.shields.io/docker/pulls/zxteamorg/devel.docker-registry-mrproper?label=Image%20Pulls)](https://hub.docker.com/r/zxteamorg/devel.docker-registry-mrproper)
[![Docker Stars](https://img.shields.io/docker/stars/zxteamorg/devel.docker-registry-mrproper?label=Image%20Stars)](https://hub.docker.com/r/zxteamorg/devel.docker-registry-mrproper)

# Docker Registry MrProper

**Docker Registry MrProper** is a tool to cleanup obsolete images on [API V2 compatible](https://docs.docker.com/registry/spec/api/) Docker Registry

By default it remove all non-latest tags with age 4+ years. See `Customize Delete Tags Matcher` section to change default behaviour.

# Launch

```shell
# Mandatory
export DOCKER_REGISTRY_URL="https://my.docker.registry.local"
export DOCKER_USER="registry-user"
export DOCKER_PASSWORD="registry-password"

# Optional
export DOCKER_REGISTRY_CA_FILE=/path/to/CA.crt
export DOCKER_IMAGES_PREFIX=my/app  # will filter catalog for my/app** images

docker run \
  --rm \
  --interactive \
  --tty \
  --env DOCKER_REGISTRY_URL \
  --env DOCKER_USER \
  --env DOCKER_PASSWORD \
  zxteamorg/devel.docker-registry-mrproper
```

# Customize Delete Tags Matcher

Tags for deletion are matching by a Python's function located in `/usr/local/docker-registry-mrproper/delete_image_matcher.py`.

To change default behaviour you have to replace this file by your own. For example:
- bind your file `delete_image_matcher.py` from host machine via an argument `--volume /path/to/delete_image_matcher.py:/usr/local/docker-registry-mrproper/delete_image_matcher.py`
- extend the image to include your file `delete_image_matcher.py`

Default implementation `/usr/local/docker-registry-mrproper/delete_image_matcher.py` looks like
```python
import datetime

FOUR_YEARS_IN_SECONDS = datetime.timedelta(days=1461).total_seconds() # about 4 years

def delete_image_matcher(image_name: str, image_tags: list[str], image_seconds_age: int) -> bool:
	"""
	A matcher should make decision about image obsoletility.

	The function returns `True` if the image not needed anymore, otherwise `False`.

	Parameters
	----------
	image_name : str
		Name of image (full name from registry root).
	image_tags : list[str]
		List of tags attached to the image.
	image_seconds_age : int
		Number of seconds from creation (pushing) date

	Returns
	-------
	bool `True` - the image not needed anymore (delete it) or `False` - the image still needed (skip deletion).
	"""

	if "latest" in image_tags:
		# Do not delete image that has tag "latest"
		return False

	if image_seconds_age < FOUR_YEARS_IN_SECONDS:
		# Do not delete image less that 4 years age
		return False

	# Delete image in any different cases
	return True
```

# Support

* Maintained by: [ZXTeam](https://zxteam.org)
* Where to get help: [Telegram Channel](https://t.me/zxteamorg)

