from typing import Any

from django import forms

from .models import DiagnosticRequest


class DiagnosticRequestForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        label="Sitio web",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "tabindex": "-1", "aria-hidden": "true"}
        ),
    )

    class Meta:
        model = DiagnosticRequest
        fields = ["name", "business", "country", "email", "need", "plan", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Tu nombre", "autocomplete": "name"}),
            "business": forms.TextInput(attrs={"placeholder": "Nombre de tu negocio"}),
            "country": forms.Select(attrs={"data-country-sync": ""}),
            "email": forms.EmailInput(
                attrs={"placeholder": "nombre@negocio.com", "autocomplete": "email"}
            ),
            "need": forms.Select(),
            "plan": forms.Select(),
            "message": forms.Textarea(
                attrs={"placeholder": "Cuéntanos brevemente qué quieres mejorar", "rows": 4}
            ),
        }

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean() or {}
        if cleaned_data.get("website"):
            raise forms.ValidationError("No fue posible procesar la solicitud.")
        return cleaned_data
