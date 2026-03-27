from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet,DocumentAccessViewSet

router = DefaultRouter()
router.register('documents', DocumentViewSet)
router.register('document-access',DocumentAccessViewSet)
urlpatterns = []
urlpatterns += router.urls