from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    #글 목록 조회
    path("", views.Index.as_view(), name='list'),
    path("detail/<int:pk>/", views.DetailView.as_view(), name='detail')
]
