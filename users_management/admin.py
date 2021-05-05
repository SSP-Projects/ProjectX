from django.contrib import admin
from .models import PermissionsAuxiliar, WeekDaysAuxiliar, ProfessionalCategoryAuxiliar, InteractionsTypesAuxiliar, NotificationTypesAuxiliar, Center, Employee, Notification, Schedule, Interaction


admin.site.register(PermissionsAuxiliar)
admin.site.register(WeekDaysAuxiliar)
admin.site.register(ProfessionalCategoryAuxiliar)
admin.site.register(InteractionsTypesAuxiliar)
admin.site.register(NotificationTypesAuxiliar)
admin.site.register(Center)
admin.site.register(Employee)
admin.site.register(Notification)
admin.site.register(Schedule)
admin.site.register(Interaction)
