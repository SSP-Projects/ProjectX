from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='accounts/login/')),
    url(r'^login/', views.login_view, name='login_view'),
    url(r'^register/', views.register, name='register'),
    url(r'^home/', views.home, name='home'), # This view will change if u re admin
    url(r'^admin/', views.admin, name='admin'),
    #home
    url(r'^ajax/insert_job_interaction/',views.postInteraction, name='postInteraction'),
    url(r'^ajax/get_employee_job_interactions/',views.getEmployeeInteractions, name='getEmployeeInteractions'),
    url(r'^ajax/get_employee_actual_status/',views.get_employee_actual_status, name='get_employee_actual_status'),
    #admin
    url(r'^ajax/get_user/',views.getUser, name='getUser'),
    url(r'^ajax/get_hours_from_range/',views.get_hours_from_range, name='get_hours_from_range'),
    url(r'^ajax/notification_ad/', views.staff_send_notification, name='sendNotificationAd'),
    url(r'^ajax/notification/', views.send_notification, name='sendNotification'),
    url(r'^ajax/desactivate_user/',views.desactivate_user, name='desactivate_user'),
    url(r'^ajax/activate_user/',views.activate_user, name='activate_user'),
    
    url(r'^ajax/get_notifications/', views.get_notifications_from_current_user, name='getNotifications'),
    url(r'^ajax/get_notification_to_show/', views.get_notification_by_id, name='getNotificationFromId'),
    url(r'^ajax/get_notification_to_show_/', views.get_notification_by_id_user, name='getNotificationFromIdUser'),
    url(r'^ajax/set_notification_as_viewed/', views.set_notification_as_viewed, name='setNotificationAsViewed'),
    url(r'^ajax/get_employee_job_interactions_dni/',views.get_employee_job_interactions_dni, name='get_employee_job_interactions_dni'),
    url(r'^ajax/modifyInteraction/',views.modifyInteraction, name='modifyInteraction'),
    url(r'^ajax/get_users_by_name/',views.get_users_by_name, name='get_users_by_name'),
    url(r'^ajax/get_employee_job_interactions_date_range/',views.get_employee_job_interactions_date_range, name='get_employee_job_interactions_date_range'),
    url(r'^ajax/get_pdf_from_month/',views.get_pdf_from_month, name='get_pdf_from_month'),
    url(r'^wuarrona',views.pdf_wuarron_testeo),
    url(r'^ajax/get_hours_from_current_month/',views.get_hours_from_current_month, name='get_hours_from_current_month'),
    url(r'^ajax/get_hours_from_desired_day/',views.get_interactions_from_day, name='get_interactions_from_day'),
]
