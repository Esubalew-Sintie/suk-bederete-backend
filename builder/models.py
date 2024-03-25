from django.db import models

# Create your models here.

class Page(models.Model):
    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    html = models.TextField()
    css = models.TextField()
    js = models.TextField()

    def __str__(self):
        return f"{self.template.name} - {self.name}"
    
class Template(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to="images/preview/")
    html = models.TextField()
    css = models.TextField()
    js = models.TextField()

    def __str__(self):
        return self.name