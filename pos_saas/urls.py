from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from catalog.urls import router as catalog_router
from seating.urls import router as seating_router
from customers.urls import router as customers_router
from orders.urls import router as orders_router
from sales.urls import router as sales_router
from cash.urls import router as cash_router

router = DefaultRouter()
router.registry.extend(catalog_router.registry)
router.registry.extend(seating_router.registry)
router.registry.extend(customers_router.registry)
router.registry.extend(orders_router.registry)
router.registry.extend(sales_router.registry)
router.registry.extend(cash_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/', include(router.urls)),
    path('api/core/', include('core.urls')),
]