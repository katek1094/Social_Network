from django import forms


class BestForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"style": 'height: 2em; width: 100%;', 'class': 'autoresizing',
                                                        'placeholder': "What's on your mind?"}),
                           label='', max_length=10000, required=False)
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='', required=False)







