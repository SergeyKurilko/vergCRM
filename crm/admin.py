from django.contrib import admin
from crm.models import (Client, ServiceRequest, Comment,
                        ImageForServiceRequest, UserProfile,
                        Task, Service, NoteForServiceRequest,
                        CostPriceCase, PartOfCostPriceCase)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageForServiceRequest)
class ImageForServiceRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_editable = ['is_completed', 'notifications',
                     'expired']
    list_display = ['id', 'title', 'is_completed', 'notifications',
                    'expired', 'created_at',
                    'must_be_completed_by',
                    'before_one_hour_deadline_notification',
                    'before_one_workday_deadline_notification']
    list_display_links = ['id', 'title']


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
