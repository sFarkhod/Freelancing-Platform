from django.contrib import admin
from user.models import User, UserConfirmation, Client, Freelancer, Feedback, Notification

admin.site.register(UserConfirmation)
admin.site.register(Client)
admin.site.register(Freelancer)
admin.site.register(Feedback)
admin.site.register(Notification)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'user_type']
    list_filter =  ['user_type',]