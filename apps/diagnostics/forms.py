from django import forms

from .models import DiagnosticRequest


class DiagnosticRequestForm(forms.ModelForm):
    class Meta:
        model = DiagnosticRequest
        fields = ["name", "business", "email", "need", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Tu nombre", "autocomplete": "name"}),
            "business": forms.TextInput(attrs={"placeholder": "Nombre de tu negocio"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "nombre@negocio.com", "autocomplete": "email"}
            ),
            "need": forms.Select(),
            "message": forms.Textarea(
                attrs={"placeholder": "Cuéntanos brevemente qué quieres mejorar", "rows": 4}
            ),
        }
