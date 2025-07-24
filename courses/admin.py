from django.contrib import admin
from courses.models import Course, Module, Video, Subscription, WatchedVideo

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Video)
admin.site.register(Subscription)
admin.site.register(WatchedVideo)
