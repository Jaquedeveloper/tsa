from django.forms import ModelForm

from tsa.models import Query


class QueryForm(ModelForm):
    class Meta:
        model = Query
        exclude = ['date', 'user']