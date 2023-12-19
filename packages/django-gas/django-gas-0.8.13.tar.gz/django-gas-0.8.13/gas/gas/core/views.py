from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from gas import gas_settings
from gas.views import GASMixin


class GASPasswordChangeView(GASMixin, PasswordChangeView):
    template_name = "gas/base_form.html"
    success_url = reverse_lazy("gas:index")
    continue_url = reverse_lazy("gas:change_password")
    title = _("Change your password")
    success_message = _("Password changed.")


class Index(GASMixin, TemplateView):
    main_menu = "index"
    template_name = "gas/index.html"
    roles = ("staff",)


class GASContextMixin:
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        css = gas_settings.MEDIA["css"]
        javascript = gas_settings.MEDIA["js"]
        if gas_settings.EXTRA_MEDIA:
            css = css + gas_settings.EXTRA_MEDIA.get("css", [])
            javascript = javascript + gas_settings.EXTRA_MEDIA.get("js", [])
        ctx.update(
            {
                "logo_static_url": gas_settings.LOGO,
                "css": css,
                "js": javascript,
            }
        )
        return ctx


class GASLoginView(GASContextMixin, LoginView):
    template_name = "gas/login.html"

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url("gas:index")


class GASPasswordResetView(GASContextMixin, PasswordResetView):
    template_name = "gas/reset.html"
    html_email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("gas:password_reset_done")


class GASPasswordResetDoneView(GASContextMixin, PasswordResetDoneView):
    template_name = "gas/reset_done.html"


class GASPasswordResetConfirmView(GASContextMixin, PasswordResetConfirmView):
    template_name = "gas/reset_confirm.html"
    success_url = reverse_lazy("gas:password_reset_complete")


class GASPasswordResetCompleteView(GASContextMixin, TemplateView):
    template_name = "gas/reset_complete.html"
