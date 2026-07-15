from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.diagnostics.forms import DiagnosticRequestForm


@require_http_methods(["GET", "POST"])
def home(request):
    form = DiagnosticRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Recibimos tu solicitud. Te contactaremos para preparar el diagnóstico.")
        return redirect("home")
    return render(request, "website/home.html", {"form": form})
