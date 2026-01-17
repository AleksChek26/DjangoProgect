from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "preview_image", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "preview_image": forms.FileInput(attrs={"class": "form-control-file"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
