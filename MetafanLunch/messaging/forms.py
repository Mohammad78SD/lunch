from django import forms
from .models import SharedFile
from lunch.models import CustomUser as User


class FileUploadForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # You might want to filter this based on your needs
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = SharedFile
        fields = ("name", "file", "recipients")
