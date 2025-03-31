from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    """Model for movies available for rent/purchase"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories_str = models.TextField(blank=True, null=True)  # Store as comma-separated string
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=3, decimal_places=1,
                                 validators=[MinValueValidator(0), MaxValueValidator(10)],
                                 default=0.0)
    trailer_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='movies/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def categories(self):
        """Convert stored string to list"""
        if not self.categories_str:
            return []
        return [cat.strip() for cat in self.categories_str.split(',')]

    def set_categories(self, categories_list):
        """Convert list to string for storage"""
        if not categories_list:
            self.categories_str = ''
        else:
            self.categories_str = ','.join(categories_list)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['-created_at']

#
# class Trailer(models.Model):
#     """Model for movie trailers featured on the homepage"""
#     title = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='trailers', null=True, blank=True)
#     trailer_url = models.URLField()
#     image = models.ImageField(upload_to='trailers/')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = 'Trailer'
#         verbose_name_plural = 'Trailers'
#         ordering = ['-created_at']
class Trailer(models.Model):
    """Model for movie trailers featured on the homepage"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='trailers', null=True, blank=True)
    trailer_url = models.URLField(help_text="YouTube or Vimeo video URL")
    image = models.ImageField(upload_to='trailers/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Trailer'
        verbose_name_plural = 'Trailers'
        ordering = ['-created_at']