from django.db import models

# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to="images/preview/")
    html = models.TextField()
    css = models.TextField()
    js = models.TextField()

    def __str__(self):
        return self.name