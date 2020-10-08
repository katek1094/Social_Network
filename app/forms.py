from django import forms


class BestForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'autoresizing',
                                                        'placeholder': "What's on your mind?",
                                                        'id': 'new_post_form-textarea'}),
                           label='', max_length=10000, required=False)
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                    'id': 'new_post_form-file_upload'}),
                             label='', required=False)


class NewProfilePictureUploadForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(), label='')





