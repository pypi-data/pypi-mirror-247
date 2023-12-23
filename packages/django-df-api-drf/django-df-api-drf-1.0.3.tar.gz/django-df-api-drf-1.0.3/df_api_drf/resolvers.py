from typing import Any

from django.contrib.sites.models import Site
from django.utils.module_loading import import_string

from df_api_drf.settings import api_settings


def site_url(**kwargs: Any) -> str:
    return import_string(api_settings.SITE_URL_RESOLVER)().format_url(**kwargs)


class SiteUrlResolver:
    def get_site(self, **kwargs: Any) -> Site:
        return Site.objects.get_current()

    def format_url(self, **kwargs: Any) -> str:
        site = self.get_site(**kwargs)
        domain = site.domain
        if api_settings.SITE_URL_SUBDOMAIN:
            domain = f"{api_settings.SITE_URL_SUBDOMAIN}.{domain}"
        url = f"https://{domain}"
        if api_settings.SITE_URL_APPEND_HASH:
            url += "/#"
        return url
