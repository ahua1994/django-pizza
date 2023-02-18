from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .forms import PizzaForm
from .models import Pizza
# Create your views here.

# class based
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = "pizza/index.html"


class PizzaOrder(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Pizza
    form_class = PizzaForm
    template_name = "pizza/order.html"
    success_url = reverse_lazy("my_orders")
    success_message = "Your order is on the way!"

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ListPizzaOrders(LoginRequiredMixin, ListView):
    model = Pizza
    # so it can be accessed in the template with name of 'data'
    # default is 'object_list'
    context_object_name = "data"
    # default template_name is 'pizza/pizza_list.html'
    template_name = "pizza/list_orders.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class PizzaOrderUpdate(LoginRequiredMixin, UpdateView):
    model = Pizza
    form_class = PizzaForm
    template_name = "pizza/update_order.html"
    pk_url_kwarg = "id"  # default is pk
    success_url = reverse_lazy("my_orders")
    success_message = "Your order has been updated!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.get_object().id
        context["id"] = id
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user:
            messages.error(request, "Access Denied")
            return redirect("home")
        if self.object.is_order_expired():
            messages.error(request, "Pizza is already delivered.")
            return redirect("my_orders")
        return super().get(request, *args, **kwargs)


class PizzaOrderDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Pizza
    pk_url_kwarg = "id"  # default is pk
    success_url = reverse_lazy("my_orders")
    template_name = "pizza/delete_order.html"
    success_message = "Your order has been cancelled."

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user:
            messages.error(request, "Access Denied")
            return redirect("home")
        if self.object.is_order_expired():
            messages.error(request, "Pizza is already delivered.")
            return redirect("my_orders")
        return super().get(request, *args, **kwargs)
# function based


def home(request):
    return render(request, "pizza/index.html")


@login_required()
def order(request):
    form = PizzaForm()
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save()
            pizza.user = request.user
            pizza.save()
            messages.success(request, "Your order is on the way!")
            return redirect("home")
    context = {
        "form": form
    }
    return render(request, "pizza/order.html", context)


@login_required()
def list_orders(request):
    orders = Pizza.objects.filter(user=request.user)
    context = {
        "data": orders
    }
    return render(request, "pizza/list_orders.html", context)


@login_required()
def update_order(request, id):
    pizza = Pizza.objects.get(id=id)
    if pizza.user != request.user:
        messages.error(request, "Access Denied")
        return redirect("home")
    if pizza.is_order_expired():
        messages.error(request, "Pizza is already delivered.")
        return redirect("my_orders")
    # if timezone.now() > pizza.created + 2hrs:
    #     messages.error("Pizza is already delivered.")
    #     return redirect("my_orders")
    form = PizzaForm(instance=pizza)
    if request.method == "POST":
        form = PizzaForm(request.POST, instance=pizza)
        if form.is_valid():
            form.save()
            messages.success("Your order has been updated!")
            return redirect("my_orders")
    context = {
        "form": form,
        "id": id,
    }
    return render(request, "pizza/update_order.html", context)


@login_required()
def delete_order(request, id):
    pizza = Pizza.objects.get(id=id)
    if pizza.user != request.user:
        messages.error(request, "Access Denied")
        return redirect("home")
    if pizza.is_order_expired():
        messages.error(request, "Pizza is already delivered.")
        return redirect("my_orders")
    if request.method == 'POST':
        pizza.delete()
        messages.success(request, "Your order has been cancelled.")
        return redirect("home")
    return render(request, 'pizza/delete_order.html')
