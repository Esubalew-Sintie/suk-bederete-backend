from django.db import models


class Template(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('household', 'Household'),
        # Add more choices as needed
    ]

    TEMPLATE_TYPE_CHOICES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to="images/preview/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    template_type = models.CharField(max_length=7, choices=TEMPLATE_TYPE_CHOICES, default='free')

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=200)
    template = models.ForeignKey(Template, related_name='pages', on_delete=models.CASCADE)
    html = models.TextField()
    css = models.TextField()
    js = models.TextField()

    def __str__(self):
        return f"{self.template.name} - {self.name}"

    

    

