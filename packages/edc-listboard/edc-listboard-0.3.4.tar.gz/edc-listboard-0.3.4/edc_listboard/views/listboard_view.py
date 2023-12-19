from __future__ import annotations

from django.apps import apps as django_apps
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from django.views.generic.list import ListView
from edc_dashboard.view_mixins import (
    TemplateRequestContextMixin,
    UrlRequestContextMixin,
)

from ..view_mixins import (
    QueryStringViewMixin,
    SearchListboardMixin,
    SiteQuerysetViewMixin,
)


class ListboardViewError(Exception):
    pass


class BaseListboardView(TemplateRequestContextMixin, ListView):
    cleaned_search_term: str | None = None
    context_object_name: str = "results"
    empty_queryset_message: str = _("Nothing to display.")
    listboard_template: str | None = None  # an existing key in request.context_data
    # if self.listboard_url declared through another mixin.
    listboard_url: str | None = None  # an existing key in request.context_data
    listboard_back_url: str | None = None

    # default, info, success, danger, warning, etc. See Bootstrap.
    listboard_panel_style: str = "default"
    listboard_fa_icon: str | None = None
    listboard_model: str | None = None  # label_lower model name or model class
    listboard_model_manager_name: str = "on_site"
    listboard_panel_title: str | None = None
    listboard_instructions: str | None = None

    permissions_warning_message: str = _("You do not have permission to view these data.")
    # e.g. "edc_subject_dashboard.view_subject_listboard"
    listboard_view_permission_codename: str | None = None
    # e.g. "edc_subject_dashboard.view_subject_listboard"
    listboard_view_only_my_permission_codename: str | None = None

    model_wrapper_cls = None
    ordering: str = "-created"

    orphans: int = 3
    paginate_by: int = 10
    paginator_url = None  # defaults to listboard_url

    def get(self, request, *args, **kwargs):
        if not self.has_view_listboard_perms:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.listboard_fa_icon and self.listboard_fa_icon.startswith("fa-"):
            self.listboard_fa_icon = f"fas {self.listboard_fa_icon}"
        kwargs.update(
            empty_queryset_message=self.get_empty_queryset_message(),
            listboard_fa_icon=self.listboard_fa_icon,
            listboard_panel_style=self.listboard_panel_style,
            listboard_panel_title=self.listboard_panel_title,
            listboard_instructions=self.listboard_instructions,
            object_list=self.get_wrapped_queryset(self.object_list),
            **self.add_url_to_context(
                new_key="listboard_url", existing_key=self.listboard_url
            ),
        )
        if self.listboard_back_url:
            kwargs.update(
                **self.add_url_to_context(
                    new_key="listboard_back_url",
                    existing_key=self.listboard_back_url,
                )
            )
        kwargs.update(
            has_listboard_model_perms=self.has_listboard_model_perms,
            has_view_listboard_perms=self.has_view_listboard_perms,
            listboard_view_permission_codename=self.listboard_view_permission_codename,
            permissions_warning_message=self.permissions_warning_message,
            **self.add_url_to_context(
                new_key="paginator_url", existing_key=self.paginator_url or self.listboard_url
            ),
        )
        return super().get_context_data(**kwargs)

    def get_template_names(self):
        return [self.get_template_from_context(self.listboard_template)]

    def get_empty_queryset_message(self) -> str:
        return self.empty_queryset_message

    @property
    def url_kwargs(self):
        """Returns a dictionary of URL options for either the
        Search form URL and the Form Action.
        """
        return {}

    @property
    def listboard_model_cls(self):
        """Returns the listboard's model class.

        Accepts `listboard_model` as a model class or label_lower.
        """
        if not self.listboard_model:
            raise ListboardViewError(
                f"Listboard model not declared. Got None. See {repr(self)}"
            )
        try:
            return django_apps.get_model(self.listboard_model)
        except (ValueError, AttributeError):
            return self.listboard_model

    def get_listboard_model_manager_name(self) -> str:
        return self.listboard_model_manager_name

    def get_queryset_exclude_options(self, request, *args, **kwargs):
        """Returns exclude options applied to every
        queryset.
        """
        return {}

    def get_queryset_filter_options(self, request, *args, **kwargs):
        """Returns filter options applied to every
        queryset.
        """
        return {}

    def get_filtered_queryset(self, filter_options=None, exclude_options=None):
        """Returns a queryset, called by `get_queryset`.

        This can be overridden but be sure to use the default_manager.
        """
        return (
            getattr(self.listboard_model_cls, self.get_listboard_model_manager_name())
            .filter(**filter_options)
            .exclude(**exclude_options)
        )

    def get_queryset(self):
        """Return the queryset for this view.

        Completely overrides ListView.get_queryset.

        Note:
            the resulting queryset filtering takes allocated
            permissions into account using Django's permissions
            framework.

            Only returns records if user has dashboard permissions to
            do so. See `has_view_listboard_perms`.

            Limit records to those created by the current user if
            `has_view_only_my_listboard_perms` return True.
            See `has_view_only_my_listboard_perms`.

        Passes filter/exclude criteria to `get_filtered_queryset`.

        Note: The returned queryset is set to self.object_list in
        `get()` just before rendering to response.
        """

        queryset = getattr(
            self.listboard_model_cls, self.get_listboard_model_manager_name()
        ).none()
        if self.has_view_listboard_perms:
            filter_options = self.get_queryset_filter_options(
                self.request, *self.args, **self.kwargs
            )
            if self.has_view_only_my_listboard_perms:
                filter_options.update(user_created=self.request.user.username)
            exclude_options = self.get_queryset_exclude_options(
                self.request, *self.args, **self.kwargs
            )
            queryset = self.get_filtered_queryset(
                filter_options=filter_options, exclude_options=exclude_options
            )
            queryset = self.get_updated_queryset(queryset)
            ordering = self.get_ordering()
            if ordering:
                if isinstance(ordering, (str,)):
                    ordering = (ordering,)
                queryset = queryset.order_by(*ordering)
        return queryset

    def get_updated_queryset(self, queryset):
        """Return the queryset for this view.

        Hook for a last chance to modify the queryset
        before ordering.
        """
        return queryset

    def get_wrapped_queryset(self, queryset):
        """Returns a list of wrapped model instances.

        Usually is passed the queryset `object_list` and wraps each
        instance just before passing to the template.
        """
        wrapped_objs = []
        for obj in queryset:
            model_wrapper = self.get_model_wrapper_cls()(model_obj=obj)
            model_wrapper = self.update_wrapped_instance(model_wrapper)
            wrapped_objs.append(model_wrapper)
        return wrapped_objs

    def get_model_wrapper_cls(self):
        return self.model_wrapper_cls

    def update_wrapped_instance(self, model_wrapper):
        """Returns a model_wrapper.

        Hook to add attrs to wrapped model instance.
        """
        return model_wrapper

    @property
    def has_view_listboard_perms(self):
        """Returns True if request.user has permissions to
        view the listboard.

        If False, `get_queryset` returns an empty queryset.
        """
        return self.request.user.has_perm(self.listboard_view_permission_codename)

    @property
    def has_view_only_my_listboard_perms(self):
        """Returns True if `request.user` ONLY has permissions to
        view records created by `request.user` on the listboard.
        """
        return self.request.user.has_perm(self.listboard_view_only_my_permission_codename)

    @property
    def has_listboard_model_perms(self):
        """Returns True if `request.user` has permissions to
        add/change the listboard model.

        Does not affect `get_queryset`.

        Used in templates.
        """
        app_label = self.listboard_model_cls._meta.label_lower.split(".")[0]
        model_name = self.listboard_model_cls._meta.label_lower.split(".")[1]
        return self.request.user.has_perms(
            [f"{app_label}.add_{model_name}", f"{app_label}.change_{model_name}"]
        )


class ListboardView(
    SiteQuerysetViewMixin,
    QueryStringViewMixin,
    UrlRequestContextMixin,
    SearchListboardMixin,
    BaseListboardView,
):
    urlconfig_getattr = "listboard_urls"

    @classmethod
    def get_urlname(cls):
        return cls.listboard_url
