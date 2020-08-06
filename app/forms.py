from django import forms


class BestForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"style": 'height: 8em'}),
                           label='', max_length=10000, required=False)
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='', required=False)







