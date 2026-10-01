from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='menu_items'
    )

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    menuitem = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menuitem.title}"


class Order(models.Model):
    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Out for delivery'),
        (2, 'Delivered'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    delivery_crew = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='delivery_orders'
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    menuitem = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.quantity} x {self.menuitem.title}"