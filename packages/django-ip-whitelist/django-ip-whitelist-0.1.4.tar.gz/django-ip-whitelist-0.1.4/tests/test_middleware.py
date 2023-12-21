from django.core.exceptions import PermissionDenied
from django.test import TestCase, override_settings
from django.urls import reverse

from ip_whitelist.middleware import IPWhiteListMiddleware
from ip_whitelist.models import AllowedIP, AllowedIPRange

from .mocks import Request, get_response


class IPWhiteListMiddlewareTestCase(TestCase):
    def setUp(self):
        AllowedIP.objects.create(address="127.0.0.1")
        AllowedIPRange.objects.create(range="192.168.0.0/28")

        self.instance = IPWhiteListMiddleware(get_response=get_response)

    def test_middleware_remote_address(self):
        path = reverse("admin:index")
        request = Request({"REMOTE_ADDR": "127.0.0.1"}, path)
        response = self.instance(request)

        self.assertTrue(request.ip_allowed)
        self.assertEqual(response, "success")

    def test_middleware_forwarded_ip(self):
        path = reverse("admin:index")
        request = Request({"HTTP_X_FORWARDED_FOR": "178.23.123.11,192.168.0.13"}, path)
        response = self.instance(request)

        self.assertTrue(request.ip_allowed)
        self.assertEqual(response, "success")

    def test_middleware_outside_ip(self):
        path = reverse("admin:index")
        request = Request({"REMOTE_ADDR": "192.168.1.1"}, path)
        with self.assertRaises(PermissionDenied):
            request = self.instance(request)

        self.assertFalse(request.ip_allowed)

    def test_outside_ip_in_allowed_and_disallowed_paths(self):
        path = reverse("dashboard")
        request = Request({"REMOTE_ADDR": "192.168.1.1"}, path, authenticated=False)
        response = self.instance(request)

        self.assertTrue(request.ip_allowed)
        self.assertEqual(response, "success")

        request_path = reverse("admin:index")
        request = Request(
            {"REMOTE_ADDR": "192.168.1.1"}, request_path, authenticated=False
        )

        with self.assertRaises(PermissionDenied):
            self.instance(request)
        self.assertFalse(request.ip_allowed)

    @override_settings(WHITELIST_IP_RANGES=["192.168.1.0/24"])
    def test_whitelisted_ip_ranges(self):
        path = reverse("admin:index")
        request = Request(
            {"REMOTE_ADDR": "192.168.2.1"}, path, authenticated=False
        )

        with self.assertRaises(PermissionDenied):
            self.instance(request)

        request = Request({"REMOTE_ADDR": "192.168.1.1"}, path, authenticated=False)
        response = self.instance(request)
        self.assertTrue(request.ip_allowed)
        self.assertEqual(response, "success")

        request = Request({"REMOTE_ADDR": "192.168.1.255"}, path, authenticated=False)
        response = self.instance(request)
        self.assertTrue(request.ip_allowed)
        self.assertEqual(response, "success")
