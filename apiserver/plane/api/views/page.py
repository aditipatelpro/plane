# Python imports
from datetime import timedelta, date, datetime

# Django imports
from django.db import connection
from django.db.models import Exists, OuterRef, Q, Prefetch
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.gzip import gzip_page
from django.db.models import (
    OuterRef,
    Func,
    F,
    Q,
    Exists,
)

# Third party imports
from rest_framework import status
from rest_framework.response import Response
from sentry_sdk import capture_exception

# Module imports
from .base import BaseViewSet, BaseAPIView
from plane.api.permissions import ProjectEntityPermission
from plane.db.models import (
    Page,
    PageFavorite,
    Issue,
    IssueAssignee,
    IssueActivity,
    PageLog,
)
from plane.api.serializers import (
    PageSerializer,
    PageFavoriteSerializer,
    PageLogSerializer,
    IssueLiteSerializer,
    SubPageSerializer,
)


def unarchive_archive_page_and_descendants(page_id, archived_at):
    # Your SQL query
    sql = """
    WITH RECURSIVE descendants AS (
        SELECT id FROM pages WHERE id = %s
        UNION ALL
        SELECT pages.id FROM pages, descendants WHERE pages.parent_id = descendants.id
    )
    UPDATE pages SET archived_at = %s WHERE id IN (SELECT id FROM descendants);
    """

    # Execute the SQL query
    with connection.cursor() as cursor:
        cursor.execute(sql, [page_id, archived_at])


