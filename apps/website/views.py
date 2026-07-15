from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.diagnostics.forms import DiagnosticRequestForm

from .content import CASE_SCENARIOS, METHOD_STAGES, SERVICES


def _diagnostic_page(
    request: HttpRequest, template_name: str, success_url: str, **context: object
) -> HttpResponse:
    form = DiagnosticRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request, "Recibimos tu solicitud. Te contactaremos para preparar el diagnóstico."
        )
        return redirect(success_url)
    return render(request, template_name, {"form": form, **context})


@require_http_methods(["GET", "POST"])
def home(request: HttpRequest) -> HttpResponse:
    return _diagnostic_page(
        request,
        "website/home.html",
        "home",
        services=SERVICES[:3],
        method_stages=METHOD_STAGES,
    )


def solutions(request: HttpRequest) -> HttpResponse:
    return render(request, "website/solutions.html", {"services": SERVICES})


def solution_detail(request: HttpRequest, slug: str) -> HttpResponse:
    service = next((item for item in SERVICES if item["slug"] == slug), None)
    if service is None:
        raise Http404("La solución solicitada no existe.")
    related = tuple(item for item in SERVICES if item["slug"] != slug)[:3]
    return render(
        request,
        "website/solution_detail.html",
        {"service": service, "related_services": related},
    )


def method(request: HttpRequest) -> HttpResponse:
    return render(request, "website/method.html", {"method_stages": METHOD_STAGES})


def cases(request: HttpRequest) -> HttpResponse:
    return render(request, "website/cases.html", {"case_scenarios": CASE_SCENARIOS})


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "website/about.html")


@require_http_methods(["GET", "POST"])
def contact(request: HttpRequest) -> HttpResponse:
    return _diagnostic_page(request, "website/contact.html", "contact")


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "website/privacy.html")
