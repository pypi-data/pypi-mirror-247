import warnings

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_revision.views import RevisionMixin
from edc_sites.view_mixins import SiteViewMixin

from .message_view_mixin import MessageViewMixin
from .template_request_context_mixin import TemplateRequestContextMixin


class EdcViewMixin(
    LoginRequiredMixin,
    MessageViewMixin,
    RevisionMixin,
    SiteViewMixin,
    TemplateRequestContextMixin,
):
    """Adds common template variables and warning messages."""

    edc_device_app = "edc_device"

    def get_context_data(self, **kwargs) -> dict:
        try:
            edc_device_app_config = django_apps.get_app_config(self.edc_device_app)
        except LookupError as e:
            edc_device_app_config = None
            warnings.warn(str(e))
        live_system = getattr(settings, "LIVE_SYSTEM", "TEST")
        kwargs.update(
            {
                "device_id": getattr(edc_device_app_config, "device_id", "device_id?"),
                "device_role": getattr(edc_device_app_config, "device_role", "device_role?"),
                "live_system": live_system,
            }
        )
        self.check_for_warning_messages(live_system=live_system)
        return super().get_context_data(**kwargs)

    def check_for_warning_messages(self, live_system=None) -> None:
        if settings.DEBUG:
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    "This EDC is running in DEBUG-mode. Use for testing only. "
                    "Do not use this system for production data collection!"
                ),
            )
        elif not settings.DEBUG and not live_system:
            messages.add_message(
                self.request,
                messages.WARNING,
                (
                    "This EDC is for testing only. "
                    "Do not use this system for production data collection!"
                ),
            )
        try:
            if settings.WARNING_MESSAGE:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    settings.WARNING_MESSAGE,
                    extra_tags="warning",
                )
        except AttributeError:
            pass
        if self.request.user.is_superuser:
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    "You are using a `superuser` account. The EDC does not operate correctly "
                    "with user acounts that have the `superuser` status. "
                    "Update your user account before continuing."
                ),
            )
