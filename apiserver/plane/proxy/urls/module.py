from django.urls import path

from plane.proxy.views import ModuleAPIEndpoint, ModuleIssueAPIEndpoint

urlpatterns = [
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/modules/",
        ModuleAPIEndpoint.as_view(),
        name="modules",
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/modules/<uuid:pk>/",
        ModuleAPIEndpoint.as_view(),
        name="modules",
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/modules/<uuid:module_id>/module-issues/",
        ModuleIssueAPIEndpoint.as_view(),
        name="module-issues",
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/modules/<uuid:module_id>/module-issues/<uuid:pk>/",
        ModuleIssueAPIEndpoint.as_view(),
        name="module-issues",
    ),
]
