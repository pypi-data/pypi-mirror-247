import ipaddress
import logging

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.urls.resolvers import RegexPattern, URLResolver

from .models import AllowedIP, AllowedIPRange
from .utils import get_request_ips

logger = logging.getLogger(__name__)


class IPWhiteListMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if self.allowed_path(request):
            setattr(request, "ip_allowed", True)
            return self.get_response(request)
        self.process_request(request)

        if request.ip_allowed:
            return self.get_response(request)
        else:
            raise PermissionDenied

    @staticmethod
    def is_allowed(ips, allowed_ips, allowed_ranges):
        allowed = False
        for ip_str in ips:
            if ip_str in allowed_ips:
                allowed = True
                break

            ip = ipaddress.ip_address(ip_str)

            for allowed_range in allowed_ranges:
                try:
                    network = ipaddress.ip_network(allowed_range)
                except ValueError as e:
                    logger.warning(
                        "Failed to parse specific network address: {}".format(
                            "".join(e.args)
                        )
                    )
                    continue

                if ip in network:
                    allowed = True
                    break

            if allowed:
                break

        return allowed

    def process_request(self, request):
        allowed_ips = set(settings.WHITELIST_IPS)
        cached_allowed_ips = cache.get("allowed_ips", None)
        if cached_allowed_ips is None:
            db_allowed_ips = AllowedIP.objects.values_list("address", flat=True)
            cache.set("allowed_ips", list(db_allowed_ips))
            cached_allowed_ips = cache.get("allowed_ips")
        allowed_ips.update(cached_allowed_ips)

        allowed_ranges = set(settings.WHITELIST_IP_RANGES)
        cached_allowed_ranges = cache.get("allowed_ranges", None)
        if cached_allowed_ranges is None:
            db_allowed_ranges = AllowedIPRange.objects.values_list("range", flat=True)
            cache.set("allowed_ranges", list(db_allowed_ranges))
            cached_allowed_ranges = cache.get("allowed_ranges")
        allowed_ranges.update(cached_allowed_ranges)

        ips = get_request_ips(request)

        # Check cached and settings ips.
        allowed = self.is_allowed(
            ips=ips, allowed_ips=allowed_ips, allowed_ranges=allowed_ranges
        )
        setattr(request, "ip_allowed", allowed)

    def allowed_path(self, request):

        external_flatpage = getattr(request, "external_flatpage", False)

        if external_flatpage:
            return True

        return not request.path.startswith(settings.OUTSIDE_IP_DISALLOWED_PATHS)
