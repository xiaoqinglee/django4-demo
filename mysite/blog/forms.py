from django import forms


class ShareWithEmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()  # 业务逻辑里没有使用这个field
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
