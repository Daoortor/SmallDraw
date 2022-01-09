from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Category, Game, Word


class HostForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['n_rounds']
        labels = {
            'n_rounds': _('Number of rounds'),
        }


class StartForm(forms.Form):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Enter game id'}))
    player = forms.ChoiceField(choices=[('First', 'First'), ('Second', 'Second')])


class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name='name')


class WordForm(forms.Form):
    def __init__(self, words, *args, **kwargs):
        super(WordForm, self).__init__(*args, **kwargs)
        self.fields['word'] = forms.ChoiceField(choices=[(word, word) for word in words])
