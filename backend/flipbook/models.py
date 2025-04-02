import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class FlipBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to="pdfs/")
    flipbook_url = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def images_folder(self):
        """Returns the correct absolute folder path for images"""
        return os.path.join(settings.MEDIA_ROOT, "flipbooks", f"flipbook_{self.id}")
