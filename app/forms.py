from django import forms


class BestForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'autoresizing',
                                                        'placeholder': "What's on your mind?",
                                                        'id': 'new_post_text_form'}),
                           label='', max_length=10000, required=False)
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                    'id': 'new_post_image_form'}),
                             label='', required=False)


class NewProfilePictureUploadForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(), label='')





