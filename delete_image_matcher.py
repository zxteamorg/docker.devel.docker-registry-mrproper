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
