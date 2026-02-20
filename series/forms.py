from django import forms
from series.models import Series

spisok_bad_words = ["n-word"]



class CreateSeriesForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField()

    class Meta:
        model = Series
        fields = ["name", "description", "image", "price"]


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию, описанию или тегам...',
            'autocomplete': 'off'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from series.models import Category
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Все категории"