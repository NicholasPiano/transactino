
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from apps.transactino.api import ProxyView
from apps.transactino.api.test.view import TransactinoTestView

urlpatterns = [
  path('', RedirectView.as_view(url='start/', permanent=True)),
  path('admin/', admin.site.urls),
  path('api/', ProxyView.as_view()),
  path('test/', TransactinoTestView.as_view()),
  path('readme/', TemplateView.as_view(template_name='readme.html')),
  path('start/', TemplateView.as_view(template_name='jormungand.html'))
]

if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
