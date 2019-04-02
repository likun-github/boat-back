from django.contrib import admin
from . import models
admin.site.register(models.User)
admin.site.register(models.Production)
admin.site.register(models.Merchant)
admin.site.register(models.Order)
admin.site.register(models.Period)
admin.site.register(models.Comment)
admin.site.register(models.Team)
admin.site.register(models.Cutting)
admin.site.register(models.Steam)

# Register your models here.
