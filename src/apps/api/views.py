"""API views."""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.decision_engine.models import Decision, TradingSignal
from apps.trading.models import Order, Position

from .serializers import (
    DecisionSerializer,
    OrderSerializer,
    PositionSerializer,
    TradingSignalSerializer,
)


class HealthCheckView(APIView):
    """Health check endpoint."""

    permission_classes = [AllowAny]

    def get(self, request):
        """Return health status."""
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)


class PositionViewSet(viewsets.ReadOnlyModelViewSet):
    """Position viewset."""

    serializer_class = PositionSerializer
    queryset = Position.objects.select_related("token", "wallet").all()

    @action(detail=False, methods=["get"])
    def open(self, request):
        """Get open positions."""
        positions = self.queryset.filter(is_open=True)
        serializer = self.get_serializer(positions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def closed(self, request):
        """Get closed positions."""
        positions = self.queryset.filter(is_open=False)
        serializer = self.get_serializer(positions, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Order viewset."""

    serializer_class = OrderSerializer
    queryset = Order.objects.select_related("token", "wallet").all()

    @action(detail=False, methods=["get"])
    def pending(self, request):
        """Get pending orders."""
        orders = self.queryset.filter(status="pending")
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def filled(self, request):
        """Get filled orders."""
        orders = self.queryset.filter(status="filled")
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class TradingSignalViewSet(viewsets.ReadOnlyModelViewSet):
    """Trading signal viewset."""

    serializer_class = TradingSignalSerializer
    queryset = TradingSignal.objects.select_related("token", "strategy").all()

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """Get recent signals."""
        signals = self.queryset.order_by("-created_at")[:100]
        serializer = self.get_serializer(signals, many=True)
        return Response(serializer.data)


class DecisionViewSet(viewsets.ReadOnlyModelViewSet):
    """Decision viewset."""

    serializer_class = DecisionSerializer
    queryset = Decision.objects.select_related("token").all()

    @action(detail=False, methods=["get"])
    def approved(self, request):
        """Get approved decisions."""
        decisions = self.queryset.filter(approved=True)
        serializer = self.get_serializer(decisions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def rejected(self, request):
        """Get rejected decisions."""
        decisions = self.queryset.filter(approved=False)
        serializer = self.get_serializer(decisions, many=True)
        return Response(serializer.data)
