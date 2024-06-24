import jwt 
from rest_framework.response import Response

from rest_framework import status



def Auth(model , request , serializer):
    if "Authentication" in request.headers:
            token = request.headers["Authentication"]
            try:
                user = jwt.decode(token,key = "backend" , algorithms="HS256")
                data = model.objects.filter(id =user["id"] , email = user["email"]).first()
                if data:
                    # print(data)
                    serializer = serializer(data)
                    # print(serializer.data)
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response("User Not Found",status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response("Please provide valid token",status=status.HTTP_400_BAD_REQUEST)    
    else:
        return Response("Please Provide header",status=status.HTTP_400_BAD_REQUEST)