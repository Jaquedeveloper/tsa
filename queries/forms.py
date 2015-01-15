from django import forms

PRIVATE_CHOICES = (
    (False, "Private"),
    (True, "Public")
)


class QueryForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square', 'id': 'title'}),
        max_length=100, required=True,
        label="Query title (required)"
    )

    all_words = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square', 'id': 'all_words'}),
        max_length=50, required=False,
        label="All of these words"
    )

    phrase = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square', 'id': 'phrase'}),
        max_length=50, required=False,
        label="This exact phrase"
    )

    any_word = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square', 'id': 'any_word'}),
        max_length=50, required=False,
        label="Any of these words"
    )

    none_of = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square', 'id': 'none_of'}),
        max_length=50, required=False,
        label="None of these words"
    )

    hashtags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square', 'id': 'hashtags'}),
        max_length=100, required=False,
        label="These hashtags"
    )

    users = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'square', 'id': 'users'}),
        max_length=100, required=False,
        label="From these users"
    )

    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'square', 'id': 'df'}), required=False, label="From this date"
    )

    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'square', 'id': 'dt'}), required=False, label="To this date"
    )

    is_public = forms.ChoiceField(
        choices=PRIVATE_CHOICES, required=True, label="Access",
        widget=forms.Select(
            attrs={
                'class': 'full-width',
                'id': 'is_public'
            }
        )
    )