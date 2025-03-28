from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic as views_generic

from adhocracy4.categories import filters as category_filters
from adhocracy4.dashboard import mixins
from adhocracy4.exports.views import DashboardExportView
from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from adhocracy4.filters import widgets as filters_widgets
from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.projects.mixins import DisplayProjectOrModuleMixin
from adhocracy4.projects.mixins import ProjectMixin
from apps.contrib.widgets import AplusOrderingWidget
from apps.ideas import views as idea_views

from . import forms
from . import models


class XRPrioView(ProjectMixin, views_generic.TemplateView, DisplayProjectOrModuleMixin):
    template_name = "a4_candy_xrprio/module_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def serve_threejs_content(request):
    return render(request, "a4_candy_xrprio/threejs_content.html")


# class FreeTextFilterWidget(filters_widgets.FreeTextFilterWidget):
#     label = _("Search")


# class XRPrioFilterSet(a4_filters.DefaultsFilterSet):
#     defaults = {"ordering": "name"}
#     category = category_filters.CategoryFilter()
#     ordering = a4_filters.DynamicChoicesOrderingFilter(
#         choices=(
#             ("name", _("Alphabetical")),
#             ("-positive_rating_count", _("Most popular")),
#             ("-comment_count", _("Most commented")),
#         ),
#         widget=AplusOrderingWidget,
#     )
#     search = FreeTextFilter(widget=FreeTextFilterWidget, fields=["name"])

#     class Meta:
#         model = models.XRPrio
#         fields = ["search", "category"]


# class XRPrioListView(idea_views.AbstractIdeaListView, DisplayProjectOrModuleMixin):
#     model = models.XRPrio
#     filter_set = XRPrioFilterSet


# class XRPrioDetailView(idea_views.AbstractIdeaDetailView):
#     model = models.XRPrio
#     queryset = (
#         models.XRPrio.objects.annotate_positive_rating_count().annotate_negative_rating_count()
#     )
#     permission_required = "a4_candy_xrprio.view_topic"


# class XRPrioCreateFilterSet(a4_filters.DefaultsFilterSet):
#     defaults = {"ordering": "name"}

#     category = category_filters.CategoryFilter()

#     ordering = a4_filters.DynamicChoicesOrderingFilter(
#         choices=(("name", _("Alphabetical")),), widget=AplusOrderingWidget
#     )

#     class Meta:
#         model = models.XRPrio
#         fields = ["category"]


# class XRPrioListDashboardView(
#     ProjectMixin,
#     mixins.DashboardBaseMixin,
#     mixins.DashboardComponentMixin,
#     filter_views.FilteredListView,
# ):
#     model = models.XRPrio
#     template_name = "a4_candy_xrprio/topic_dashboard_list.html"
#     filter_set = XRPrioCreateFilterSet
#     permission_required = "a4projects.change_project"

#     def get_queryset(self):
#         return super().get_queryset().filter(module=self.module)

#     def get_permission_object(self):
#         return self.project


# class XRPrioCreateView(
#     mixins.DashboardBaseMixin,
#     mixins.DashboardComponentMixin,
#     mixins.DashboardComponentFormSignalMixin,
#     idea_views.AbstractIdeaCreateView,
# ):
#     model = models.XRPrio
#     form_class = forms.XRPrioForm
#     permission_required = "a4_candy_xrprio.add_topic"
#     template_name = "a4_candy_xrprio/topic_create_form.html"

#     def get_success_url(self):
#         return reverse(
#             "a4dashboard:topic-list",
#             kwargs={
#                 "organisation_slug": self.module.project.organisation.slug,
#                 "module_slug": self.module.slug,
#             },
#         )

#     def get_permission_object(self):
#         return self.module


# class XRPrioUpdateView(
#     mixins.DashboardBaseMixin,
#     mixins.DashboardComponentMixin,
#     mixins.DashboardComponentFormSignalMixin,
#     idea_views.AbstractIdeaUpdateView,
# ):
#     model = models.XRPrio
#     form_class = forms.XRPrioForm
#     permission_required = "a4_candy_xrprio.change_topic"
#     template_name = "a4_candy_xrprio/topic_update_form.html"

#     @property
#     def organisation(self):
#         return self.project.organisation

#     def get_success_url(self):
#         return reverse(
#             "a4dashboard:topic-list",
#             kwargs={
#                 "organisation_slug": self.module.project.organisation.slug,
#                 "module_slug": self.module.slug,
#             },
#         )

#     def get_permission_object(self):
#         return self.get_object()


# class XRPrioDeleteView(
#     mixins.DashboardBaseMixin,
#     mixins.DashboardComponentMixin,
#     mixins.DashboardComponentFormSignalMixin,
#     idea_views.AbstractIdeaDeleteView,
# ):
#     model = models.XRPrio
#     success_message = _("The topic has been deleted")
#     permission_required = "a4_candy_xrprio.change_topic"
#     template_name = "a4_candy_xrprio/topic_confirm_delete.html"

#     @property
#     def organisation(self):
#         return self.project.organisation

#     def get_success_url(self):
#         return reverse(
#             "a4dashboard:topic-list",
#             kwargs={
#                 "organisation_slug": self.module.project.organisation.slug,
#                 "module_slug": self.module.slug,
#             },
#         )

#     def get_permission_object(self):
#         return self.get_object()


# class XRPrioDashboardExportView(DashboardExportView):
#     template_name = "a4exports/export_dashboard.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["export"] = reverse(
#             "a4dashboard:topic-export",
#             kwargs={
#                 "organisation_slug": self.module.project.organisation.slug,
#                 "module_slug": self.module.slug,
#             },
#         )
#         context["comment_export"] = reverse(
#             "a4dashboard:topic-comment-export",
#             kwargs={
#                 "organisation_slug": self.module.project.organisation.slug,
#                 "module_slug": self.module.slug,
#             },
#         )
#         return context
