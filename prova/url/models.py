from django.db import models

# Create your models here.


class Url(models.Model):
    url_grande = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)

    def __str__(self):
        return self.url_grande

    def clean_input(self):
        input = self.cleaned_data['input']
        return input


