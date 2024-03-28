from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
                  'title',
                  'image',
                  'category',
                  'summary',
                  'content',
                  ]
        widgets = {
          'summary': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"form-control"})
