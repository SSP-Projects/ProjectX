from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/login/')),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^home/', views.home, name='home'), # This view will change if u re admin
    url(r'^admin/', views.admin, name='admin'),
]
