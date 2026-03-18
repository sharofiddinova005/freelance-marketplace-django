from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Bid)
admin.site.register(Contract)
admin.site.register(Review)