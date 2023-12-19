<!-- IMPORTS:START -->
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from .forms import {{model_name_cap}}Form
from .models import {{model_name_cap}}
<!-- IMPORTS:END -->


<!-- CODE:START -->
def {{model_name}}_list(request: HttpRequest):
    return TemplateResponse(
        request,
        "{{app_label}}/{{model_name}}_list.html",
        context={"{{model_name_plural}}": {{model_name_cap}}.objects.all()},
    )

def {{model_name}}_detail(request: HttpRequest, pk: int):
    {{model_name}} = get_object_or_404({{model_name_cap}}.objects, pk=pk)
    return TemplateResponse(
        request,
        "{{app_label}}/{{model_name}}_details.html",
        context={"{{model_name}}": {{model_name}}},
    )

def {{model_name}}_create(request:HttpRequest):
    form = {{model_name_cap}}Form(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("{{app_lab}}:{{model_name}}_list")
    return TemplateResponse(
        request,
        "{{app_label}}/{{model_name}}_create.html",
        context={"form": form},
    )

def {{model_name}}_update(request:HttpRequest, pk:int):
    {{model_name}} = get_object_or_404({{model_name_cap}}.objects, pk=pk)
    form = {{model_name_cap}}Form(request.POST or None, instance={{model_name}})
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("{{app_label}}:{{model_name}}_detail", pk=pk)
    return TemplateResponse(
        request,
        "{{app_label}}/{{model_name}}_update.html",
        context={"{{model_name}}": {{model_name}}, "form": form },
    )

@require_http_methods(["DELETE"])
def {{model_name}}_delete(request:HttpRequest, pk:int):
    {{model_name_cap}}.objects.filter(pk=pk).delete()
    return HttpResponse("OK")
<!-- CODE:END -->
