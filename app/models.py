from django.db import models
import uuid

# Create your models here.

class Profile(models.Model):
    pid = models.CharField(max_length=12, unique=True, help_text='12 digit P-ID', editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    image1 = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    portfolio_availability = models.BooleanField(default=False)
    portfolio_url = models.URLField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    current_address = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    citizenship = models.CharField(max_length=100, blank=True, null=True)
    languages = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new object
            self.pid = str(uuid.uuid4().hex)[:12]  # Generate a unique 12-digit alphanumeric string
        super().save(*args, **kwargs)