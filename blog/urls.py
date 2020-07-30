from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from posts.views import index, blog, post, post_delete, post_update, post_create,login_view, password_reset, register_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('blog/', blog, name="post-list"),
    path('post/<id>/', post,name="post-detail"),
    path('post/<id>/update', post_update,name="post-update"),
    path('post/<id>/delete', post_delete,name="post-delete"),
    path('create/', post_create,name="post-create"),
    path('search/', blog ,name="search"),
    path('category/<str:cat>', blog, name="category-search"),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', login_view, name="login"),
    path('password_reset/', password_reset, name='password-reset'),
    path('signup/', register_view, name="sign-up"),
    path('logout/',logout_view,name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)