from django.urls import path

from . import views

app_name = 'apiv1'
urlpatterns = [
    path('books/', views.BookListAPIView.as_view())
]
