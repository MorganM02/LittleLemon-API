from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from .permissions import IsManager
from .permissions import IsManagerOrReadOnly, IsDeliveryCrew
class MenuItemPagination(PageNumberPagination):
    page_size = 3
from .models import Category, MenuItem, Cart, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = MenuItemPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['price']

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return Cart.objects.filter(id=cart.id)

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        menuitem_id = request.data.get('menuitem')
        quantity = request.data.get('quantity', 1)

        if not menuitem_id:
            return Response(
                {'error': 'menuitem is required'},
                status=400
            )

        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            return Response(
                {'error': 'Menu item not found'},
                status=404
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menuitem=menuitem,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = self.get_serializer(cart)

        return Response(
            serializer.data,
            status=201
        )
class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()

        if user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=user)

        return Order.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user

        # Managers can create orders by assigning them to a customer.
        if user.groups.filter(name='Manager').exists():
            customer_id = request.data.get('user')

            if not customer_id:
                return Response(
                    {'error': 'user is required'},
                    status=400
                )

            try:
                customer = User.objects.get(id=customer_id)
            except User.DoesNotExist:
                return Response(
                    {'error': 'Customer not found'},
                    status=404
                )

            order = Order.objects.create(
                user=customer,
                total=0
            )

            serializer = self.get_serializer(order)

            return Response(
                serializer.data,
                status=201
            )

        # Customers place orders from their own cart.
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = cart.items.select_related('menuitem')

        if not cart_items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=400
            )

        order = Order.objects.create(
            user=user,
            total=0
        )

        total = 0

        for cart_item in cart_items:
            unit_price = cart_item.menuitem.price
            total += unit_price * cart_item.quantity

            OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=unit_price
            )

        order.total = total
        order.save()

        cart_items.delete()

        serializer = self.get_serializer(order)

        return Response(
            serializer.data,
            status=201
        )
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrReadOnly]


class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = MenuItemPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['price']
    permission_classes = [IsManagerOrReadOnly]


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]    
class DeliveryCrewUserView(APIView):
    permission_classes = [IsManager]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=404
            )

        group, _ = Group.objects.get_or_create(name='Delivery Crew')
        user.groups.add(group)

        return Response(
            {
                'message': f'{user.username} added to Delivery Crew'
            },
            status=200
        )
class OrderAssignmentView(APIView):
    permission_classes = [IsManager]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=404
            )

        delivery_crew_id = request.data.get('delivery_crew')

        if not delivery_crew_id:
            return Response(
                {'error': 'delivery_crew is required'},
                status=400
            )

        try:
            delivery_crew = User.objects.get(id=delivery_crew_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Delivery crew user not found'},
                status=404
            )

        if not delivery_crew.groups.filter(
            name='Delivery Crew'
        ).exists():
            return Response(
                {'error': 'User is not in Delivery Crew'},
                status=400
            )

        order.delivery_crew = delivery_crew
        order.status = 1
        order.save()

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=200)    
class DeliveryStatusView(APIView):
    permission_classes = [IsDeliveryCrew]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(
                id=order_id,
                delivery_crew=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found or not assigned to you'},
                status=404
            )

        order.status = 2
        order.save()

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=200)    