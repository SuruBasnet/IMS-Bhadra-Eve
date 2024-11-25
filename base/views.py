from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from .models import Product, ProductType
from .serializers import ProductSerializer, ProductTypeSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser,DjangoModelPermissions
from django.contrib.auth.models import Group

# Create your views here.
class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


class ProductTypeApiView(GenericAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request):
        product_type_objs = self.get_queryset()
        serializer = self.get_serializer(product_type_objs,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProductTypeDetailApiView(GenericAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


    def get(self,request,pk):
        product_type_obj = self.get_object()
        serializer = self.get_serializer(product_type_obj)
        return Response(serializer.data)
    
    def put(self,request,pk):
        product_type_obj = self.get_object()
        serializer = self.get_serializer(product_type_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        product_type_obj = self.get_object()
        product_type_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_employee(request):
    if request.user.groups.name == 'Management':
        employee_group = Group.objects.get(name='Employee')
        password = request.data.get('password')
        hash_password = make_password(password)
        data = request.data.copy()
        data['password'] = hash_password
        data['groups'] = employee_group.id
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else:
        return Response('Permission denied!',status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_management(request):
    management_group = Group.objects.get(name='Management')
    password = request.data.get('password')
    hash_password = make_password(password)
    data = request.data.copy()
    data['password'] = hash_password
    data['groups'] = management_group.id
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username,password=password)

    if user == None:
        return Response('Invalid username or password!',status=status.HTTP_400_BAD_REQUEST)
    else:
        token,_ = Token.objects.get_or_create(user=user)
        return Response(token.key)
    