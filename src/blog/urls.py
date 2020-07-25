from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from posts.views import index, blog, post, search, post_delete, post_update, post_create, category_search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('blog/', blog, name="post-list"),
    path('post/<id>/', post,name="post-detail"),
    path('post/<id>/update', post_update,name="post-update"),
    path('post/<id>/delete', post_delete,name="post-delete"),
    path('create/', post_create,name="post-create"),
    path('search/', search ,name="search"),
    path('category/<str:cat>', category_search, name="category-search"),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)