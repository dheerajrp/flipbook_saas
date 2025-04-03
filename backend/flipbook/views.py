import os
from django.conf import settings
from django.shortcuts import render
from pdf2image import convert_from_path
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import FlipBook
from .serializers import FlipBookSerializer

class FlipBookViewSet(viewsets.ModelViewSet):
    queryset = FlipBook.objects.all()
    serializer_class = FlipBookSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        flipbook = serializer.save(user=self.request.user)

        # ✅ Correct file paths
        pdf_path = os.path.join(settings.MEDIA_ROOT, str(flipbook.pdf_file))
        flipbook_folder = os.path.join(settings.MEDIA_ROOT, f"flipbooks/flipbook_{flipbook.id}")

        # ✅ Ensure directory exists
        os.makedirs(flipbook_folder, exist_ok=True)

        # ✅ Convert PDF to images
        images = convert_from_path(pdf_path, dpi=200)
        image_paths = []
        for i, image in enumerate(images):
            image_path = os.path.join(flipbook_folder, f"page_{i + 1}.jpg")
            image.save(image_path, "JPEG")
            image_paths.append(f"/media/flipbooks/flipbook_{flipbook.id}/page_{i + 1}.jpg")

        flipbook.flipbook_url = f"/flipbook/{flipbook.id}/"
        flipbook.save()

    

# ✅ User Registration
@api_view(["POST"])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_authenticated_user(request):
    return Response({"user": str(request.user)})


# ✅ Flipbook View
def flipbook_view(request, flipbook_id):
    flipbook_folder = os.path.join(settings.MEDIA_ROOT, f"flipbooks/flipbook_{flipbook_id}")
    media_url = settings.MEDIA_URL + f"flipbooks/flipbook_{flipbook_id}/"

    # Ensure the folder exists
    if not os.path.exists(flipbook_folder):
        return render(request, "flipbook.html", {"image_urls": []})

    # Get all images sorted
    images = sorted([media_url + img for img in os.listdir(flipbook_folder) if img.endswith(".jpg")])

    return render(request, "flipbook.html", {"image_urls": images})

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username  # Custom claim
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello {request.user.username}, you are authenticated!"})