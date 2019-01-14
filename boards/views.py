from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView
from django.views.generic.edit import DeleteView
from boards.models import Board,Topic,Post
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.db.models import Count
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    paginate_by = 10
    template_name = 'boards/topics.html'

    def get_context_data(self,**kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board,pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies = Count('posts')-1)
        return queryset


@login_required()
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            user = request.user
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user,
            )
            return redirect('board_topics', pk=pk)
    else:
        form = NewTopicForm()
    return render(request,'boards/new_topic.html',{'form': form,'board':board})


class TopicPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 10

    def get_context_data(self,**kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('-created_at')
        return queryset

    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            message = self.request.POST.get('message'),
            topic = get_object_or_404(Topic, pk=self.kwargs.get('topic_pk')),
            created_by = self.request.user,
        )
        post.save()
        return redirect('topic_posts',**kwargs)


@login_required()
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic,pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts',pk=pk,topic_pk = topic_pk)
    else:
        form = PostForm()
    return render(request,'reply_topic.html',{'form':form,'topic':topic})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'boards/edit_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_pk'

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit = False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts',pk=post.topic.board.pk,topic_pk = post.topic.pk)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post

    pk_url_kwarg = 'post_pk'

    def get(self, request, *args, **kwargs):
        return self.delete(request,*args, **kwargs)

    def get_success_url(self, **kwargs):
            post = self.object
            return reverse_lazy('topic_posts', kwargs={'pk':post.topic.board.pk,'topic_pk':post.topic.pk})
