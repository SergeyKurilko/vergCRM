from django.contrib import admin
from crm.models import (Client, ServiceRequest, Comment,
                        ImageForServiceRequest, UserProfile,
                        Task, Service, NoteForServiceRequest)


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
    pass

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(NoteForServiceRequest)
class NoteForServiceRequestAdmin(admin.ModelAdmin):
    pass
