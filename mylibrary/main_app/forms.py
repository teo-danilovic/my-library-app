from django import forms
from .models import Book, ReadingSession, Tag

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publication_year', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'publication_year': forms.NumberInput(attrs={'min': 0, 'max': 2100})
        }

class ReadingSessionForm(forms.ModelForm):
    class Meta:
        model = ReadingSession
        fields = ['date_started', 'date_finished', 'current_page', 'rating', 'notes']
        widgets = {
            'date_started': forms.DateInput(attrs={'type': 'date'}),
            'date_finished': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }