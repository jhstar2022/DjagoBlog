from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse

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

        comment_form = CommentForm()


        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
        }
        
        return render(request, 'blog/post_detail.html', context)
    

class Write(View):
    # Mixin: LoginRequiredMixin
    def get(self, request):
        form = PostForm()
        context = {
            'form': form
        }
        return render(request, 'blog/post_form.html', context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) 
            post.writer = request.user
            post.save()
            return redirect('blog:list') 
        form.add_error(None, '폼이 유효하지 않습니다.')
        context = {
            'form': form
        }
        return render(request, 'blog/post_form.html')
    

class Update(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content']
    # success_url = reverse_lazy('blog:list')
    
    # intial 기능 사용 -> form에 값을 미리 넣어주기 위해서
    def get_initial(self):
        initial = super().get_initial() # UpdateView(generic view)에서 제공하는 initial(딕셔너리)
        post = self.get_object() # pk 기반으로 객체를 가져옴
        initial['title'] = post.title
        initial['content'] = post.content
        return initial
    
    def get_success_url(self): # get_absolute_url
        post = self.get_object() # pk 기반으로 현재 객체 가져오기
        return reverse('blog:detail', kwargs={ 'pk': post.pk })


class Delete(View):
    def post(self, request, pk): # post_id
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('blog:list')
    
    # 클래스 자체에 아예 접근하지 못하게 -> LoginRequiredMixin
    # Login이 되었을 때만 삭제 버튼이 보이게


### Comment
class CommentWrite(View):
    # def get(self, request):
    #     pass
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            # 사용자에게 댓글 내용을 받아옴
            content = form.cleaned_data['content']
            # 해당 아이디에 해당하는 글 불러옴
            post = Post.objects.get(pk=pk)
            # 댓글 객체 생성, create 메서드를 사용할 때는 save 필요 없음
            comment = Comment.objects.create(post=post, content=content)
            # comment = Comment(post=post) -> comment.save()
            return redirect('blog:detail', pk=pk)


class CommentDelete(View):
    def post(self, request, pk):
        # 지울 객체를 찾아야 한다. -> 댓글 객체
        comment = Comment.objects.get(pk=pk)
        # 상세페이지로 돌아가기
        post_id = comment.post.id
        # 삭제
        comment.delete()
        
        return redirect('blog:detail', pk=post_id)