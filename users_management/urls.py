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
    url(r'^ajax/get_notifications/', views.get_notifications_from_current_user, name='getNotifications'),
    url(r'^ajax/get_notification_to_show/', views.get_notification_by_id, name='getNotificationFromId'),
    url(r'^ajax/get_notification_to_show_/', views.get_notification_by_id_user, name='getNotificationFromIdUser'),
    url(r'^ajax/set_notification_as_viewed/', views.set_notification_as_viewed, name='setNotificationAsViewed'),
    url(r'^ajax/get_employee_job_interactions_dni/',views.get_employee_job_interactions_dni, name='get_employee_job_interactions_dni'),
    url(r'^ajax/modifyInteraction/',views.modifyInteraction, name='modifyInteraction'),
    url(r'^ajax/get_users_by_name/',views.get_users_by_name, name='get_users_by_name'),
    url(r'^ajax/get_employee_job_interactions_date_range/',views.get_employee_job_interactions_date_range, name='get_employee_job_interactions_date_range'),
]
