"""API URL configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"positions", views.PositionViewSet, basename="position")
router.register(r"orders", views.OrderViewSet, basename="order")
router.register(r"signals", views.TradingSignalViewSet, basename="signal")
router.register(r"decisions", views.DecisionViewSet, basename="decision")

urlpatterns = [
    path("", include(router.urls)),
    path("health/", views.HealthCheckView.as_view(), name="health"),
]
