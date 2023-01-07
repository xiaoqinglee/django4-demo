from django import forms
from .models import Comment


class ShareWithEmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()  # 业务逻辑里没有使用这个field
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
