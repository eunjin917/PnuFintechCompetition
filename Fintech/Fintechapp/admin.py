from django.contrib import admin
from .models import Price, Predict, KakaoUser

# Register your models here.

admin.site.register(Price)
admin.site.register(Predict)
admin.site.register(KakaoUser)