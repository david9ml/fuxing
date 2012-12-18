from django.contrib import admin
from fuxing.activity.models import Activity

class ActivityAdmin(admin.ModelAdmin):
	list_display = ('activityname', 'pic_intro', 'txt_intro')

admin.site.register(Activity, ActivityAdmin)
