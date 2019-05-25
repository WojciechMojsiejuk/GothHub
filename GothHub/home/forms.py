from django import forms

from .models import Repository,Catalog

class RepoCreationForm(forms.Form):
    name = forms.CharField(max_length=128)
    is_public = forms.BooleanField(required=False)

    class Meta:
        model = Repository
        fields = ('name', 'is_public')

class CatalogCreationForm(forms.Form):
    name = forms.CharField(max_length=128)

    class Meta:
        model = Catalog
        fields=('name')
