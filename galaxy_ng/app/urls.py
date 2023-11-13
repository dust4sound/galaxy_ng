from django.conf import settings
from django.urls import re_path as url
from django.shortcuts import redirect
from django.urls import include, path
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.backends.utils import load_backends
from social_django.utils import load_strategy, psa

from . import views
from galaxy_ng.app.api import urls as api_urls
from galaxy_ng.ui import urls as ui_urls

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularYAMLAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

API_PATH_PREFIX = settings.GALAXY_API_PATH_PREFIX.strip("/")

galaxy_urls = [
    path(f"{API_PATH_PREFIX}/", include(api_urls)),
]

urlpatterns = [
    path("", include((galaxy_urls, "api"), namespace="galaxy")),
    path("", include(ui_urls)),
    path("", include("django_prometheus.urls")),
    path(
        f"{API_PATH_PREFIX}/v3/openapi.json",
        SpectacularJSONAPIView.as_view(),
        name="schema",
    ),
    path(
        f"{API_PATH_PREFIX}/v3/openapi.yaml",
        SpectacularYAMLAPIView.as_view(),
        name="schema-yaml",
    ),
    path(
        f"{API_PATH_PREFIX}/v3/redoc/",
        SpectacularRedocView.as_view(),
        name="schema-redoc",
    ),
    path(
        f"{API_PATH_PREFIX}/v3/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("healthz", views.health_view),
    path("", include("social_django.urls", namespace="social")),
]

if settings.get("API_ROOT") != "/pulp/":
    urlpatterns.append(
        path(
            "pulp/api/<path:api_path>",
            views.PulpAPIRedirectView.as_view(),
            name="pulp_redirect")
    )

if settings.get("SOCIAL_AUTH_KEYCLOAK_KEY"):
    urlpatterns.append(path("login/", lambda request: redirect("/login/keycloak/",
                                                               permanent=False)))
elif settings.get("SOCIAL_AUTH_GITHUB_KEY"):
    urlpatterns.append(path("login/", lambda request: redirect("/login/github/",
                                                               permanent=False)))
elif settings.get("SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY"):
    urlpatterns.append(path("login/", lambda request: redirect("/login/azuread-tenant-oauth2/",
                                                               permanent=False)))
elif settings.get("SOCIAL_AUTH_AMAZON_KEY"):
    urlpatterns.append(path("login/", lambda request: redirect("/login/amazon/",
                                                               permanent=False)))
elif settings.get("SOCIAL_AUTH_GITLAB_KEY"):
    urlpatterns.append(path("login/", lambda request: redirect("/login/gitlab/",
                                                               permanent=False)))
elif settings.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"):
    urlpatterns.append(path("login/", lambda request: redirect("/login/google-oauth2/",
                                                               permanent=False)))
