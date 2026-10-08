from django.contrib.staticfiles.apps import StaticFilesConfig


class CalcStaticFilesConfig(StaticFilesConfig):
    """collectstatic skips the lesson videos (about a gigabyte). nginx serves them from VIDEO_DIR directly,
    and hashing them into a manifest would only double the disk they use."""
    ignore_patterns = StaticFilesConfig.ignore_patterns + ["video", "video/*"]
