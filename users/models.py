from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email, first_name, last_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Користувач повинен мати номер телефону')
        if not email:
            raise ValueError('Користувач повинен мати email')
        user = self.model(
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, email, first_name, last_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location_short = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=False)  

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    objects = CustomUserManager()

    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_by_natural_key(self, username):
        return self.get(phone_number=username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('social', 'Соціальна допомога'),
        ('medical', 'Медична допомога'),
        ('environment', 'Екологічна допомога'),
        ('humanitarian', 'Гуманітарна допомога')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_events')
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location_short = models.CharField(max_length=100)  
    location_full = models.TextField(max_length=100) 
    people_needed = models.PositiveIntegerField(default=0, blank=False) 
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def decrease_people_needed(self):
        if self.people_needed > 0:
            self.people_needed -= 1
            self.save()

    class Meta:
        ordering = ['start_date']
    
    def is_expired(self):
        
        return self.end_date < now().date()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='written_comments')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment from {self.author} to {self.recipient}"
    
class UserEventParticipation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} participation in {self.event.title}'
    
    class Meta:
        unique_together = ('user', 'event')

    
