from django import forms
from .models import KeyPair

class KeyPairForm(forms.ModelForm):
    class Meta:
        model = KeyPair
        fields = ['private_key', 'public_key_x', 'public_key_y']