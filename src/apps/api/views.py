"""API views."""

from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.decision_engine.models import Decision, TradingSignal
from apps.trading.models import Order, Position, Token, TokenHolder, TokenHolderSnapshot, TokenHolderSync

from .serializers import (
    DecisionSerializer,
    OrderSerializer,
    PositionSerializer,
    TokenHolderBulkCreateSerializer,
    TokenHolderSerializer,
    TokenHolderSnapshotSerializer,
    TokenHolderSyncSerializer,
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


class TokenHolderViewSet(viewsets.ModelViewSet):
    """Token holder viewset for managing holder data."""

    serializer_class = TokenHolderSerializer
    queryset = TokenHolder.objects.select_related("token").all()

    def get_queryset(self):
        """Filter by token address and chain if provided."""
        queryset = super().get_queryset()
        token_address = self.request.query_params.get("token_address")
        chain_id = self.request.query_params.get("chain_id")
        wallet_address = self.request.query_params.get("wallet_address")

        if token_address:
            queryset = queryset.filter(token__address__iexact=token_address)
        if chain_id:
            queryset = queryset.filter(token__chain_id=chain_id)
        if wallet_address:
            queryset = queryset.filter(wallet_address__iexact=wallet_address)

        return queryset

    @action(detail=False, methods=["get"])
    def by_token(self, request):
        """Get holders for a specific token."""
        token_address = request.query_params.get("token_address")
        chain_id = request.query_params.get("chain_id", 1)

        if not token_address:
            return Response(
                {"error": "token_address is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        holders = self.queryset.filter(
            token__address__iexact=token_address,
            token__chain_id=chain_id,
        ).order_by("-balance")

        serializer = self.get_serializer(holders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def diamond_hands(self, request):
        """Get holders who haven't transferred (diamond hands)."""
        token_address = request.query_params.get("token_address")
        chain_id = request.query_params.get("chain_id", 1)

        queryset = self.queryset.filter(has_initiated_transfer=False)

        if token_address:
            queryset = queryset.filter(
                token__address__iexact=token_address,
                token__chain_id=chain_id,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def top_holders(self, request):
        """Get top holders by balance."""
        token_address = request.query_params.get("token_address")
        chain_id = request.query_params.get("chain_id", 1)
        limit = int(request.query_params.get("limit", 100))

        if not token_address:
            return Response(
                {"error": "token_address is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        holders = self.queryset.filter(
            token__address__iexact=token_address,
            token__chain_id=chain_id,
        ).order_by("-balance")[:limit]

        serializer = self.get_serializer(holders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def bulk_sync(self, request):
        """Bulk create or update token holders from external data."""
        serializer = TokenHolderBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_address = serializer.validated_data["token_address"]
        chain_id = serializer.validated_data["chain_id"]
        holders_data = serializer.validated_data["holders"]
        next_offset = serializer.validated_data.get("next_offset")

        # Get or create the token
        token, _ = Token.objects.get_or_create(
            address__iexact=token_address,
            chain_id=chain_id,
            defaults={
                "address": token_address,
                "symbol": "UNKNOWN",
                "name": "Unknown Token",
                "decimals": 18,
            },
        )

        # Get or create sync state
        sync_state, _ = TokenHolderSync.objects.get_or_create(token=token)
        sync_state.sync_in_progress = True
        sync_state.save()

        created_count = 0
        updated_count = 0

        try:
            with transaction.atomic():
                for holder_data in holders_data:
                    wallet_address = holder_data.get("wallet_address")
                    balance = Decimal(holder_data.get("balance", "0"))
                    first_acquired_str = holder_data.get("first_acquired")
                    has_initiated_transfer = holder_data.get("has_initiated_transfer", False)

                    first_acquired = None
                    if first_acquired_str:
                        first_acquired = parse_datetime(first_acquired_str)
                    if not first_acquired:
                        first_acquired = timezone.now()

                    holder, created = TokenHolder.objects.update_or_create(
                        token=token,
                        wallet_address=wallet_address.lower(),
                        defaults={
                            "balance": balance,
                            "first_acquired": first_acquired,
                            "has_initiated_transfer": has_initiated_transfer,
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                # Update sync state
                sync_state.last_sync_at = timezone.now()
                sync_state.next_offset = next_offset
                sync_state.total_holders = TokenHolder.objects.filter(token=token).count()
                sync_state.sync_in_progress = False
                sync_state.last_error = None
                sync_state.save()

        except Exception as e:
            sync_state.sync_in_progress = False
            sync_state.last_error = str(e)
            sync_state.save()
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({
            "created": created_count,
            "updated": updated_count,
            "total_holders": sync_state.total_holders,
            "next_offset": next_offset,
        })

    @action(detail=False, methods=["get"], url_path="snapshots/(?P<wallet_address>[^/.]+)")
    def wallet_history(self, request, wallet_address=None):
        """Get historical snapshots for a specific wallet."""
        token_address = request.query_params.get("token_address")
        chain_id = request.query_params.get("chain_id", 1)

        queryset = TokenHolderSnapshot.objects.filter(
            wallet_address__iexact=wallet_address
        )

        if token_address:
            queryset = queryset.filter(
                token__address__iexact=token_address,
                token__chain_id=chain_id,
            )

        serializer = TokenHolderSnapshotSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def sync_status(self, request):
        """Get sync status for all tokens or a specific token."""
        token_address = request.query_params.get("token_address")
        chain_id = request.query_params.get("chain_id")

        queryset = TokenHolderSync.objects.select_related("token").all()

        if token_address:
            queryset = queryset.filter(token__address__iexact=token_address)
        if chain_id:
            queryset = queryset.filter(token__chain_id=chain_id)

        serializer = TokenHolderSyncSerializer(queryset, many=True)
        return Response(serializer.data)
