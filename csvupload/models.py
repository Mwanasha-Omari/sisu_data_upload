from django.db import models

class CsvUpload(models.Model):
    name = models.CharField(max_length=25)
    tsc_number = models.PositiveIntegerField(null=True, blank=True)  
    region = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)  

    def __str__(self):
        return self.name
