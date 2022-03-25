from django.contrib import admin
from . models import Users, Company, Attendance
admin.site.site_header = 'Boshqaruv paneli'
admin.site.site_title = 'Boshqaruv paneli'
admin.site.index_title = "Bosh sahifa"

class UsersAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'full_name', 'company_key', 'join_date', 'left_date']
    list_filter = ['company_key']

class AttendanceAdmin(admin.ModelAdmin):
    list_filter = ['user', 'company']
    list_display = ['user', 'company', 'join_date', 'left_date', 'date']
    date_hierarchy = 'date'

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['key', 'bot_token', 'channel_id', 'create_at']

admin.site.register(Users, UsersAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Attendance, AttendanceAdmin)
