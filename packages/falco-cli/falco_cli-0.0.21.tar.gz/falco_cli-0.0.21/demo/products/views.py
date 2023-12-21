from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from core.utils import paginate_queryset

from .forms import ProductForm
from .models import Product


def product_list(request: HttpRequest):
    products = Product.objects.all()
    return TemplateResponse(
        request,
        "products/product_list.html",
        context={"products": paginate_queryset(request, products)},
    )


def product_detail(request: HttpRequest, pk: int):
    product = get_object_or_404(Product.objects, pk=pk)
    return TemplateResponse(
        request,
        "products/product_detail.html",
        context={"product": product},
    )


def product_create(request: HttpRequest):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("products:product_list")
    return TemplateResponse(
        request,
        "products/product_create.html",
        context={"form": form},
    )


def product_update(request: HttpRequest, pk: int):
    product = get_object_or_404(Product.objects, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("products:product_detail", pk=pk)
    return TemplateResponse(
        request,
        "products/product_update.html",
        context={"product": product, "form": form},
    )


@require_http_methods(["DELETE"])
def product_delete(request: HttpRequest, pk: int):
    Product.objects.filter(pk=pk).delete()
    return HttpResponse("OK")
