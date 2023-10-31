from django.contrib import admin

from apps.skills.models import Availability, Skills, TimeSlot, Days, ChildCareNeed,Expectation

# Register your models here.
admin.site.register(Availability)
admin.site.register(Skills)
admin.site.register(TimeSlot)
admin.site.register(Days)
admin.site.register(ChildCareNeed)
admin.site.register(Expectation)
