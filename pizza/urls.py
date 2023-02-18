from django.urls import path
from .views import *

urlpatterns = [
    # path("", home, name="home"),
    path("", HomeView.as_view()),
    # path("order/", order, name="order"),
    path("order/", PizzaOrder.as_view(), name="order"),
    # path("myorders/", list_orders, name="my_orders"),
    path("myorders/", ListPizzaOrders.as_view(), name="my_orders"),
    # path("order/<int:id>/", update_order, name="update_order"),
    path("order/<int:id>/", PizzaOrderUpdate.as_view(), name="update_order"),
    # path("delete/<int:id>/", delete_order, name="delete_order"),
    path("delete/<int:id>/", PizzaOrderDelete.as_view(), name="delete_order"),
]
