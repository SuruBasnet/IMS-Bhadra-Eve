from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from .models import Product, ProductType
from .serializers import ProductSerializer, ProductTypeSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductTypeApiView(GenericAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

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
