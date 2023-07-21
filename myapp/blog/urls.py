from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    #글 목록 조회
    path("", views.Index.as_view(), name='list'),
    path("detail/<int:pk>/", views.DetailView.as_view(), name='detail'),
    path("write/", views.Write.as_view(), name='write'),
    path("detail/<int:pk>/edit/", views.Update.as_view(), name='edit'),
    path("detail/<int:pk>/delete/", views.Delete.as_view(), name='delete'),
    path("detail/<int:pk>/comment/edit/", views.CommentWrite.as_view(), name='cm-write'),
    path("detail/comment/<int:pk>/delete/", views.CommentDelete.as_view(), name='cm-delete')
]
