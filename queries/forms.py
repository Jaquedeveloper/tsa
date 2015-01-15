from django import forms


class QueryForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square'}),
        max_length=50, required=False,
        label="Query title"
    )

    all_words = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square'}),
        max_length=50, required=False,
        label="All of these words"
    )

    phrase = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square'}),
        max_length=50, required=False,
        label="This exact phrase"
    )

    any_word = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square'}),
        max_length=50, required=False,
        label="Any of these words"
    )

    none_of = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square'}),
        max_length=50, required=False,
        label="None of these words"
    )

    hashtags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square'}),
        max_length=50, required=False,
        label="These hashtags"
    )

    users = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square'}),
        max_length=50, required=False,
        label="From these users"
    )

    date_from = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square', 'id': 'df'}), required=False, label="From this date",
        max_length=16
    )

    date_to = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square', 'id': 'dt'}), required=False, label="To this date",
        max_length=16
    )