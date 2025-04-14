from django.contrib import admin
from crm.models import (Client, ServiceRequest, Comment,
                        UserProfile, Task, Service,
                        NoteForServiceRequest,
                        CostPriceCase, PartOfCostPriceCase,
                        Reminder, DisplayNotification)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass





@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_editable = ['is_completed', 'notifications',
                     'expired', 'before_one_hour_deadline_notification',
                     'before_one_workday_deadline_notification']
    list_display = ['id', 'title', 'is_completed', 'notifications',
                    'expired', 'created_at',
                    'must_be_completed_by',
                    'before_one_hour_deadline_notification',
                    'before_one_workday_deadline_notification']
    list_display_links = ['id', 'title']
    list_per_page = 15


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(NoteForServiceRequest)
class NoteForServiceRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(CostPriceCase)
class CostPriceCaseAdmin(admin.ModelAdmin):
    pass


@admin.register(PartOfCostPriceCase)
class PartOfCostPriceCaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    pass

@admin.register(DisplayNotification)
class DisplayNotificationAdmin(admin.ModelAdmin):
    list_display = [
        "id", "type", "viewed"
    ]
    list_editable = ["viewed"]