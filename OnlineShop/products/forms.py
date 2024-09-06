from django import forms


class CreateOrderForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "Иванов Иван Иванович",
        'minlength': 8,
        'maxlength': 50}))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "ivan@example.com"}))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "Район, улица, дом.корп.кв.",
        'minlength': 8,
        'maxlength': 256}))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "Москва",
        'minlength': 1,
        'maxlength': 30}))

    index = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': '555555'}))

