from django.urls import include, path
from rest_framework.routers import SimpleRouter

from workspaces import views

router = SimpleRouter()
router.register("", views.WorkspacesView)

urlpatterns = [path("open", views.open), path("", include(router.urls))]
