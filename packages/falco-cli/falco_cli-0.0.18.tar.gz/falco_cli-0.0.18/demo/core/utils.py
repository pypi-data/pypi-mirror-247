from django.core.paginator import InvalidPage, Paginator
from django.http import Http404, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet


def paginate_queryset(request: HttpRequest, queryset:QuerySet, page_size:int = 20):
    """
    Paginates a queryset, and returns a page object.
    copied from https://github.com/carltongibson/neapolitan/blob/main/src/neapolitan/views.py
    """
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page") or 1
    try:
        page_number = int(page_number)
    except ValueError:
        if page_number == "last":
            page_number = paginator.num_pages
        else:
            msg = "Page is not 'last', nor can it be converted to an int."
            raise Http404(_(msg))

    try:
        return paginator.page(page_number)
    except InvalidPage as exc:
        msg = "Invalid page (%s): %s"
        raise Http404(_(msg) % (page_number, str(exc)))
