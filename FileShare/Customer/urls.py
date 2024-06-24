from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views




router = DefaultRouter()


# router.register("signup",views.SignupViewset,basename="signup")
router.register("login",views.LoginViewset,basename="login")




urlpatterns = router.urls+[
    path('signup/', views.SignUpView.as_view()),
    path('upload-file/', views.UploadFileView.as_view()),
    path("all-upload-files/",views.ListFilesView.as_view()),
    path("download-file/<int:file_id>/",views.DownloadFileView.as_view()),
    
]