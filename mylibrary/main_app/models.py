from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

STATUS_CHOICES = (
    ('TR', 'To Read'),
    ('RG', 'Currently Reading'),
    ('RD', 'Read'),
    ('DNF', 'Did Not Finish'),
)

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)] # 1 to 5 stars

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20, default='#DDDDDD') # Hex color

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tags_detail', kwargs={'pk': self.id})

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, blank=True)
    publication_year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='TR'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books_detail', kwargs={'book_id': self.id})

    class Meta:
        ordering = ['-created_at'] # Show newest books first by default

class ReadingSession(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_sessions')
    date_started = models.DateField(default=timezone.now)
    date_finished = models.DateField(blank=True, null=True)
    current_page = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        blank=True,
        null=True
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Reading session for {self.book.title} on {self.date_started}"

    class Meta:
        ordering = ['-date_started']

class Photo(models.Model): # For Book Covers
    url = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return f"Photo for book_id: {self.book_id} @{self.url}"
# Create your models here.
