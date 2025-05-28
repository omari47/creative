from django.db import models

# Create your models here.
from django.db import models

class Category(models.Model):
    """Categories for portfolio items"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class PortfolioItem(models.Model):
    """Portfolio items showcasing previous work"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='portfolio/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Portfolio Item'
        verbose_name_plural = 'Portfolio Items'
        ordering = ['-created_at']
