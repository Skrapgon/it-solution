from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('add_quote/', views.add_quote, name='add_quote'),
    path('my_quotes/', views.my_quotes, name='my_quotes'),
    path('random/', views.random_quote, name='random_quote'),
    path('', RedirectView.as_view(url='random/', permanent=True)),
    path('top_10_quotes/', views.top_10_quotes, name='top_10_quotes'),
    path('<int:pk>/like/', views.like_quote, name='like_quote'),
    path('<int:pk>/dislike/', views.dislike_quote, name='dislike_quote'),
]