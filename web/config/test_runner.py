from django.test.runner import DiscoverRunner
from django.test.utils import override_settings


class Runner(DiscoverRunner):
    """Rate limits off for the suite (counts would leak between tests through the shared cache).
    The tests of the limiter itself switch them back on with override_settings and clear the cache."""

    def setup_test_environment(self, **kw):
        super().setup_test_environment(**kw)
        self._limits = override_settings(RATELIMIT_ENABLED=False)
        self._limits.enable()

    def teardown_test_environment(self, **kw):
        self._limits.disable()
        super().teardown_test_environment(**kw)
