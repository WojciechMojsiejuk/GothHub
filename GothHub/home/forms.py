from django import forms

from .models import Repository, File

class RepoCreationForm(forms.Form):
    name = forms.CharField(max_length=128)
    is_public = forms.BooleanField(required=False)

    class Meta:
        model = Repository
        fields = ('name', 'is_public')

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('dir',)
