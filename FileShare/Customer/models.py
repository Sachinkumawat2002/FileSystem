from django.db import models

from core.validators import validate_file_type
# Create your models here.
# class CommanDetail(models.Model):
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()
#     is_active = models.BooleanField(default=True)


class User(models.Model):
    email = models.EmailField(max_length=256,unique = True)
    password = models.CharField(max_length=100)
    is_opsuser = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.email
    

class UploadFile(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', validators=[validate_file_type])
    uploaded_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
        return str(self.uploaded_by)  


