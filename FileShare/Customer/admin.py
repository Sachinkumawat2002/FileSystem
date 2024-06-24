from typing import Any
from django.contrib import admin
from .models import * 
from django.contrib.auth.hashers import make_password
# Register your models here.

@admin.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email" ]
    search_fields = ["id"]
    list_filter = ["id"]

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if change:
            password = make_password(obj.password)
            obj.password = password
            return super().save_model(request, obj, form, change)
        else:
            password = make_password(obj.password)
            obj.password = password
        return super().save_model(request, obj, form, change)
    


@admin.register(UploadFile)

class UploadFileAdmin(admin.ModelAdmin):
    list_display = ["id", "uploaded_by" ,"uploaded_at"]
    search_fields = ["id"]  
