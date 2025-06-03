from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # Book URLs
    path('books/', views.books_index, name='books_index'),
    path('books/<int:book_id>/', views.books_detail, name='books_detail'),
    path('books/create/', views.BookCreate.as_view(), name='books_create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='books_update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='books_delete'),
    # Reading Session URLs
    path('books/<int:book_id>/add_reading_session/', views.add_reading_session, name='add_reading_session'),
    path('books/<int:book_id>/reading_session/<int:session_id>/delete/', views.delete_reading_session, name='delete_reading_session'),
    # Tag URLs
    path('tags/', views.TagList.as_view(), name='tags_index'),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name='tags_detail'),
    path('tags/create/', views.TagCreate.as_view(), name='tags_create'),
    path('tags/<int:pk>/update/', views.TagUpdate.as_view(), name='tags_update'),
    path('tags/<int:pk>/delete/', views.TagDelete.as_view(), name='tags_delete'),
    # Association URLs
    path('books/<int:book_id>/assoc_tag/<int:tag_id>/', views.assoc_tag, name='assoc_tag'),
    path('books/<int:book_id>/unassoc_tag/<int:tag_id>/', views.unassoc_tag, name='unassoc_tag'),
    # Photo URL
    # path('books/<int:book_id>/add_photo/', views.add_photo, name='add_photo'),
    # Auth
    path('accounts/signup/', views.signup, name='signup'),
    
]