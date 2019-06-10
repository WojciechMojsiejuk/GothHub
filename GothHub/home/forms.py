from django import forms

from .models import Repository, Catalog, File, Version


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
        fields = ('name')


class FileUploadForm(forms.ModelForm):
    dir = forms.FileField()
    class Meta:
        model = File
        fields = ('dir', )


class ShowFileForm(forms.ModelForm):
    version_nr = forms.IntegerField()

    class Meta:
        model = Version
        fields = ('version_nr',)