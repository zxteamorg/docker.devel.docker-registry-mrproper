#!/usr/bin/env python
#
from typing import Optional
import requests 
from requests.auth import HTTPBasicAuth
from os import environ
import sys
import datetime

from delete_image_matcher import delete_image_matcher

class ImageInfo(object):
	def __init__(self, name: str, seconds_age: int, digest: str) -> None:
		self.name = name
		self.seconds_age = seconds_age
		self.digest = digest
		self.tags = []
	pass

def main(registry_url: str, user: str, password: str, registry_ca_file: Optional[str] = None, images_prefix: Optional[str] = None):
	try:
		now = datetime.datetime.now()

		credentials = HTTPBasicAuth(user, password)

		verify = False
		if registry_ca_file is not None:
			verify = registry_ca_file

		print("Scanning repository on %s ..." % (registry_url), flush=True)
		catalog_api_url = registry_url + "/v2/_catalog"

		catalog_response = requests.get(catalog_api_url, auth = credentials, verify=verify)
		if catalog_response.status_code != 200:
			raise Exception("Unable to get repository catalog by GET %s. HTTP Code: %s" % (catalog_api_url, catalog_response.status_code))
		catalog = catalog_response.json()
		repositories = catalog['repositories']
		for repo_name in repositories:
			if images_prefix is not None:
				if not repo_name.startswith(images_prefix):
					continue

			images: dict[str, dict[str, ImageInfo]] = {}

			print("Fetching tags for image '%s' ..." % (repo_name), flush=True)
			tag_api_url= registry_url + "/v2/%s/tags/list" % repo_name
			tag_response = requests.get(tag_api_url, auth = credentials, verify=verify)
			catalog_tag_list = tag_response.json()
			catalog_name = catalog_tag_list['name']

			for tag_name in catalog_tag_list['tags']:
				manifest_api_url = registry_url + "/v2/%s/manifests/%s" % (catalog_name, tag_name)  
				headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
				fetch_manifest_response = requests.head(manifest_api_url, headers = headers, auth = credentials, verify=verify)
				digest = fetch_manifest_response.headers['Docker-Content-Digest']
				last_modified_str = fetch_manifest_response.headers['Last-Modified']
				last_modified = datetime.datetime.strptime(last_modified_str, "%a, %d %b %Y %H:%M:%S %Z")
				age = now - last_modified

				if digest not in images:
					images[digest] = { catalog_name:  ImageInfo(catalog_name, age.total_seconds(), digest) }

				if catalog_name not in images[digest]:
					images[digest][catalog_name] = ImageInfo(catalog_name, age.total_seconds(), digest)

				if images[digest][catalog_name].seconds_age < age.total_seconds():
					images[digest][catalog_name].seconds_age = age.total_seconds() # Use oldest

				images[digest][catalog_name].tags.append(tag_name)

			for digest in images:
				named_images: dict[str, ImageInfo] = images[digest]
				for image_name in named_images:
					image_info: ImageInfo = named_images[image_name]
					if delete_image_matcher(image_info.name, image_info.tags, image_info.seconds_age):
						print("Deleting %s:%s ... " % (image_info.name, ",".join(image_info.tags)), end="", flush=True)
						delete_manifest_api_url = registry_url + "/v2/%s/manifests/%s" % (catalog_name, digest)  
						delete_manifest_response = requests.delete(delete_manifest_api_url, auth = credentials, verify=verify)
						if delete_manifest_response.status_code != 202:
							raise Exception("Unable to delete image %s:%s. HTTP Code: %s" % (catalog_name, tag_name, delete_manifest_response.status_code))
						print("OK", flush=True)

		print("Cleanup done successfully", flush=True)
	except Exception as ex:
		print("Attempt failure. {0}".format(ex.with_traceback()), file=sys.stderr)

def _get_environ_variable(name: str, exit_code: int):
	value = environ.get(name, None)
	if value is None:
		print("A required environment variable '%s' is not set." % name, file=sys.stderr)
		sys.exit(exit_code)
	return value

if __name__ == "__main__":
	import sys

	registry_url = _get_environ_variable("DOCKER_REGISTRY_URL", 1)
	user = _get_environ_variable("DOCKER_USER", 2)
	password = _get_environ_variable("DOCKER_PASSWORD", 3)
	registry_ca_file =  environ.get("DOCKER_REGISTRY_CA_FILE", None)
	images_prefix = environ.get("DOCKER_IMAGES_PREFIX", None)

	# launch application loop
	main(registry_url, user, password, registry_ca_file=registry_ca_file, images_prefix=images_prefix)
