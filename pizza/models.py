from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Topping(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    SIZE = (
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
    )
    size = models.CharField(max_length=1, choices=SIZE, default="M")
    topping = models.ManyToManyField(Topping)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        toppings = [str(i) for i in self.topping.all()]
        return f"{timezone.datetime.strftime(self.created, '%m/%d/%Y, %H:%M')} {self.size} {toppings} pizza"

    def is_order_expired(self):
        now = timezone.now()
        time_diff = now - self.created
        return time_diff.total_seconds() > 600
