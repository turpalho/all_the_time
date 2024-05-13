import json
import re
import hashlib
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from .serializers import (ReceiptSerializer,
                          ReceiptImageSerializer,
                          ProductSerializer,
                          StoreSerializer)
from .models import Receipt, Product, Store
from .services.utils import system_instruction
from .services.image_manager import process_receipt_image

from project.core.services.utils import encode_in_memory_upload_image
from project.core.services.openai_client import OpenaiClient
from project.core.services.supabase_client import SupabaseClient
# from project.users.models import User


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class ReceiptListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows receipts created or retrieved.
    """
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]


class ReceiptImageCreateView(generics.CreateAPIView):
    """
    API endpoint that allows receipts created.
    """
    serializer_class = ReceiptImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["image"]
        image = uploaded_file.read()
        extracted_data = process_receipt_image(image)
        extracted_data['created_by'] = request.user.id

        receipt_serializer = ReceiptSerializer(data=extracted_data)
        receipt_serializer.is_valid(raise_exception=True)
        receipt_serializer.save()

        return Response(receipt_serializer.data, status=status.HTTP_201_CREATED)


class ProductListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows product created or retrieved.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['creator']


class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
