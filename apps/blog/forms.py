from django import forms

from apps.blog.models import Comment, Post

from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text":forms.Textarea(attrs={"class":"form-control"})
        }


from django_select2 import forms as s2forms

class CategorySelectWidget(s2forms.ModelSelect2TagWidget):
    search_fields = [
        "name__icontains"
    ]

class PostCreationForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget)

    class Meta:
        model = Post
        fields = [
            "title",
            "image",
            "description",
            "category",
            "is_active",
        ]

        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "category": CategorySelectWidget
            # "is_active":forms.CheckboxInput(attrs={"class":"form-control"}),
        }
        
