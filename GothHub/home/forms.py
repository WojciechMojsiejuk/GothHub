from django import forms

from .models import Repository, Catalog, File


class RepoCreationForm(forms.Form):
    name = forms.CharField(max_length=128)
    is_public = forms.BooleanField(required=False)

    class Meta:
        model = Repository
        fields = ('name', 'is_public')

    def __init__(self, *args, **kwargs):
        super(RepoCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['is_public'].label = 'Publiczne'


class CatalogCreationForm(forms.Form):
    name = forms.CharField(max_length=128)

    class Meta:
        model = Catalog
        fields = ('name')

    def __init__(self, *args, **kwargs):
        super(CatalogCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'


class FileUploadForm(forms.ModelForm):
    dir = forms.FileField()
    class Meta:
        model = File
        fields = ('dir', )
