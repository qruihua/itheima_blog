from django.urls import path
from home.views import IndexView
urlpatterns = [
    path('', IndexView.as_view(),name='index'),
]