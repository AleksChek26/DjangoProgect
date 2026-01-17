from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    name = forms.CharField(max_length=255, label="Название")
    description = forms.CharField(widget=forms.Textarea, label="Описание")
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Цена")

    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": f"Введите {field.label}"}
            )
        self.fields["name"].widget.attrs.update(
            {"class": "form-control form-control-lg", "autocomplete": "off"}
        )
        self.fields["description"].widget.attrs.update(
            {"rows": 5, "style": "resize: vertical;"}
        )
        self.fields["price"].widget.attrs.update(
            {"class": "form-control text-end", "step": "0.01", "min": "0"}
        )

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and any(word in name.lower() for word in self.FORBIDDEN_WORDS):
            for word in self.FORBIDDEN_WORDS:
                if word in name.lower():
                    raise ValidationError(
                        f'Слово "{word}" запрещено использовать в названии.'
                    )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description and any(
            word in description.lower() for word in self.FORBIDDEN_WORDS
        ):
            for word in self.FORBIDDEN_WORDS:
                if word in description.lower():
                    raise ValidationError(
                        f'Слово "{word}" запрещено использовать в описании.'
                    )
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price
