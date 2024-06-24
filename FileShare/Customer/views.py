from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import LoginSerializer, SignupSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.permissions import  AllowAny
from django.contrib.auth.hashers import check_password
from django.conf import settings

from .models import *
from .utils import send_mail
from core.permissions import *
import jwt
import uuid

from django.contrib.auth.hashers import make_password
# Create your views here.

class SignUpView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = urlsafe_base64_encode(force_bytes(user.pk))
            verify_link = f"http://{request.get_host()}/api/verify-email/{token}/"
            send_mail(
                "Verify your email",
                f"Click the link to verify your email: {verify_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )
            return Response({"message": "User created successfully. Check your email for verification link."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class LoginViewset(viewsets.ModelViewSet):
    serializer_class  = LoginSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        if request.data["password"] is not None or request.data["email"] is not None:
            user = User.objects.filter(email = request.data["email"]).first()
            if user:
                if check_password(request.data["password"],user.password):
                    token = jwt.encode({"id":user.id,"email":user.email,"Sachin":str(uuid.uuid4)},key="backend",algorithm="HS256")
                    return Response(token,status=status.HTTP_200_OK)
                else:
                    return Response("Invalid Credentials",status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("User Not Found",status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response("Please Provide the data")     



# class LoginViewset(viewsets.ModelViewSet):
ALLOWED_FILE_TYPES = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',     # .xlsx
                      'application/vnd.openxmlformats-officedocument.presentationml.presentation']  # .pptx

class UploadFileView(views.APIView):
    permission_classes = [UserAuth]
    # parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        print(request.user["id"])
        user = request.user
        if user["is_opsuser"] == False:
            return Response({'error': 'Only Ops User can upload files'}, status=status.HTTP_403_FORBIDDEN)

        file_obj = request.FILES['file']
        if file_obj.content_type not in ALLOWED_FILE_TYPES:
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
        us = User.objects.filter(id = int(user["id"])).first()
        file_instance = UploadFile(uploaded_by=us, file=file_obj)
        file_instance.save()
        return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)




class ListFilesView(views.APIView):
    permission_classes = [UserAuth]

    def get(self, request):
        if request.user["is_opsuser"]==False:
            files = UploadFile.objects.all()
            serializer = FileUploadSerializer(files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
    

class DownloadFileView(views.APIView):
    permission_classes = [UserAuth]

    def get(self, request, file_id, *args, **kwargs):
        file_instance = get_object_or_404(UploadFile, id=file_id)
        # print(file_instance)
        if request.user["is_opsuser"]:
            return Response({'error': 'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)

        download_url = jwt.encode({"file_id": file_instance.id}, "backend", algorithm="HS256")
        return Response({"download-link": f"http://{request.get_host()}/api/download-file/{download_url}/", "message": "success"}, status=status.HTTP_200_OK)    