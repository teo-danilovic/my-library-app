# Create your views here.
import uuid
# import boto3
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Book, Tag, Photo, ReadingSession
from .forms import ReadingSessionForm, BookForm, TagForm

S3_BASE_URL = os.getenv('S3_BASE_URL', 'https://s3.amazonaws.com/')
BUCKET = os.getenv('S3_BUCKET', 'your-default-bucket-name') # Fallback if not set

# --- Home and About ---
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# --- Book Views (LoginRequiredMixin for all that modify or view user-specific data) ---
@login_required
def books_index(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'main_app/book_list.html', {'books': books})

@login_required
def books_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    tags_book_doesnt_have = Tag.objects.exclude(id__in=book.tags.all().values_list('id'))
    reading_session_form = ReadingSessionForm()
    return render(request, 'main_app/book_detail.html', {
        'book': book,
        'reading_session_form': reading_session_form,
        'tags': tags_book_doesnt_have
    })

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm # Using custom form
    template_name = 'main_app/book_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm # Using custom form
    template_name = 'main_app/book_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class BookDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    success_url = '/books/'
    template_name = 'main_app/book_confirm_delete.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

# --- ReadingSession Views ---
@login_required
def add_reading_session(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    form = ReadingSessionForm(request.POST)
    if form.is_valid():
        new_session = form.save(commit=False)
        new_session.book = book
        new_session.save()
    return redirect('books_detail', book_id=book_id)

@login_required
def delete_reading_session(request, book_id, session_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    session = get_object_or_404(ReadingSession, id=session_id, book=book)
    if request.method == 'POST': # Ensure it's a POST request for deletion
        session.delete()
        return redirect('books_detail', book_id=book_id)
    # Optionally, you could render a confirmation page if it's a GET request
    return redirect('books_detail', book_id=book_id) # Or an error page

# --- Tag Views (These are global, not user-specific for creation/listing) ---
class TagList(LoginRequiredMixin, ListView): # Users need to be logged in to see/use tags
    model = Tag
    template_name = 'main_app/tag_list.html'

class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'main_app/tag_detail.html'

class TagCreate(LoginRequiredMixin, CreateView): # Consider if only admins should create tags
    model = Tag
    form_class = TagForm
    template_name = 'main_app/tag_form.html'

class TagUpdate(LoginRequiredMixin, UpdateView): # Consider admin only
    model = Tag
    form_class = TagForm
    template_name = 'main_app/tag_form.html'

class TagDelete(LoginRequiredMixin, DeleteView): # Consider admin only
    model = Tag
    success_url = '/tags/'
    template_name = 'main_app/tag_confirm_delete.html'

# --- Association Views ---
@login_required
def assoc_tag(request, book_id, tag_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    tag = get_object_or_404(Tag, id=tag_id)
    book.tags.add(tag)
    return redirect('books_detail', book_id=book_id)

@login_required
def unassoc_tag(request, book_id, tag_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    tag = get_object_or_404(Tag, id=tag_id)
    book.tags.remove(tag)
    return redirect('books_detail', book_id=book_id)

# --- Photo (Book Cover) View ---
# @login_required
# def add_photo(request, book_id):
#     book = get_object_or_404(Book, id=book_id, user=request.user)
#     photo_file = request.FILES.get('photo-file', None)
#     if photo_file:
#         s3 = boto3.client('s3')
#         # Need a unique "key" for S3 / needs image file extension too
#         key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#         try:
#             s3.upload_fileobj(photo_file, BUCKET, key)
#             url = f"{S3_BASE_URL}{BUCKET}/{key}"
#             Photo.objects.create(url=url, book=book)
#         except Exception as e:
#             print('An error occurred uploading file to S3')
#             print(e)
#             # Optionally, add a Django message here for the user
#     return redirect('books_detail', book_id=book_id)

# --- Signup View ---
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('books_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
