from django.db import models
from django.contrib.auth.models import User

class FlipBook(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='flipbooks/')
    flipbook_url = models.URLField(blank=True, null=True)  # Flipbook URL
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Add this field

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flipbook = models.ForeignKey(FlipBook, on_delete=models.CASCADE)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.flipbook.title}"
