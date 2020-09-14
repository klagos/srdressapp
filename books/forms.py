# -*- encoding: utf-8 -*-
from django import forms

class UserForm(forms.Form):
    id = forms.IntegerField(label='User ID')
    
class BookForm(forms.Form):
    id = forms.IntegerField(label='Book ISNB')