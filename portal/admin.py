from django.contrib import admin
from fuxing.portal.models import Customer

class Customer_admin(admin.ModelAdmin):
	list_display = ('user', 'gender', 'cellphone', 'addition')
	list_filter = ('user', 'gender', 'cellphone', 'addition')

admin.site.register(Customer, Customer_admin)

