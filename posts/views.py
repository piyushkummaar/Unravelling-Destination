from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from django.template import RequestContext
from posts.forms import CommentForm, PostForm
from posts.models import Post, Author, PostView
from posts.forms import EmailSignupForm
from posts.models import Signup
from .forms import ContactForm

form = EmailSignupForm()


def get_author(user):
    '''
    DOCSTRING : Information About Function
    INPUT : Get author object 
    OUTPUT : check the author exist or not
    '''
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class SearchView(View):
    '''
        DOCSTRING : INFORMATION ABOUT The SEARCH FUNCTION 
        INPUT : GET THE INPUT FROM THE QUERY SET
        OUTPUT : GIVES THE USER APPROPIATE RESUTE ABOUT ITS SERACH
        '''
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset
            
        }
        if queryset:
            return render(request, 'search_results.html', context)
        else:
            return render(request, 'search_results.html', context=True)

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


class IndexView(View):
    form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)[0:1]
        latest = Post.objects.order_by('-timestamp')[0:3]
        context = {
            'object_list': featured,
            'latest': latest,
            'form': self.form,
            'title': 'Home'
        }
        return render(request, 'index.html', context)


def newsletter(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_qs = Signup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, "You are already subscribed")
            else:
                form.save()
                messages.info(request, "Sucessfully subscribed")
    return HttpResponseRedirect('/')
    
    
class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'queryset'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['title'] = 'Blog'
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        context['title'] = 'Post'
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'post_confirm_delete.html'


def about(request):
    title = 'About'
    return render(request, 'about.html', {'title': title})


def contact(request):
    title = 'Contact'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()
    return render(request, 'contact.html' , {'title':title,'form' : form})

def policy(request):
    title = 'Privacy'
    return render(request, 'privacy&policy.html', {'title': title})

def east(request):
    title = 'EastSikkim'
    return render(request, 'allsikkim/east.html', {'title': title})

def west(request):
    title = 'WestSikkim'
    return render(request, 'allsikkim/west.html', {'title': title})

def north(request):
    title = 'NorthSikkim'
    return render(request, 'allsikkim/north.html', {'title': title})

def south(request):
    title = 'SouthSikkim'
    return render(request, 'allsikkim/south.html', {'title': title})

def server_error(request ,*args,**kwargs):
    return render(request, 'errors/404.html',status=404)


def not_found(request ,*args,**kwargs):
    return render(request, 'errors/500.html',status=500)


def permission_denied(request ,*args,**kwargs):
    return render(request, 'errors/404.html',status=403)


def bad_request(request ,*args,**kwargs):
    return render(request, 'errors/500.html',status=400)
