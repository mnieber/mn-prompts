from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

import blogs_be.api.urls
import blogs_be.users.urls
import blogs_be.blogs.urls
from blogs_be.app.utils.serve_static import serve_static

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"", include(blogs_be.api.urls)),
    path(r"api/blogs/", include(blogs_be.blogs.urls)),
    path(r"api/users/", include(blogs_be.users.urls)),
    path(
        "api/v1/schema/",
        staff_member_required(SpectacularAPIView.as_view()),
        name="schema",
    ),
    path(
        "api/v1/schema/swagger-ui/",
        staff_member_required(SpectacularSwaggerView.as_view(url_name="schema")),
        name="swagger-ui",
    ),
] + ([] + serve_static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
