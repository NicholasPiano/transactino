
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from apps.transactino.api import TransactinoView
from apps.transactino.api.test.view import TransactinoTestView

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/', TransactinoView.as_view()),
  path('test/', TransactinoTestView.as_view()),
  path('readme/', TemplateView.as_view(template_name='readme.html')),
]
