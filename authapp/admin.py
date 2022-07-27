from django.contrib import admin
from .models import report,Room,Message,Post
# Register your models here.

admin.site.register(report)
admin.site.register(Room)
admin.site.register(Message)

class PostAdmin(admin.ModelAdmin):#makes the admin dashboard bit more elobrative for easy analysis
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post,PostAdmin)