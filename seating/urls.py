from rest_framework.routers import DefaultRouter
from .views import AreaViewSet, TableViewSet

router = DefaultRouter()
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'tables', TableViewSet, basename='table')