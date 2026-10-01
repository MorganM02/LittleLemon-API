from django.urls import path
from .views import (
    CategoryListView,
    MenuItemListView,
    MenuItemDetailView,
    CartView,
    OrderView,
    DeliveryCrewUserView,
    OrderAssignmentView,
    DeliveryStatusView
)

urlpatterns = [
    path('categories', CategoryListView.as_view()),
    path('menu-items', MenuItemListView.as_view()),
    path('menu-items/<int:pk>', MenuItemDetailView.as_view()),
    path('cart', CartView.as_view()),
    path('orders', OrderView.as_view()),
    path('delivery-crew/<int:user_id>', DeliveryCrewUserView.as_view()),
    path('orders/<int:order_id>/assign', OrderAssignmentView.as_view()),
    path('orders/<int:order_id>/status', DeliveryStatusView.as_view()),
]