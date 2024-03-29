from django.contrib import admin

from apps.skills.models import Availability, Skills, TimeSlot, Days, Expectation, Experience

# Register your models here.
admin.site.register(Availability)
admin.site.register(Skills)
# admin.site.register(TimeSlot)
admin.site.register(Days)
admin.site.register(Experience)
admin.site.register(Expectation)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('name', 'slug')
