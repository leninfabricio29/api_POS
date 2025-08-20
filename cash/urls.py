from rest_framework.routers import DefaultRouter
from .views import CashSessionViewSet, CashMovementViewSet

router = DefaultRouter()
router.register(r'cash-sessions', CashSessionViewSet, basename='cashsession')
router.register(r'cash-movements', CashMovementViewSet, basename='cashmovement')