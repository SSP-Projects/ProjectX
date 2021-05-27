from django.conf.urls import url
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='accounts/login/')),
    url(r'^register/', views.register, name='register'),
    url(r'^home/', views.home, name='home'), # This view will change if u re admin
    url(r'^admin/', views.admin, name='admin'),
    url(r'^ajax/insert_job_interaction/',views.postInteraction, name='postInteraction'),
    url(r'^ajax/get_employee_job_interactions/',views.getEmployeeInteractions, name='getEmployeeInteractions'),
    url(r'^ajax/get_user/',views.getUser, name='getUser'),
    url(r'^ajax/notification_ad/', views.staff_send_notification, name='sendNotificationAd'),
    url(r'^ajax/notification/', views.send_notification, name='sendNotification'),
    url(r'^ajax/delete_user/',views.delete_user, name='delete_user'),
    url(r'^ajax/get_employee_job_interactions_dni/',views.get_employee_job_interactions_dni, name='get_employee_job_interactions_dni'),
    
]
