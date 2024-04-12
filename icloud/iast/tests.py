from django.test import TestCase

from iast.services.iast_api_service import (
    service_get_target,
    service_new_or_start_target,
)


# Create your tests here.
class TestIastApi(TestCase):
    def test_get_target(self):
        resp = service_get_target("http://192.168.198.138:18664")
        assert resp["status"] == 0

    def test_new_or_start_target(self):
        # resp = service_get_target("http://192.168.198.138:18664")
        resp = service_new_or_start_target(
            "http://192.168.198.138:18664", "192.168.198.137", 8080
        )
        assert resp["status"] == 0 or resp["status"] == 3
