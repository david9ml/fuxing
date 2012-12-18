from django.contrib import admin
from fuxing.room.models import Room, Reservation

class RoomAdmin(admin.ModelAdmin):
	list_display = ('roomname', 'volume', 'date_created', 'pic_intro', 'txt_intro')

admin.site.register(Room, RoomAdmin)

class ReservationAdmin(admin.ModelAdmin):
	list_display = ('customer', 'room', 'date_created', 'deadline', 'description')

admin.site.register(Reservation, ReservationAdmin)
