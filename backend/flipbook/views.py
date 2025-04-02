import os
from django.contrib.auth.models import User
from django.conf import settings
from pdf2image import convert_from_path
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import FlipBook
from .serializers import FlipBookSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class FlipBookViewSet(viewsets.ModelViewSet):
    queryset = FlipBook.objects.all()
    serializer_class = FlipBookSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        flipbook = serializer.save(user=self.request.user)

        # ✅ Get correct paths
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

        # ✅ Generate `index.html`
        flipbook_html_path = os.path.join(flipbook_folder, "index.html")
        flipbook_url = f"/media/flipbooks/flipbook_{flipbook.id}/index.html"

        with open(flipbook_html_path, "w") as f:
            f.write(self.generate_flipbook_html(image_paths))

        flipbook.flipbook_url = flipbook_url
        flipbook.save()

        print(f"✅ Flipbook saved at: {flipbook_folder}")  # Debugging line

    def generate_flipbook_html(self, image_paths):
        """Creates an HTML file that displays images as a flipbook"""
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Flipbook</title>
            <style>
                body {{ text-align: center; font-family: Arial, sans-serif; }}
                .flipbook-container {{ width: 80%; margin: auto; }}
                img {{ max-width: 100%; height: auto; display: block; margin: auto; }}
                .nav {{ margin-top: 20px; }}
                button {{ padding: 10px; margin: 5px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <div class="flipbook-container">
                <img id="flipbookImage" src="{image_paths[0]}" alt="Page 1">
            </div>
            <div class="nav">
                <button onclick="prevPage()">Previous</button>
                <button onclick="nextPage()">Next</button>
            </div>

            <script>
                var pages = {image_paths};
                var currentPage = 0;

                function updateImage() {{
                    document.getElementById('flipbookImage').src = pages[currentPage];
                }}

                function prevPage() {{
                    if (currentPage > 0) {{
                        currentPage--;
                        updateImage();
                    }}
                }}

                function nextPage() {{
                    if (currentPage < pages.length - 1) {{
                        currentPage++;
                        updateImage();
                    }}
                }}
            </script>
        </body>
        </html>
        """
        return html_template






# User Registration View
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
