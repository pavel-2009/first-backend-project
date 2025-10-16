from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view



handler404 = 'core.views.page_not_found'

schema_view = get_schema_view(
   openapi.Info(
      title="Yatube API",
      default_version='v1',
      description="Документация для приложения Yatube",
      contact=openapi.Contact(email="admin@kittygram.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
    
urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
       name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), 
       name='schema-redoc'),
]