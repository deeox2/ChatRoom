from django.contrib import admin
from chatRoomApi.models import Messages

class MessagesAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'message']

admin.site.register(Messages, MessagesAdmin)