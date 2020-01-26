from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from posts.views import (
    search,
    IndexView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    about,
    contact,
    policy,
    east,
    west,
    south,
    north,
    newsletter,


)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('blog/', PostListView.as_view(), name='post-list'),
    path('search/', search, name='search'),
    path('newsletter/', newsletter, name='newsletter'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('privacy&policy/',policy,name='policy'),
    path('EastSikkim', east, name='east'),
    path('WestSikkim', west, name='west'),
    path('NorthSikkim', north, name='north'),
    path('SouthSikkim', south, name='south')

]


urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'posts.views.not_found'
handler500 = 'posts.views.server_error'
handler403 = 'posts.views.permission_denied'
handler400 = 'posts.views.bad_request'
