from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from .forms import ProductForm
from .models import Product


def Product_list(request: HttpRequest):
    return TemplateResponse(
        request,
        "products/Product_list.html",
        context={"Products": Product.objects.all()},
    )


def Product_detail(request: HttpRequest, pk: int):
    Product = get_object_or_404(Product.objects, pk=pk)
    return TemplateResponse(
        request,
        "products/Product_details.html",
        context={"Product": Product},
    )


def Product_create(request: HttpRequest):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(":Product_list")
    return TemplateResponse(
        request,
        "products/Product_create.html",
        context={"form": form},
    )


def Product_update(request: HttpRequest, pk: int):
    Product = get_object_or_404(Product.objects, pk=pk)
    form = ProductForm(request.POST or None, instance=Product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("products:Product_detail", pk=pk)
    return TemplateResponse(
        request,
        "products/Product_update.html",
        context={"Product": Product, "form": form},
    )


@require_http_methods(["DELETE"])
def Product_delete(request: HttpRequest, pk: int):
    Product.objects.filter(pk=pk).delete()
    return HttpResponse("OK")
