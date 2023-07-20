from django.shortcuts import render
from django.views import View
from .models import Post, Comment

app_name= 'blog'
# Create your views here.
class Index(View):
    
    def get(self, request):
        posts = Post.objects.all()
        context = {
            "posts" : posts,
            "title" : "blog"
        }
        return render(request, 'blog/post_list.html', context)

class DetailView(View):

    def get(self, request, pk):

        # 해당 글
        post = Post.objects.get(pk=pk)
        # 댓글
        comments = Comment.objects.filter(post=post)

        context = {
            'post': post,
            'comments': comments,
        }
        
        return render(request, 'blog/post_detail.html', context)