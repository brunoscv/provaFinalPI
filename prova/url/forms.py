from django import forms
from .models import *


class URLForm(forms.ModelForm):

    class Meta:
        model = Url
        fields = ('url_grande', )