from django.http import HttpResponse
from inventory.models import Order


def index(request):
    latest_order_list = Order.objects.order_by("delivery_date")[:5]
    output = ", ".join([o.supplier for o in latest_order_list])
    return HttpResponse(output)


def products(request, order_id):
    response = "You're looking at the details of order %s."
    return HttpResponse(response % order_id)

