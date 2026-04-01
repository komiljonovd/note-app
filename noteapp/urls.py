from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet,DocumentAccessViewSet,test_page
from django.urls import path


router = DefaultRouter()
router.register('documents', DocumentViewSet)
router.register('document-access',DocumentAccessViewSet)
urlpatterns = [
    path('test/', test_page),

]
urlpatterns += router.urls