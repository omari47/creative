from django.db import models

# Create your models here.
from django.db import models


class Workshop(models.Model):
    """Workshops offered by the company"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    location = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='workshops/')
    tags_str = models.TextField(blank=True, null=True)  # Store tags as comma-separated string
    seats_available = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def tags(self):
        """Convert stored string to list"""
        if not self.tags_str:
            return []
        return [tag.strip() for tag in self.tags_str.split(',')]

    def set_tags(self, tags_list):
        """Convert list to string for storage"""
        if not tags_list:
            self.tags_str = ''
        else:
            self.tags_str = ','.join(tags_list)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Workshop'
        verbose_name_plural = 'Workshops'
        ordering = ['date']


class Registration(models.Model):
    """Workshop registrations"""
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='workshop_registrations')
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workshop.title}"

    class Meta:
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
        unique_together = ['workshop', 'user']