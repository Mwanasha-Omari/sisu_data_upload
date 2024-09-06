from django.db import models

class JsonData(models.Model):
    data = models.JSONField()
    file = models.FileField(upload_to='uploads/')
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
