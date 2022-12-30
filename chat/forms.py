from django import forms
from .models import Chat_post
from ckeditor.widgets import CKEditorWidget


class Chat_view_Form(forms.ModelForm):
    content = forms.CharField(max_length=500, widget=CKEditorWidget(config_name='chat_config',
         attrs={'cols':110, 'rows': 5, 'placeholder': 'Say something..', 'class': 'form-control'}))
    class Meta:
        model = Chat_post
        fields = ['content']