class PageViewSet(BaseViewSet):
    serializer_class = PageSerializer
    model = Page
    permission_classes = [
        ProjectEntityPermission,
    ]
    search_fields = [
        "name",
    ]

    def get_queryset(self):
        subquery = PageFavorite.objects.filter(
            user=self.request.user,
            page_id=OuterRef("pk"),
            project_id=self.kwargs.get("project_id"),
            workspace__slug=self.kwargs.get("slug"),
        )
        return self.filter_queryset(
            super()
            .get_queryset()
            .filter(workspace__slug=self.kwargs.get("slug"))
            .filter(project_id=self.kwargs.get("project_id"))
            .filter(project__project_projectmember__member=self.request.user)
            .filter(parent__isnull=True)
            .filter(Q(owned_by=self.request.user) | Q(access=0))
            .select_related("project")
            .select_related("workspace")
            .select_related("owned_by")
            .annotate(is_favorite=Exists(subquery))
            .order_by(self.request.GET.get("order_by", "-created_at"))
            .prefetch_related("labels")
            .order_by("-is_favorite","-created_at")
            .distinct()
        )

    def perform_create(self, serializer):
        serializer.save(
            project_id=self.kwargs.get("project_id"), owned_by=self.request.user
        )

    def create(self, request, slug, project_id):
        serializer = PageSerializer(
            data=request.data,
            context={"project_id": project_id, "owned_by_id": request.user.id},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, slug, project_id, pk):
        try:
            page = Page.objects.get(pk=pk, workspace__slug=slug, project_id=project_id)

            if page.is_locked:
                return Response(
                    {"error": "Page is locked"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            parent = request.data.get("parent", None)
            if parent:
                _ = Page.objects.get(
                    pk=parent, workspace__slug=slug, project_id=project_id
                )

            # Only update access if the page owner is the requesting  user
            if (
                page.access != request.data.get("access", page.access)
                and page.owned_by_id != request.user.id
            ):
                return Response(
                    {
                        "error": "Access cannot be updated since this page is owned by someone else"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = PageSerializer(page, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Page.DoesNotExist:
            return Response(
                {
                    "error": "Access cannot be updated since this page is owned by someone else"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def lock(self, request, slug, project_id, pk):
        page = Page.objects.filter(
            pk=pk, workspace__slug=slug, project_id=project_id
        )

        # only the owner can lock the page
        if request.user.id != page.owned_by_id:
            return Response(
                {"error": "Only the page owner can lock the page"},
            )

        page.is_locked = True
        page.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def unlock(self, request, slug, project_id, pk):
        page = Page.objects.get(pk=pk, workspace__slug=slug, project_id=project_id)

        # only the owner can unlock the page
        if request.user.id != page.owned_by_id:
            return Response(
                {"error": "Only the page owner can unlock the page"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        page.is_locked = False
        page.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, slug, project_id):
        queryset = self.get_queryset().filter(archived_at__isnull=True)
        page_view = request.GET.get("page_view", False)

        if not page_view:
            return Response(
                {"error": "Page View parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # All Pages
        if page_view == "all":
            return Response(
                PageSerializer(queryset, many=True).data, status=status.HTTP_200_OK
            )

        # Recent pages
        if page_view == "recent":
            current_time = date.today()
            day_before = current_time - timedelta(days=1)
            todays_pages = queryset.filter(updated_at__date=date.today())
            yesterdays_pages = queryset.filter(updated_at__date=day_before)
            earlier_this_week = queryset.filter(
                updated_at__date__range=(
                    (timezone.now() - timedelta(days=7)),
                    (timezone.now() - timedelta(days=2)),
                )
            )
            return Response(
                {
                    "today": PageSerializer(todays_pages, many=True).data,
                    "yesterday": PageSerializer(yesterdays_pages, many=True).data,
                    "earlier_this_week": PageSerializer(
                        earlier_this_week, many=True
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        # Favorite Pages
        if page_view == "favorite":
            queryset = queryset.filter(is_favorite=True)
            return Response(
                PageSerializer(queryset, many=True).data, status=status.HTTP_200_OK
            )

        # My pages
        if page_view == "created_by_me":
            queryset = queryset.filter(owned_by=request.user)
            return Response(
                PageSerializer(queryset, many=True).data, status=status.HTTP_200_OK
            )

        # Created by other Pages
        if page_view == "created_by_other":
            queryset = queryset.filter(~Q(owned_by=request.user), access=0)
            return Response(
                PageSerializer(queryset, many=True).data, status=status.HTTP_200_OK
            )

        return Response(
            {"error": "No matching view found"}, status=status.HTTP_400_BAD_REQUEST
        )

    def archive(self, request, slug, project_id, page_id):
        _ = Page.objects.get(
            project_id=project_id,
            owned_by_id=request.user.id,
            workspace__slug=slug,
            pk=page_id,
        )

        unarchive_archive_page_and_descendants(page_id, datetime.now())

        return Response(status=status.HTTP_204_NO_CONTENT)

    def unarchive(self, request, slug, project_id, page_id):
        page = Page.objects.get(
            project_id=project_id,
            owned_by_id=request.user.id,
            workspace__slug=slug,
            pk=page_id,
        )

        page.parent = None
        page.save()

        unarchive_archive_page_and_descendants(page_id, None)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def archive_list(self, request, slug, project_id):
        pages = (
            Page.objects.filter(
                project_id=project_id,
                workspace__slug=slug,
            )
            .filter(archived_at__isnull=False)
            .filter(parent_id__isnull=True)
        )

        if not pages:
            return Response(
                {"error": "No pages found"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            PageSerializer(pages, many=True).data, status=status.HTTP_200_OK
        )



class PageFavoriteViewSet(BaseViewSet):
    permission_classes = [
        ProjectEntityPermission,
    ]

    serializer_class = PageFavoriteSerializer
    model = PageFavorite

    def get_queryset(self):
        return self.filter_queryset(
            super()
            .get_queryset()
            .filter(archived_at__isnull=True)
            .filter(workspace__slug=self.kwargs.get("slug"))
            .filter(user=self.request.user)
            .select_related("page", "page__owned_by")
        )

    def create(self, request, slug, project_id):
        serializer = PageFavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, project_id=project_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug, project_id, page_id):
        page_favorite = PageFavorite.objects.get(
            project=project_id,
            user=request.user,
            workspace__slug=slug,
            page_id=page_id,
        )
        page_favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PageLogEndpoint(BaseAPIView):
    permission_classes = [
        ProjectEntityPermission,
    ]

    serializer_class = PageLogSerializer
    model = PageLog

    def post(self, request, slug, project_id, page_id):
        serializer = PageLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=project_id, page_id=page_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug, project_id, page_id, transaction):
        page_transaction = PageLog.objects.get(
            workspace__slug=slug,
            project_id=project_id,
            page_id=page_id,
            transaction=transaction,
        )
        serializer = PageLogSerializer(
            page_transaction, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, project_id, page_id, transaction):
        transaction = PageLog.objects.get(
            workspace__slug=slug,
            project_id=project_id,
            page_id=page_id,
            transaction=transaction,
        )
        # Delete the transaction object
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateIssueFromBlockEndpoint(BaseAPIView):
    permission_classes = [
        ProjectEntityPermission,
    ]

    def post(self, request, slug, project_id, page_id):
        page = Page.objects.get(
            workspace__slug=slug,
            project_id=project_id,
            pk=page_id,
        )
        issue = Issue.objects.create(
            name=request.data.get("name"),
            project_id=project_id,
        )
        _ = IssueAssignee.objects.create(
            issue=issue, assignee=request.user, project_id=project_id
        )

        _ = IssueActivity.objects.create(
            issue=issue,
            actor=request.user,
            project_id=project_id,
            comment=f"created the issue from {page.name} block",
            verb="created",
        )

        return Response(IssueLiteSerializer(issue).data, status=status.HTTP_200_OK)


class SubPagesEndpoint(BaseAPIView):
    permission_classes = [
        ProjectEntityPermission,
    ]

    @method_decorator(gzip_page)
    def get(self, request, slug, project_id, page_id):
        pages = (
            PageLog.objects.filter(
                page_id=page_id,
                project_id=project_id,
                workspace__slug=slug,
                entity_name__in=["forward_link", "back_link"],
            )
            .filter(archived_at__isnull=True)
            .select_related("project")
            .select_related("workspace")
        )
        return Response(
            SubPageSerializer(pages, many=True).data, status=status.HTTP_200_OK
        )

