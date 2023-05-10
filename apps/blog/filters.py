import django_filters
from django_filters.widgets import DateRangeWidget
from django import forms 

from apps.blog.models import Post




class PostFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        label="По дате создания",
        widget=DateRangeWidget(attrs={"type":"date", "class":"form-control"})
        )
    title = django_filters.CharFilter(
        lookup_expr="icontains", 
        widget=forms.TextInput(attrs={"class":"form-control"})
        )

    class Meta:
        model = Post
        fields = [
            "title",
            "created_at"
        ]